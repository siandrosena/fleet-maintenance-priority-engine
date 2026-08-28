import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from wheel_diagnosis import WheelReading, WheelVerdict, diagnose_wheel


def test_even_wear_is_ok():
    reading = WheelReading(10, 10, 10, 10)
    assert diagnose_wheel(reading) == WheelVerdict.OK


def test_small_variation_within_tolerance_is_ok():
    reading = WheelReading(10, 9, 9, 10)
    assert diagnose_wheel(reading) == WheelVerdict.OK


def test_outer_edge_worn_suggests_alinhar_esquerda():
    reading = WheelReading(borda_externa=6, centro_externo=8, centro_interno=8, borda_interna=10)
    assert diagnose_wheel(reading) == WheelVerdict.ALINHAR_ESQUERDA


def test_inner_edge_worn_suggests_alinhar_direita():
    reading = WheelReading(borda_externa=10, centro_externo=8, centro_interno=8, borda_interna=6)
    assert diagnose_wheel(reading) == WheelVerdict.ALINHAR_DIREITA


def test_edges_more_worn_than_center_suggests_calibrar_mais():
    reading = WheelReading(borda_externa=6, centro_externo=10, centro_interno=10, borda_interna=6)
    assert diagnose_wheel(reading) == WheelVerdict.CALIBRAR_MAIS


def test_center_more_worn_than_edges_suggests_calibrar_menos():
    reading = WheelReading(borda_externa=10, centro_externo=6, centro_interno=6, borda_interna=10)
    assert diagnose_wheel(reading) == WheelVerdict.CALIBRAR_MENOS


def test_mixed_pattern_is_irregular():
    reading = WheelReading(borda_externa=4, centro_externo=10, centro_interno=10, borda_interna=10)
    assert diagnose_wheel(reading) == WheelVerdict.DESGASTE_IRREGULAR
