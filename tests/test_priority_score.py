import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from priority_score import score_vehicle, rank_fleet, severity_from_days_overdue


def test_severity_from_days_overdue_saturates_at_one():
    assert severity_from_days_overdue(0, 30) == 0.0
    assert severity_from_days_overdue(15, 30) == 0.5
    assert severity_from_days_overdue(300, 30) == 1.0


def test_negative_days_overdue_is_zero_severity():
    assert severity_from_days_overdue(-5, 30) == 0.0


def test_calibragem_weighs_more_than_lubrificacao():
    same_severity = {"calibragem": 1.0}
    other = {"lubrificacao": 1.0}
    assert score_vehicle("V1", same_severity).score > score_vehicle("V2", other).score


def test_unknown_category_is_ignored_not_crashed():
    result = score_vehicle("V1", {"categoria_inexistente": 1.0})
    assert result.score == 0.0


def test_worst_category_points_to_highest_contribution():
    result = score_vehicle("V1", {"calibragem": 0.2, "sulco": 1.0})
    # sulco: peso 4 * 1.0 = 4.0 ; calibragem: peso 5 * 0.2 = 1.0 -> sulco vence mesmo com peso menor
    assert result.worst_category == "sulco"


def test_rank_fleet_orders_by_score_descending():
    fleet = {
        "V1": {"calibragem": 0.1},   # 5 * 0.1 = 0.5
        "V2": {"calibragem": 1.0, "sulco": 1.0},  # 5 + 4 = 9.0
        "V3": {"lubrificacao": 1.0},  # 1 * 1.0 = 1.0
    }
    ranking = rank_fleet(fleet, top_n=3)
    assert [v.vehicle for v in ranking] == ["V2", "V3", "V1"]


def test_rank_fleet_respects_top_n():
    fleet = {f"V{i}": {"calibragem": i / 10} for i in range(1, 8)}
    ranking = rank_fleet(fleet, top_n=5)
    assert len(ranking) == 5
    assert ranking[0].vehicle == "V7"
