import uuid
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.user import User
from packages.security.jwt import decode_access_token
from packages.security.permissions import has_permission
from packages.core.enums import UserRole


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail={"error": {"code": "AUTH_MISSING_TOKEN", "message": "Missing bearer token"}})
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail={"error": {"code": "AUTH_INVALID_TOKEN", "message": "Invalid or expired token"}})
    user = db.query(User).filter(User.id == uuid.UUID(payload["sub"])).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail={"error": {"code": "AUTH_INVALID_TOKEN", "message": "User not found or inactive"}})
    return user


def require_permission(permission: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if not has_permission(UserRole(user.role), permission):
            raise HTTPException(status_code=403, detail={"error": {"code": "AUTH_FORBIDDEN", "message": "Insufficient permissions"}})
        return user
    return checker
