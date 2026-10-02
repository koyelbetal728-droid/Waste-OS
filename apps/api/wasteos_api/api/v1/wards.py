from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.ward import Ward
from packages.database.models.user import User
from wasteos_api.schemas.ward import WardCreateRequest, WardResponse
from wasteos_api.dependencies import require_permission

router = APIRouter()


@router.get("", response_model=list[WardResponse])
def list_wards(db: Session = Depends(get_db), user: User = Depends(require_permission("municipality:read"))):
    q = db.query(Ward)
    if user.organization_id:
        q = q.filter(Ward.organization_id == user.organization_id)
    return q.order_by(Ward.created_at.desc()).all()


@router.post("", response_model=WardResponse, status_code=201)
def create_ward(payload: WardCreateRequest, db: Session = Depends(get_db), user: User = Depends(require_permission("municipality:read"))):
    ward = Ward(organization_id=user.organization_id, **payload.model_dump())
    db.add(ward)
    db.commit()
    db.refresh(ward)
    return ward
