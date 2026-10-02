from pydantic import BaseModel
from typing import Optional


class AdminUserResponse(BaseModel):
    id: str
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
    id: str
    name: str
    type: str

    class Config:
        from_attributes = True
