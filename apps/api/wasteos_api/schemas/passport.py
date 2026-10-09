from pydantic import BaseModel
from typing import Any
from .common import UUIDStr


class PassportResponse(BaseModel):
    id: UUIDStr
    waste_id: UUIDStr
    qr_token: str
    events: list[Any]

    class Config:
        from_attributes = True
