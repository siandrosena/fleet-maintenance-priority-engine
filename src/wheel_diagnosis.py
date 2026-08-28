"""Diagnóstico de roda a partir de 4 leituras de sulco (borda-externa,
centro-externo, centro-interno, borda-interna).

Reimplementação simplificada, em Python puro, da regra usada num "resumo
visual pro mecânico" que rodava como desenho automático numa planilha real:
o padrão de desgaste entre as 4 posições do sulco denuncia o problema físico
da roda antes de olhar o pneu de perto.

Regra de física de pneu (não é chute): pneu desalinhado desgasta mais de UM
lado (diferença grande entre as duas bordas); pneu com pressão errada
desgasta ou o centro ou as bordas de forma simétrica.
"""

from dataclasses import dataclass
from enum import Enum


class WheelVerdict(Enum):
    OK = "ok"
    ALINHAR_ESQUERDA = "alinhar_esquerda"
    ALINHAR_DIREITA = "alinhar_direita"
    CALIBRAR_MAIS = "calibrar_mais"  # bordas mais gastas que o centro = pneu murcho
    CALIBRAR_MENOS = "calibrar_menos"  # centro mais gasto que as bordas = pneu cheio demais
    DESGASTE_IRREGULAR = "desgaste_irregular"


DIFERENCA_ALINHAMENTO_MM = 3.0
DIFERENCA_CALIBRAGEM_MM = 2.0


@dataclass
class WheelReading:
    borda_externa: float
    centro_externo: float
    centro_interno: float
    borda_interna: float

    @property
    def bordas(self):
        return (self.borda_externa, self.borda_interna)

    @property
    def media_bordas(self):
        return sum(self.bordas) / 2

    @property
    def media_centro(self):
        return (self.centro_externo + self.centro_interno) / 2


def diagnose_wheel(reading):
    delta_bordas = reading.borda_externa - reading.borda_interna
    delta_centro_bordas = reading.media_centro - reading.media_bordas

    desalinhado = abs(delta_bordas) >= DIFERENCA_ALINHAMENTO_MM
    pressao_errada = abs(delta_centro_bordas) >= DIFERENCA_CALIBRAGEM_MM

    if desalinhado and pressao_errada:
        return WheelVerdict.DESGASTE_IRREGULAR

    if desalinhado:
        # lado com MENOR sulco é o lado gasto -> alinhar pra esse lado
        return WheelVerdict.ALINHAR_ESQUERDA if delta_bordas < 0 else WheelVerdict.ALINHAR_DIREITA

    if pressao_errada:
        # bordas mais gastas (sulco menor) que o centro = pneu murcho -> calibrar+
        return WheelVerdict.CALIBRAR_MAIS if delta_centro_bordas > 0 else WheelVerdict.CALIBRAR_MENOS

    return WheelVerdict.OK
