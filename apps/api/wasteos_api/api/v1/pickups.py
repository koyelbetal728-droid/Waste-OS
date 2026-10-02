import uuid
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.pickup import Pickup
from packages.database.models.user import User
from packages.core.enums import PickupStatus
from packages.collection.status import transition_pickup
from packages.core.exceptions import InvalidStateTransitionError
from packages.events.outbox import publish_event
from packages.idempotency.service import get_cached_response, store_response
from wasteos_api.schemas.pickup import PickupCreateRequest, PickupResponse
from wasteos_api.dependencies import get_current_user, require_permission

router = APIRouter()


@router.post("", response_model=PickupResponse, status_code=201)
def create_pickup(
    payload: PickupCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if idempotency_key:
        cached = get_cached_response(db, idempotency_key)
        if cached:
            return cached

    pickup = Pickup(
        citizen_id=user.id,
        waste_id=uuid.UUID(payload.waste_id) if payload.waste_id else None,
        latitude=payload.latitude,
        longitude=payload.longitude,
        preferred_time=payload.preferred_time,
        idempotency_key=idempotency_key,
    )
    db.add(pickup)
    db.flush()
    publish_event(db, "PickupRequested", {"pickup_id": str(pickup.id), "citizen_id": str(user.id)})

    response = PickupResponse.model_validate(pickup).model_dump()
    if idempotency_key:
        store_response(db, idempotency_key, "/pickups", response)
    db.commit()
    return response


@router.get("/my-route-stops")
def my_route_stops(db: Session = Depends(get_db), user: User = Depends(require_permission("pickup:read_assigned"))):
    """Real assigned/accepted pickups with coordinates for this collector —
    never a sample stop list. Returns an empty array if nothing is
    assigned yet; the frontend must show that honestly, not substitute
    fake stops."""
    pickups = (
        db.query(Pickup)
        .filter(Pickup.collector_id == user.id, Pickup.status.in_([PickupStatus.assigned, PickupStatus.accepted]))
        .filter(Pickup.latitude.isnot(None), Pickup.longitude.isnot(None))
        .all()
    )
    return [{"id": str(p.id), "latitude": p.latitude, "longitude": p.longitude} for p in pickups]


@router.get("", response_model=list[PickupResponse])
def list_pickups(db: Session = Depends(get_db), user: User = Depends(get_current_user), mine: bool = True):
    """Citizens see their own requests; collectors see open + their own
    accepted jobs (real query, not a placeholder)."""
    if user.role.value == "collector":
        q = db.query(Pickup).filter(
            (Pickup.status == PickupStatus.requested) | (Pickup.collector_id == user.id)
        )
    else:
        q = db.query(Pickup).filter(Pickup.citizen_id == user.id)
    return q.order_by(Pickup.created_at.desc()).all()


@router.get("/{pickup_id}", response_model=PickupResponse)
def get_pickup(pickup_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    pickup = db.query(Pickup).filter(Pickup.id == uuid.UUID(pickup_id)).first()
    return pickup


@router.patch("/{pickup_id}/status", response_model=PickupResponse)
def update_pickup_status(
    pickup_id: str,
    status: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("pickup:update_status")),
):
    """Collector-only. Uses the real state machine in
    packages/collection/status.py — an invalid jump (e.g. requested ->
    collected) is rejected, not silently applied."""
    pickup = db.query(Pickup).filter(Pickup.id == uuid.UUID(pickup_id)).first()
    if not pickup:
        raise HTTPException(status_code=404, detail={"error": {"code": "PICKUP_NOT_FOUND", "message": "Pickup not found."}})
    try:
        new_status = transition_pickup(pickup.status, PickupStatus(status))
    except (InvalidStateTransitionError, ValueError) as e:
        raise HTTPException(status_code=409, detail={"error": {"code": "PICKUP_INVALID_STATE", "message": str(e)}})
    pickup.status = new_status
    if new_status == PickupStatus.accepted:
        pickup.collector_id = user.id
    db.flush()
    publish_event(db, "PickupStatusChanged", {"pickup_id": str(pickup.id), "status": new_status.value})

    if new_status == PickupStatus.verified:
        from packages.database.models.reward import Reward
        from packages.rewards.rules import points_for
        from packages.notifications.service import notify
        citizen = db.query(User).filter(User.id == pickup.citizen_id).first()
        points = points_for("pickup_verified")
        db.add(Reward(user_id=pickup.citizen_id, points=points, reason="pickup_verified", reference_id=pickup.id))
        publish_event(db, "RewardEarned", {"user_id": str(pickup.citizen_id), "points": points, "reason": "pickup_verified"})
        if citizen:
            notify(db, citizen, "reward_earned", points=points, reason="a verified pickup")

    db.commit()
    db.refresh(pickup)
    return pickup
