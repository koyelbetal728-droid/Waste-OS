from pydantic import BaseModel
from .common import UUIDStr


class Stop(BaseModel):
    id: UUIDStr | None = None
    latitude: float
    longitude: float


class RouteOptimizeRequest(BaseModel):
    depot: Stop
    stops: list[Stop]


class RouteOptimizeResponse(BaseModel):
    ordered_stops: list[Stop]
    total_distance_km: float
