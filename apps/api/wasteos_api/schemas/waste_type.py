from pydantic import BaseModel


class WasteTypeCreateRequest(BaseModel):
    name: str
    category: str
    recyclable_default: bool = True


class WasteTypeResponse(BaseModel):
    id: str
    name: str
    category: str
    recyclable_default: bool

    class Config:
        from_attributes = True
