from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class AdminUserResponse(BaseModel):
    id: UUIDStr
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class AdminUserUpdateRequest(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None


class OrganizationCreateRequest(BaseModel):
    name: str
    type: str  # municipality | recycler | business | facility


class OrganizationResponse(BaseModel):
    id: UUIDStr
    name: str
    type: str

    class Config:
        from_attributes = True
