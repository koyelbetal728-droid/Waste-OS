"""Food surplus eligibility — deterministic, conservative rules. Never makes
a food-safety determination from an image alone; requires explicit
freshness/condition input from the reporting party."""


def donation_eligibility(condition: str | None, hours_since_prep: float | None) -> dict:
    if condition == "spoiled":
        return {"eligible_for_donation": False, "recommended_action": "compost"}
    if hours_since_prep is not None and hours_since_prep > 4:
        return {"eligible_for_donation": False, "recommended_action": "compost", "reason": "exceeds safe holding window"}
    if condition in ("fresh", "unopened", "surplus"):
        return {"eligible_for_donation": True, "recommended_action": "donate"}
    return {"eligible_for_donation": False, "recommended_action": "manual_review"}
