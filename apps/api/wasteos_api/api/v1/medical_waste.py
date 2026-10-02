from fastapi import APIRouter, Depends
from packages.special_waste.medical.compliance import compliance_status
from wasteos_api.schemas.special_waste import MedicalWasteRequest, MedicalWasteResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=MedicalWasteResponse)
def classify_medical_waste(payload: MedicalWasteRequest, user=Depends(get_current_user)):
    return compliance_status(payload.category)
