from pydantic import BaseModel
from typing import Any


class PassportResponse(BaseModel):
    id: str
    waste_id: str
    qr_token: str
    events: list[Any]

    class Config:
        from_attributes = True
