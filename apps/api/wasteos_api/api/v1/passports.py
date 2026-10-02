import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.passport import Passport
from wasteos_api.schemas.passport import PassportResponse

router = APIRouter()


@router.get("/verify/{qr_token}", response_model=PassportResponse)
def verify_passport(qr_token: str, db: Session = Depends(get_db)):
    """Public verification endpoint — intentionally exposes only lifecycle
    data, never owner PII."""
    passport = db.query(Passport).filter(Passport.qr_token == qr_token).first()
    if not passport:
        raise HTTPException(status_code=404, detail={"error": {"code": "PASSPORT_NOT_FOUND", "message": "Passport not found."}})
    return passport


@router.get("/{waste_id}", response_model=PassportResponse)
def get_passport(waste_id: str, db: Session = Depends(get_db)):
    passport = db.query(Passport).filter(Passport.waste_id == uuid.UUID(waste_id)).first()
    if not passport:
        raise HTTPException(status_code=404, detail={"error": {"code": "PASSPORT_NOT_FOUND", "message": "Passport not found."}})
    return passport
