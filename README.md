# 🚦 Motor de Priorização de Manutenção de Frota

> Diagnóstico automático de roda (alinhamento/calibragem) a partir de 4 leituras de sulco, e um motor de score que cruza várias categorias de inspeção de uma frota inteira pra responder: **qual veículo olhar primeiro?**

*(English summary below ⬇️)*

---

## 🎯 O problema

Numa operação real de transporte rodofluvial de passageiros (garagem em Barcarena-PA), a manutenção preventiva de ~20 veículos gera dado de várias categorias — calibragem, sulco de pneu, alinhamento, óleo/filtros, lubrificação — cada uma com sua própria criticidade e prazo. Duas dores concretas:

1. **O mecânico olha 4 números de sulco e precisa decidir na hora**: esse pneu está gasto porque está desalinhado, ou porque a calibragem está errada? São ações diferentes (alinhar vs. calibrar), e o padrão entre os 4 pontos do sulco já denuncia qual é — mas só se alguém souber ler.
2. **O gestor de frota olha 20 veículos e precisa saber qual é mais urgente**, sem abrir aba por aba nem tratar todas as categorias como se pesassem igual (calibragem errada degrada rápido; lubrificação atrasada tem mais folga).

## 💡 A solução

Dois módulos de regra de negócio, independentes e testados:

- **`wheel_diagnosis`** — recebe as 4 leituras de sulco de uma roda (borda externa, centro externo, centro interno, borda interna) e devolve um veredito: `OK`, `ALINHAR_ESQUERDA`/`ALINHAR_DIREITA` (desgaste concentrado numa borda = ângulo/câmber), `CALIBRAR_MAIS`/`CALIBRAR_MENOS` (desgaste concentrado no centro ou nas bordas = pressão errada), ou `DESGASTE_IRREGULAR` (os dois padrões juntos).
- **`priority_score`** — recebe a severidade (0.0–1.0) de cada categoria de inspeção por veículo, pondera por criticidade (`calibragem > sulco > alinhamento > óleo/filtros > lubrificação`) e devolve o TOP N da frota que precisa de atenção agora.

```
4 sulcos da roda → wheel_diagnosis → veredito (alinhar/calibrar/ok/irregular)
Severidade por categoria × frota → priority_score → TOP N veículos mais urgentes
```

## ⚙️ Como rodar

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt

python scripts/priority_report.py --input sample_data/frota_severidade.json --top 5
```

## ✅ Testes

```bash
pytest tests/
```

14 testes cobrindo os 6 vereditos de roda (incluindo o caso misto/irregular) e o motor de score (peso por categoria, saturação de severidade por dias de atraso, ranqueamento, corte por top-N).

## 🧰 Stack

- **Python** (stdlib) — sem dependência externa em produção
- **pytest** para os testes
- Desenhado a partir de uma automação real em Google Sheets + Apps Script (leitura de sulco → desenho automático de resumo visual pro mecânico, `onEdit`; dashboard de priorização 100% fórmula/`QUERY`) — a lógica de negócio é a mesma, reescrita aqui em Python puro e generalizado

## 📊 Impacto

- Reduz o "qual pneu tem problema e por quê" de leitura manual pra veredito automático
- Reduz o "qual dos 20 veículos eu olho primeiro" de intuição pra score explicável
- Base validada de um sistema em produção numa operação real de transporte de passageiros

## 🌍 Contexto real e sobre a anonimização

Extraído e generalizado (sem nome de empresa, placa ou qualquer dado identificável) de um sistema de manutenção preventiva que estruturei para uma empresa de transporte rodofluvial de passageiros com garagem em Barcarena-PA. A versão em produção roda como fórmula/Apps Script dentro de uma planilha real do cliente e não é publicada aqui — o que este repositório mostra é a **lógica de decisão**, reescrita do zero em Python puro e testada isoladamente.

---

## 🇬🇧 English summary

**Fleet maintenance priority engine.** Two independent rule-based modules: `wheel_diagnosis` reads 4 tread-depth measurements per wheel and returns a verdict (alignment issue, pressure issue, or OK) based on wear pattern; `priority_score` ranks an entire fleet by weighted criticality across inspection categories (tire pressure > tread > alignment > oil/filters > lubrication) to answer "which vehicle needs attention first?". Generalized from a real production system (Google Sheets + Apps Script) built for a passenger river-transport operator — no company name, plates, or identifiable data included; the production formulas stay with the client, this repo shows the decision logic, rewritten from scratch in plain Python.

**Stack:** Python (stdlib) · pytest.

---

## 👤 Autor

**Siandro Sena** — Engenheiro (Produção / Materiais), MBA em Inteligência Artificial. Automação de processos com IA, dados e eficiência operacional.
🔗 [LinkedIn](https://www.linkedin.com/in/siandro-sena-847712314)
