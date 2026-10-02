from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from packages.database.session import get_db
from packages.database.models.waste import Waste
from packages.ml.forecasting.inference import forecast_daily_waste
from wasteos_api.schemas.forecasting import ForecastRequest, ForecastPoint
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.get("/history")
def real_history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Aggregates ACTUAL Waste rows by day — never a sample/fabricated
    series. Returns whatever real history exists (which may be empty or
    short on a fresh install); the frontend must not substitute fake data
    when this comes back thin."""
    rows = (
        db.query(cast(Waste.created_at, Date).label("day"), func.sum(Waste.quantity_kg).label("total_kg"))
        .filter(Waste.quantity_kg.isnot(None))
        .group_by("day")
        .order_by("day")
        .all()
    )
    return [{"date": str(r.day), "quantity_kg": float(r.total_kg)} for r in rows]


@router.post("", response_model=list[ForecastPoint])
def get_forecast(payload: ForecastRequest, user=Depends(get_current_user)):
    """Forecasts from whatever history the caller supplies. The frontend
    is expected to fetch it from GET /forecasting/history (real DB data)
    rather than construct it — this endpoint doesn't care where the caller
    got the numbers, but the app never fabricates them client-side."""
    history = [h.model_dump() for h in payload.history]
    return forecast_daily_waste(history, payload.days_ahead)
