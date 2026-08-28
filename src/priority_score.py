"""Motor de priorização de manutenção: cruza várias categorias de inspeção
de uma frota inteira e decide QUAL veículo olhar primeiro.

A ideia central (visão de Engenharia de Produção antes de automação): nem
toda categoria de manutenção tem o mesmo custo de ignorar. Calibragem errada
degrada rápido e é barata de checar; lubrificação atrasada tem folga maior.
A ordem de peso abaixo segue essa lógica de criticidade (referência: material
educativo de segurança de pneus tipo NHTSA TireWise sobre o impacto de
calibragem/sulco na frenagem e estabilidade), não é arbitrária — mas o valor
exato de cada peso é ajustável por frota/operação.
"""

from dataclasses import dataclass, field

CATEGORY_WEIGHTS = {
    "calibragem": 5,
    "sulco": 4,
    "alinhamento": 3,
    "oleo_filtros": 2,
    "lubrificacao": 1,
}


def severity_from_days_overdue(dias_atraso, prazo_maximo_dias):
    """Converte dias de atraso numa severidade 0.0-1.0, saturando em 1.0."""
    if dias_atraso <= 0:
        return 0.0
    return min(1.0, dias_atraso / prazo_maximo_dias)


@dataclass
class VehicleScore:
    vehicle: str
    score: float
    breakdown: dict = field(default_factory=dict)

    @property
    def worst_category(self):
        return max(self.breakdown, key=lambda cat: self.breakdown[cat])


def score_vehicle(vehicle, severities):
    """severities: dict categoria -> severidade 0.0-1.0 (só categorias conhecidas contam)."""
    breakdown = {}
    total = 0.0
    for category, severity in severities.items():
        weight = CATEGORY_WEIGHTS.get(category)
        if weight is None:
            continue
        contribution = weight * severity
        breakdown[category] = contribution
        total += contribution
    return VehicleScore(vehicle=vehicle, score=total, breakdown=breakdown)


def rank_fleet(fleet_severities, top_n=5):
    """fleet_severities: dict veiculo -> dict categoria -> severidade 0.0-1.0.

    Retorna os top_n veículos por score, do mais urgente pro menos urgente.
    """
    scores = [score_vehicle(vehicle, severities) for vehicle, severities in fleet_severities.items()]
    scores.sort(key=lambda vs: vs.score, reverse=True)
    return scores[:top_n]
