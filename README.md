# 🚦 Qual veículo da frota precisa de manutenção HOJE?

> Sistema que lê os dados de inspeção de cada veículo — pneu, calibragem, alinhamento, óleo, lubrificação — e devolve uma lista ordenada: **comece por aqui, é o mais urgente.**

*(English summary below ⬇️)*

---

## 🎯 O problema

Numa frota com vários veículos, cada um gera dado de manutenção o tempo todo: sulco de pneu, pressão, alinhamento, óleo, lubrificação. Sem um sistema, isso vira uma de duas coisas — **decisão na intuição de um mecânico experiente** (que erra, esquece, ou não está lá no dia), ou **planilha manual que ninguém olha até o pneu estourar na estrada**. Nos dois casos, quem decide "qual veículo eu vejo primeiro" está adivinhando, não sabendo.

## 💡 A solução

O sistema faz duas coisas, na ordem:

1. **Olha os 4 pontos de sulco de cada roda** e já diz o que fazer: o pneu está gasto porque está desalinhado, ou porque a calibragem está errada? São ações diferentes (alinhar vs. calibrar), e o padrão de desgaste já denuncia qual — o sistema lê isso sozinho.
2. **Cruza essa leitura com as outras categorias de manutenção de toda a frota** (calibragem, sulco, alinhamento, óleo/filtros, lubrificação — nem todas pesam igual: calibragem errada degrada rápido, lubrificação atrasada tem mais folga) e devolve um **ranking**: começa por aqui.

### Exemplo real de saída

Frota de 7 veículos, situação bagunçada — cada um com um problema diferente, ninguém sabe por onde começar:

```
$ python scripts/priority_report.py --input sample_data/frota_severidade.json --top 5

TOP 5 — veículos que precisam de atenção agora:

1. VEICULO-07 — score 15.0 (pior categoria: calibragem)
2. VEICULO-03 — score 6.4 (pior categoria: sulco)
3. VEICULO-01 — score 6.4 (pior categoria: calibragem)
4. VEICULO-05 — score 6.0 (pior categoria: calibragem)
5. VEICULO-02 — score 1.9 (pior categoria: sulco)
```

Uma lista de "todo mundo precisa de alguma coisa" virou uma ordem de prioridade com o motivo ao lado — sem ninguém abrir aba por aba.

## 🔑 Por que isso importa

- **Menos pneu estourando na estrada** — o problema é sinalizado antes de virar parada não planejada, não depois.
- **A decisão para de depender de UMA pessoa** — hoje, "qual veículo eu olho primeiro" muitas vezes só um mecânico experiente sabe responder de cabeça. Isso vira algo que qualquer pessoa da operação consegue rodar.
- **Cada categoria pesa o que realmente pesa** — calibragem errada não é tratada igual a lubrificação atrasada, porque na vida real elas não têm a mesma urgência.

---

## 🧰 Por baixo do capô (pra quem quiser entrar no código)

Dois módulos de regra de negócio, independentes e testados:

- **`wheel_diagnosis`** — recebe as 4 leituras de sulco de uma roda (borda externa, centro externo, centro interno, borda interna) e devolve um veredito: `OK`, `ALINHAR_ESQUERDA`/`ALINHAR_DIREITA` (desgaste concentrado numa borda = ângulo/câmber), `CALIBRAR_MAIS`/`CALIBRAR_MENOS` (desgaste concentrado no centro ou nas bordas = pressão errada), ou `DESGASTE_IRREGULAR` (os dois padrões juntos).
- **`priority_score`** — recebe a severidade (0.0–1.0) de cada categoria de inspeção por veículo, pondera por criticidade (`calibragem > sulco > alinhamento > óleo/filtros > lubrificação`) e devolve o TOP N da frota que precisa de atenção agora.

```
4 sulcos da roda → wheel_diagnosis → veredito (alinhar/calibrar/ok/irregular)
Severidade por categoria × frota → priority_score → TOP N veículos mais urgentes
```

### Como rodar

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt

python scripts/priority_report.py --input sample_data/frota_severidade.json --top 5
```

### Testes

```bash
pytest tests/
```

14 testes cobrindo os 6 vereditos de roda (incluindo o caso misto/irregular) e o motor de score (peso por categoria, saturação de severidade por dias de atraso, ranqueamento, corte por top-N).

### Stack

- **Python** (stdlib) — sem dependência externa em produção
- **pytest** para os testes
- Desenhado a partir de uma automação real em Google Sheets + Apps Script (leitura de sulco → desenho automático de resumo visual pro mecânico, `onEdit`; dashboard de priorização 100% fórmula/`QUERY`) — a lógica de negócio é a mesma, reescrita aqui em Python puro e generalizado

### ⚠️ Limitações conhecidas

- **`wheel_diagnosis` confia na leitura de sulco como verdadeira** — não valida se os 4 números fazem sentido físico (ex.: valor negativo, fora da faixa de um pneu novo/gasto). Garbage in, garbage out.
- **Os limiares (3mm pra alinhamento, 2mm pra calibragem) são constantes fixas**, não calibradas por modelo/marca de pneu ou por eixo (dianteiro e traseiro desgastam diferente) — funcionam como regra geral, não como valor validado estatisticamente.
- **Só cobre 2 eixos de desgaste** (borda-a-borda e centro-vs-bordas) combinados em 5 vereditos. Padrão de desgaste que não se encaixa nesses dois (ex.: desgaste diagonal por problema de rolamento/suspensão) cai em `DESGASTE_IRREGULAR` sem indicar a causa real.
- **`priority_score` não considera custo, disponibilidade de peça/oficina ou criticidade da rota** — é um score de severidade de inspeção, não uma otimização operacional completa.
- **Categoria com nome digitado errado é ignorada em silêncio** (`score_vehicle` só soma o que reconhece) — um typo na severidade de entrada derruba a pontuação daquele veículo sem aviso nenhum.

### Contexto real e anonimização

Extraído e generalizado (sem nome de empresa, placa ou qualquer dado identificável) de um sistema de manutenção preventiva que estruturei para uma empresa de transporte rodofluvial de passageiros com garagem em Barcarena-PA. A versão em produção roda como fórmula/Apps Script dentro de uma planilha real do cliente e não é publicada aqui — o que este repositório mostra é a **lógica de decisão**, reescrita do zero em Python puro e testada isoladamente.

---

## 🇬🇧 English summary

**Which fleet vehicle needs maintenance today?** A system that reads per-vehicle inspection data (tire tread, pressure, alignment, oil, lubrication) and returns a ranked list — start here, this one's most urgent. Under the hood: `wheel_diagnosis` reads 4 tread-depth measurements per wheel and returns a verdict (alignment issue, pressure issue, or OK) based on wear pattern; `priority_score` ranks the fleet by weighted criticality across categories. Generalized from a real production system (Google Sheets + Apps Script) built for a passenger river-transport operator — no company name, plates, or identifiable data included.

**Stack:** Python (stdlib) · pytest.

---

## 👤 Autor

**Siandro Sena** — Engenheiro (Produção / Materiais), MBA em Inteligência Artificial. Automação de processos com IA, dados e eficiência operacional.
🔗 [LinkedIn](https://www.linkedin.com/in/siandro-sena-847712314)
