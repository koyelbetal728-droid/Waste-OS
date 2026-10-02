"""Configurable point rules. Points are always calculated server-side —
never trust a client-provided value."""

POINT_RULES = {
    "pickup_verified": 20,
    "waste_recycled": 15,
    "correct_segregation": 10,
    "report_verified": 25,
    "food_donation": 30,
}


def points_for(reason: str) -> int:
    return POINT_RULES.get(reason, 0)
