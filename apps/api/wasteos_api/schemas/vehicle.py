from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class VehicleCreateRequest(BaseModel):
    label: str
    capacity_kg: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VehicleResponse(BaseModel):
    id: UUIDStr
    label: str
    capacity_kg: Optional[float]
    status: str
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        from_attributes = True
