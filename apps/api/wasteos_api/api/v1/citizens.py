"""Aggregated citizen profile/dashboard endpoint — combines waste, rewards
and open pickups in one call instead of making the frontend fan out to
three endpoints for the dashboard header."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from packages.database.session import get_db
from packages.database.models.waste import Waste
from packages.database.models.reward import Reward
from packages.database.models.pickup import Pickup
from packages.database.models.user import User
from packages.core.enums import RecyclabilityStatus, PickupStatus
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.get("/dashboard")
def citizen_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total_waste = db.query(Waste).filter(Waste.owner_id == user.id).count()
    recycled = db.query(Waste).filter(Waste.owner_id == user.id, Waste.recyclability == RecyclabilityStatus.recyclable).count()
    total_points = db.query(func.coalesce(func.sum(Reward.points), 0)).filter(Reward.user_id == user.id).scalar()
    pending_pickups = db.query(Pickup).filter(Pickup.citizen_id == user.id, Pickup.status.notin_([PickupStatus.collected, PickupStatus.cancelled, PickupStatus.failed])).count()

    return {
        "total_waste": total_waste,
        "recycled": recycled,
        "green_points": total_points,
        "pending_pickups": pending_pickups,
    }
