from packages.waste.recyclability import determine_recyclability
from packages.core.enums import RecyclabilityStatus as R


def test_unknown_material_without_confidence_is_unknown():
    assert determine_recyclability(None, "low", None) == R.unknown


def test_low_confidence_is_unknown():
    assert determine_recyclability("PET", "low", 0.3) == R.unknown


def test_high_contamination_blocks_recycling_even_for_recyclable_material():
    assert determine_recyclability("PET", "high", 0.9) == R.not_recyclable


def test_clean_recyclable_material_is_recyclable():
    assert determine_recyclability("PET", "low", 0.9) == R.recyclable


def test_medium_contamination_is_conditional():
    assert determine_recyclability("Aluminium", "medium", 0.8) == R.conditionally_recyclable


def test_non_recyclable_material_is_not_recyclable():
    assert determine_recyclability("StyrofoamMystery", "low", 0.9) == R.not_recyclable
