from pydantic import BaseModel


class Stop(BaseModel):
    id: str | None = None
    latitude: float
    longitude: float


class RouteOptimizeRequest(BaseModel):
    depot: Stop
    stops: list[Stop]


class RouteOptimizeResponse(BaseModel):
    ordered_stops: list[Stop]
    total_distance_km: float
