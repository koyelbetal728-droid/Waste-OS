"""Real MAE/RMSE against a chronological (non-shuffled) held-out split."""
import numpy as np


def evaluate_forecast(model, X_test, y_test) -> dict:
    if len(y_test) == 0:
        return {"mae": None, "rmse": None, "test_set_size": 0}
    y_pred = model.predict(X_test)
    mae = float(np.mean(np.abs(y_test - y_pred)))
    rmse = float(np.sqrt(np.mean((y_test - y_pred) ** 2)))
    return {"mae": round(mae, 2), "rmse": round(rmse, 2), "test_set_size": len(y_test)}
