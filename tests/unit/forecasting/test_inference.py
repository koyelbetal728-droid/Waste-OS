from packages.ml.forecasting.inference import forecast_daily_waste


def test_empty_history_returns_empty_forecast():
    assert forecast_daily_waste([]) == []


def test_forecast_returns_requested_number_of_days():
    history = [{"date": f"2026-01-{d:02d}", "quantity_kg": 800 + d} for d in range(1, 15)]
    forecast = forecast_daily_waste(history, days_ahead=5)
    assert len(forecast) == 5


def test_forecast_bounds_are_ordered():
    history = [{"date": f"2026-01-{d:02d}", "quantity_kg": 800 + d} for d in range(1, 15)]
    forecast = forecast_daily_waste(history, days_ahead=3)
    for point in forecast:
        assert point["lower_bound_kg"] <= point["forecast_kg"] <= point["upper_bound_kg"]
