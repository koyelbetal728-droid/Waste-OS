from pydantic import BaseModel


class HistoryPoint(BaseModel):
    date: str
    quantity_kg: float


class ForecastRequest(BaseModel):
    history: list[HistoryPoint]
    days_ahead: int = 7


class ForecastPoint(BaseModel):
    date: str
    forecast_kg: float
    lower_bound_kg: float
    upper_bound_kg: float
    method: str
