from fastapi import APIRouter, Depends
from packages.special_waste.food.donation import donation_eligibility
from wasteos_api.schemas.special_waste import FoodWasteRequest, FoodWasteResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=FoodWasteResponse)
def check_food_waste(payload: FoodWasteRequest, user=Depends(get_current_user)):
    return donation_eligibility(payload.condition, payload.hours_since_prep)
