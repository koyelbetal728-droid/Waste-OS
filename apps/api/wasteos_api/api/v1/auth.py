from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.user import User
from packages.security.password import hash_password, verify_password
from packages.security.jwt import create_access_token
from packages.security.audit import write_audit
from wasteos_api.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail={"error": {"code": "AUTH_EMAIL_TAKEN", "message": "Email already registered"}})
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail={"error": {"code": "AUTH_INVALID_CREDENTIALS", "message": "Invalid email or password"}})
    token = create_access_token(str(user.id), user.role.value, str(user.organization_id) if user.organization_id else None)
    write_audit(db, user.id, "login", target=f"user:{user.id}")
    db.commit()
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


@router.delete("/me", status_code=204)
def delete_my_account(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Anonymizes the account (see packages/privacy/deletion.py) rather than
    hard-deleting — keeps foreign-key history (waste, transactions, audit)
    valid while removing personal identifiers."""
    from packages.privacy.deletion import delete_account
    delete_account(db, user)
