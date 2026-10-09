from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class WasteCreateRequest(BaseModel):
    category: Optional[str] = None
    quantity_kg: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class WasteResponse(BaseModel):
    id: UUIDStr
    category: Optional[str]
    material: Optional[str]
    lifecycle_stage: str
    scan_status: str
    recyclability: str
    confidence: Optional[float]
    estimated_value_min: Optional[float]
    estimated_value_max: Optional[float]

    class Config:
        from_attributes = True
