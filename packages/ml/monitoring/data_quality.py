"""Basic input data-quality checks — run before training or as a periodic
scheduler job, never silently trains on unvalidated data."""


def check_class_balance(labels: list[str]) -> dict:
    from collections import Counter
    counts = Counter(labels)
    total = sum(counts.values())
    if total == 0:
        return {"total": 0, "warning": "no data"}
    distribution = {k: round(v / total, 3) for k, v in counts.items()}
    min_class_share = min(distribution.values()) if distribution else 0
    return {
        "total": total,
        "distribution": distribution,
        "warning": "severe_imbalance" if min_class_share < 0.05 else None,
    }
