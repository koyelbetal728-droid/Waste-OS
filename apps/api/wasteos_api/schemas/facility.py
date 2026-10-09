from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class FacilityCreateRequest(BaseModel):
    name: str
    type: str  # recycler_facility | collection_point | processing_facility
    accepted_materials: Optional[str] = None
    capacity_kg: Optional[float] = None
    latitude: float
    longitude: float


class FacilityResponse(BaseModel):
    id: UUIDStr
    name: str
    type: str
    accepted_materials: Optional[str]
    capacity_kg: Optional[float]
    latitude: float
    longitude: float
    operational: bool

    class Config:
        from_attributes = True
