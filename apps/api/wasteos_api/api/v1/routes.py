from fastapi import APIRouter, Depends
from packages.optimization.routing.optimizer import optimize_route
from wasteos_api.schemas.routing import RouteOptimizeRequest, RouteOptimizeResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("/optimize", response_model=RouteOptimizeResponse)
def optimize(payload: RouteOptimizeRequest, user=Depends(get_current_user)):
    result = optimize_route(payload.depot.model_dump(), [s.model_dump() for s in payload.stops])
    return result
