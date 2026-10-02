"""Landfill diversion — a straightforward, honest count: kg of waste marked
recyclable/reused/recovered instead of ending up in the 'not_recyclable'
bucket. No hidden multipliers."""


def diversion_rate(total_kg: float, diverted_kg: float) -> float:
    if total_kg <= 0:
        return 0.0
    return round((diverted_kg / total_kg) * 100, 1)
