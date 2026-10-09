from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class WardCreateRequest(BaseModel):
    name: str
    population: Optional[str] = None


class WardResponse(BaseModel):
    id: UUIDStr
    name: str
    population: Optional[str]

    class Config:
        from_attributes = True
