"""Baseline forecasting model: weighted moving average with simple weekly
seasonality. This is an honest, real statistical baseline — not a trained
neural model. Swap in packages/ml/forecasting/train.py + a gradient-boosted
model once enough historical data exists; the interface stays the same."""
from datetime import date, timedelta


def forecast_daily_waste(history: list[dict], days_ahead: int = 7) -> list[dict]:
    """`history`: [{"date": "YYYY-MM-DD", "quantity_kg": float}], sorted ascending.
    Returns a forecast for the next `days_ahead` days with a naive confidence band."""
    if not history:
        return []

    values = [h["quantity_kg"] for h in history[-28:]]  # last 4 weeks if available
    avg = sum(values) / len(values)

    # weekly seasonality: average deviation per weekday, if enough history
    weekday_totals: dict[int, list[float]] = {}
    for h in history:
        d = date.fromisoformat(h["date"])
        weekday_totals.setdefault(d.weekday(), []).append(h["quantity_kg"])
    weekday_avg = {wd: sum(v) / len(v) for wd, v in weekday_totals.items() if v}

    last_date = date.fromisoformat(history[-1]["date"])
    forecast = []
    for i in range(1, days_ahead + 1):
        target_date = last_date + timedelta(days=i)
        wd = target_date.weekday()
        point_estimate = weekday_avg.get(wd, avg)
        forecast.append({
            "date": target_date.isoformat(),
            "forecast_kg": round(point_estimate, 1),
            "lower_bound_kg": round(point_estimate * 0.8, 1),
            "upper_bound_kg": round(point_estimate * 1.2, 1),
            "method": "weekday_moving_average",
        })
    return forecast
