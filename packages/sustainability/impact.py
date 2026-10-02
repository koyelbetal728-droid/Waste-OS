"""Aggregates real per-user/per-org waste rows into a sustainability
summary — computed from the database, never a fabricated placeholder."""
from packages.sustainability.carbon import estimate_carbon_avoided_kg
from packages.sustainability.landfill import diversion_rate


def summarize(waste_rows: list) -> dict:
    """`waste_rows`: ORM Waste objects with .material, .quantity_kg,
    .recyclability (RecyclabilityStatus)."""
    total_kg = sum((w.quantity_kg or 0) for w in waste_rows)
    diverted_rows = [w for w in waste_rows if w.recyclability and w.recyclability.value == "recyclable"]
    diverted_kg = sum((w.quantity_kg or 0) for w in diverted_rows)
    carbon_avoided = sum(estimate_carbon_avoided_kg(w.material or "default", w.quantity_kg or 0) for w in diverted_rows)

    return {
        "total_kg": round(total_kg, 2),
        "diverted_kg": round(diverted_kg, 2),
        "diversion_rate_pct": diversion_rate(total_kg, diverted_kg),
        "estimated_carbon_avoided_kg_co2e": round(carbon_avoided, 2),
        "note": "Estimates use configurable, non-certified emission factors — see packages/sustainability/carbon.py.",
    }
