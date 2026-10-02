from pydantic import BaseModel
from typing import Optional


class WardCreateRequest(BaseModel):
    name: str
    population: Optional[str] = None


class WardResponse(BaseModel):
    id: str
    name: str
    population: Optional[str]

    class Config:
        from_attributes = True
