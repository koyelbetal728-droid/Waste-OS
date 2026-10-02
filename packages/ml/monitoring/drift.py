"""Compares production-time class distribution against training-time
distribution. Flags drift; does NOT auto-retrain (see architecture spec —
retraining always requires human approval)."""


def detect_class_drift(training_distribution: dict, production_labels: list[str], threshold: float = 0.15) -> dict:
    from collections import Counter
    counts = Counter(production_labels)
    total = sum(counts.values())
    if total == 0:
        return {"drifted": False, "reason": "no production data yet"}
    production_distribution = {k: v / total for k, v in counts.items()}
    drifted_classes = []
    for cls, train_share in training_distribution.items():
        prod_share = production_distribution.get(cls, 0.0)
        if abs(train_share - prod_share) > threshold:
            drifted_classes.append(cls)
    return {"drifted": bool(drifted_classes), "drifted_classes": drifted_classes,
            "production_distribution": production_distribution}
