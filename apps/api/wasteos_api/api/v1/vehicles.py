from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.vehicle import Vehicle
from packages.database.models.user import User
from wasteos_api.schemas.vehicle import VehicleCreateRequest, VehicleResponse
from wasteos_api.dependencies import require_permission

router = APIRouter()


@router.get("", response_model=list[VehicleResponse])
def list_vehicles(db: Session = Depends(get_db), user: User = Depends(require_permission("municipality:read"))):
    q = db.query(Vehicle)
    if user.organization_id:
        q = q.filter(Vehicle.organization_id == user.organization_id)
    return q.order_by(Vehicle.created_at.desc()).all()


@router.post("", response_model=VehicleResponse, status_code=201)
def create_vehicle(payload: VehicleCreateRequest, db: Session = Depends(get_db), user: User = Depends(require_permission("municipality:read"))):
    vehicle = Vehicle(organization_id=user.organization_id, **payload.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle
