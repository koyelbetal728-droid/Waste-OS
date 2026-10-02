from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.waste_type import WasteTypeConfig
from packages.database.models.user import User
from wasteos_api.schemas.waste_type import WasteTypeCreateRequest, WasteTypeResponse
from wasteos_api.dependencies import require_permission

router = APIRouter()


@router.get("", response_model=list[WasteTypeResponse])
def list_waste_types(db: Session = Depends(get_db)):
    return db.query(WasteTypeConfig).order_by(WasteTypeConfig.name).all()


@router.post("", response_model=WasteTypeResponse, status_code=201)
def create_waste_type(payload: WasteTypeCreateRequest, db: Session = Depends(get_db), user: User = Depends(require_permission("admin:manage"))):
    existing = db.query(WasteTypeConfig).filter(WasteTypeConfig.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail={"error": {"code": "WASTE_TYPE_EXISTS", "message": "Waste type already exists."}})
    wt = WasteTypeConfig(**payload.model_dump())
    db.add(wt)
    db.commit()
    db.refresh(wt)
    return wt
