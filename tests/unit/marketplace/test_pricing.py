from packages.marketplace.pricing import estimate_price


def test_known_material_returns_positive_range():
    lo, hi = estimate_price("PET", 10)
    assert lo > 0 and hi > lo


def test_unknown_material_uses_default_rate():
    lo, hi = estimate_price("MysteryMaterial", 10)
    assert lo > 0


def test_clean_quality_prices_higher_than_mixed():
    clean_lo, clean_hi = estimate_price("PET", 10, "clean")
    mixed_lo, mixed_hi = estimate_price("PET", 10, "mixed")
    assert clean_hi > mixed_hi


def test_zero_quantity_returns_zero_range():
    lo, hi = estimate_price("PET", 0)
    assert lo == 0 and hi == 0
