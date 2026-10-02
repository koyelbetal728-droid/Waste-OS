"""Deterministic baseline price estimator.
Clearly an estimate — never presented as a guaranteed market price.
Replace with packages/ml/pricing once a trained regression model exists."""

BASE_RATE_PER_KG = {
    "PET": 12.0,
    "Aluminium": 90.0,
    "Cardboard": 6.0,
    "Glass": 3.0,
    "Paper": 5.0,
}

QUALITY_MULTIPLIER = {"clean": 1.15, "mixed": 0.85, None: 1.0}


def estimate_price(material: str, quantity_kg: float, quality: str | None = None) -> tuple[float, float]:
    base = BASE_RATE_PER_KG.get(material, 4.0) * quantity_kg
    mult = QUALITY_MULTIPLIER.get(quality, 1.0)
    center = base * mult
    return round(center * 0.85, 2), round(center * 1.15, 2)  # (min, max) range
