from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.organization import Organization
from packages.database.models.user import User
from wasteos_api.schemas.admin import OrganizationCreateRequest, OrganizationResponse
from wasteos_api.dependencies import require_permission

router = APIRouter()


@router.get("", response_model=list[OrganizationResponse])
def list_organizations(db: Session = Depends(get_db), admin: User = Depends(require_permission("admin:manage"))):
    return db.query(Organization).order_by(Organization.created_at.desc()).all()


@router.post("", response_model=OrganizationResponse, status_code=201)
def create_organization(payload: OrganizationCreateRequest, db: Session = Depends(get_db), admin: User = Depends(require_permission("admin:manage"))):
    org = Organization(**payload.model_dump())
    db.add(org)
    db.commit()
    db.refresh(org)
    return org
