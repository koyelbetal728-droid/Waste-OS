import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.facility import Facility
from packages.database.models.user import User
from wasteos_api.schemas.facility import FacilityCreateRequest, FacilityResponse
from wasteos_api.dependencies import require_permission, get_current_user

router = APIRouter()


@router.get("", response_model=list[FacilityResponse])
def list_facilities(db: Session = Depends(get_db), type: str | None = None):
    q = db.query(Facility).filter(Facility.operational == True)  # noqa: E712
    if type:
        q = q.filter(Facility.type == type)
    return q.order_by(Facility.created_at.desc()).all()


@router.post("", response_model=FacilityResponse, status_code=201)
def create_facility(payload: FacilityCreateRequest, db: Session = Depends(get_db), user: User = Depends(require_permission("facility:create"))):
    facility = Facility(organization_id=user.organization_id, **payload.model_dump())
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility


@router.delete("/{facility_id}", status_code=204)
def deactivate_facility(facility_id: str, db: Session = Depends(get_db), user: User = Depends(require_permission("facility:create"))):
    facility = db.query(Facility).filter(Facility.id == uuid.UUID(facility_id)).first()
    if not facility:
        raise HTTPException(status_code=404, detail={"error": {"code": "FACILITY_NOT_FOUND", "message": "Facility not found."}})
    facility.operational = False
    db.commit()
