import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.user import User
from packages.core.enums import UserRole
from packages.core.enums import UserRole
from packages.security.audit import write_audit
from wasteos_api.schemas.admin import AdminUserResponse, AdminUserUpdateRequest
from wasteos_api.dependencies import require_permission

router = APIRouter()


@router.get("", response_model=list[AdminUserResponse])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_permission("admin:manage"))):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.patch("/{user_id}", response_model=AdminUserResponse)
def update_user(user_id: str, payload: AdminUserUpdateRequest, db: Session = Depends(get_db), admin: User = Depends(require_permission("admin:manage"))):
    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail={"error": {"code": "USER_NOT_FOUND", "message": "User not found."}})
    changes = {}
    if payload.is_active is not None:
        changes["is_active"] = payload.is_active
        user.is_active = payload.is_active
    if payload.role is not None:
        changes["role"] = payload.role
        user.role = UserRole(payload.role)
    write_audit(db, admin.id, "user.updated", target=f"user:{user.id}", metadata=changes)
    db.commit()
    db.refresh(user)
    return user
