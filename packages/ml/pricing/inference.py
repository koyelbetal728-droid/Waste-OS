from packages.ml.pricing.model import estimate_price


def predict_price(material: str, quantity_kg: float, quality: str | None = None) -> dict:
    price_min, price_max = estimate_price(material, quantity_kg, quality)
    return {"estimated_min": price_min, "estimated_max": price_max, "model_version": "baseline-v1"}
