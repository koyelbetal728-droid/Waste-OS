from pydantic import BaseModel
from .common import UUIDStr


class RewardEntryResponse(BaseModel):
    id: UUIDStr
    points: int
    reason: str

    class Config:
        from_attributes = True


class RewardBalanceResponse(BaseModel):
    total_points: int
    entries: list[RewardEntryResponse]
