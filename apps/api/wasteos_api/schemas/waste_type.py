from pydantic import BaseModel
from .common import UUIDStr


class WasteTypeCreateRequest(BaseModel):
    name: str
    category: str
    recyclable_default: bool = True


class WasteTypeResponse(BaseModel):
    id: UUIDStr
    name: str
    category: str
    recyclable_default: bool

    class Config:
        from_attributes = True
