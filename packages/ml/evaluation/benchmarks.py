"""Compare a candidate model's metrics against the current production
model before promotion — never promote blind."""
from packages.ml.model_registry.registry import get_production_model


def compare_to_production(model_name: str, candidate_metrics: dict, key: str = "accuracy") -> dict:
    current = get_production_model(model_name)
    if current is None:
        return {"has_baseline": False, "recommendation": "promote (no existing production model)"}
    current_value = current["metrics"].get(key)
    candidate_value = candidate_metrics.get(key)
    if current_value is None or candidate_value is None:
        return {"has_baseline": True, "recommendation": "manual_review (metric not comparable)"}
    better = candidate_value > current_value
    return {
        "has_baseline": True,
        "current": current_value,
        "candidate": candidate_value,
        "recommendation": "promote" if better else "keep_current",
    }
