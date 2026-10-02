import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.waste import Waste
from packages.database.models.user import User
from wasteos_api.schemas.waste import WasteCreateRequest, WasteResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=WasteResponse, status_code=201)
def create_waste(payload: WasteCreateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    waste = Waste(owner_id=user.id, **payload.model_dump())
    db.add(waste)
    db.commit()
    db.refresh(waste)
    return waste


@router.get("", response_model=list[WasteResponse])
def list_my_waste(db: Session = Depends(get_db), user: User = Depends(get_current_user), page: int = 1, page_size: int = 20):
    page_size = min(page_size, 100)
    q = db.query(Waste).filter(Waste.owner_id == user.id).order_by(Waste.created_at.desc())
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/sustainability/summary")
def sustainability_summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Real aggregation over the caller's own waste rows — see
    packages/sustainability/impact.py. Powers the business dashboard's
    Sustainability Report page."""
    from packages.sustainability.impact import summarize
    rows = db.query(Waste).filter(Waste.owner_id == user.id).all()
    return summarize(rows)


@router.get("/{waste_id}", response_model=WasteResponse)
def get_waste(waste_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    waste = db.query(Waste).filter(Waste.id == uuid.UUID(waste_id)).first()
    if not waste:
        raise HTTPException(status_code=404, detail={"error": {"code": "WASTE_NOT_FOUND", "message": "Waste record was not found."}})
    if waste.owner_id != user.id and user.role.value != "admin":
        raise HTTPException(status_code=403, detail={"error": {"code": "AUTH_FORBIDDEN", "message": "Not your waste record."}})
    return waste
