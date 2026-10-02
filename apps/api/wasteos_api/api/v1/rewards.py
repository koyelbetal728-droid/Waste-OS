from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from packages.database.session import get_db
from packages.database.models.reward import Reward
from packages.database.models.user import User
from wasteos_api.schemas.rewards import RewardBalanceResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.get("/balance", response_model=RewardBalanceResponse)
def get_balance(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entries = db.query(Reward).filter(Reward.user_id == user.id).order_by(Reward.created_at.desc()).all()
    total = db.query(func.coalesce(func.sum(Reward.points), 0)).filter(Reward.user_id == user.id).scalar()
    return RewardBalanceResponse(total_points=total, entries=entries)
