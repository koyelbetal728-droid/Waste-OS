"""Read-only endpoint exposing which classification model is currently
active — lets the frontend show whether results are from the untrained placeholder or a real trained model
without duplicating scanning.py's per-item result endpoint."""
from fastapi import APIRouter
from packages.ml.model_registry.registry import get_production_model

router = APIRouter()


@router.get("/model-status")
def model_status():
    entry = get_production_model("waste-classifier")
    if entry is None:
        return {"active": "mock", "version": "dev-0", "metrics": None}
    return {"active": "trained", "version": entry["version"], "metrics": entry["metrics"]}
