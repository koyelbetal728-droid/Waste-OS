from pydantic import BaseModel


class RewardEntryResponse(BaseModel):
    id: str
    points: int
    reason: str

    class Config:
        from_attributes = True


class RewardBalanceResponse(BaseModel):
    total_points: int
    entries: list[RewardEntryResponse]
