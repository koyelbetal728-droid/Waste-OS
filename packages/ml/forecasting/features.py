"""Feature engineering for waste forecasting — shared between training and
inference so they can never silently diverge."""
from datetime import date


def build_features(date_str: str) -> dict:
    d = date.fromisoformat(date_str)
    return {
        "weekday": d.weekday(),
        "month": d.month,
        "is_weekend": int(d.weekday() >= 5),
    }
