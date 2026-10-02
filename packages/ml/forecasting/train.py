"""Trains a real (small) linear regression over weekday/month features —
genuinely fit to whatever historical data you provide, not fabricated.
This is intentionally simple; it exists to be replaced by a gradient-
boosted model (packages/ml/forecasting) once enough historical data exists
per db/seeds or a real waste-collection dataset. The API's baseline
(inference.py's forecast_daily_waste) keeps working with zero data — this
trainer only helps once real history exists."""
from datetime import datetime
from pathlib import Path
import pickle
from sklearn.linear_model import LinearRegression
from packages.ml.forecasting.dataset import build_dataset
from packages.ml.forecasting.evaluate import evaluate_forecast
from packages.ml.model_registry.registry import register_model

ARTIFACT_DIR = Path(__file__).resolve().parents[3] / "models" / "artifacts"


def train(history: list[dict]):
    if len(history) < 14:
        print(f"Not enough history to train: {len(history)} points (need >=14 days).")
        return None

    split = int(len(history) * 0.8)
    train_history, test_history = history[:split], history[split:]

    X_train, y_train = build_dataset(train_history)
    X_test, y_test = build_dataset(test_history)

    model = LinearRegression()
    model.fit(X_train, y_train)

    metrics = evaluate_forecast(model, X_test, y_test)
    print("Forecast evaluation:", metrics)

    version = datetime.utcnow().strftime("v%Y%m%d%H%M%S")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACT_DIR / f"waste-forecast-{version}.pkl"
    with open(artifact_path, "wb") as f:
        pickle.dump(model, f)

    register_model("waste-forecast", version, str(artifact_path), metrics)
    return version
