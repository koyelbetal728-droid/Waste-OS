"""Persist a reproducible evaluation report alongside the model artifact."""
import json
from pathlib import Path
from datetime import datetime

REPORTS_DIR = Path(__file__).resolve().parents[3] / "models" / "manifests"


def write_report(model_name: str, version: str, metrics: dict):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"{model_name}-{version}-report.json"
    with open(path, "w") as f:
        json.dump({"model": model_name, "version": version, "metrics": metrics,
                    "generated_at": datetime.utcnow().isoformat()}, f, indent=2)
    return str(path)
