"""Configurable carbon-avoidance estimator. Coefficients are clearly
labeled as configurable defaults, not certified emission factors — real
deployments should replace these with locally verified figures."""

# kg CO2e avoided per kg of material recycled instead of landfilled.
# Defaults drawn from commonly cited (but not certified-for-this-app)
# EPA WARM-style ballpark figures — treat as a rough estimate only.
CO2E_PER_KG_RECYCLED = {
    "PET": 1.5,
    "Aluminium": 9.0,
    "Cardboard": 0.9,
    "Glass": 0.3,
    "Paper": 0.9,
    "default": 0.5,
}


def estimate_carbon_avoided_kg(material: str, quantity_kg: float) -> float:
    factor = CO2E_PER_KG_RECYCLED.get(material, CO2E_PER_KG_RECYCLED["default"])
    return round(factor * quantity_kg, 2)
