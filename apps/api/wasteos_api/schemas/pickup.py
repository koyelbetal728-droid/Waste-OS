from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PickupCreateRequest(BaseModel):
    waste_id: Optional[str] = None
    latitude: float
    longitude: float
    preferred_time: Optional[datetime] = None


class PickupResponse(BaseModel):
    id: str
    status: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
