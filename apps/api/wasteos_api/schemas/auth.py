from pydantic import BaseModel, EmailStr
from packages.core.enums import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.citizen


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True
