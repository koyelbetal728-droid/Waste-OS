from fastapi import APIRouter, Depends
from packages.special_waste.e_waste.classifier import determine_pathway
from wasteos_api.schemas.special_waste import EWasteRequest, EWasteResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=EWasteResponse)
def classify_e_waste(payload: EWasteRequest, user=Depends(get_current_user)):
    return EWasteResponse(condition=payload.condition, pathway=determine_pathway(payload.condition))
