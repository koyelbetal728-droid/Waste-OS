import uuid
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.marketplace import Listing, Transaction, ListingStatus
from packages.database.models.user import User
from packages.marketplace.pricing import estimate_price
from packages.recycling.verification import mark_verified
from packages.events.outbox import publish_event
from packages.idempotency.service import get_cached_response, store_response
from wasteos_api.schemas.marketplace import (
    ListingCreateRequest, ListingResponse, PurchaseRequest, TransactionResponse,
)
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("/listings", response_model=ListingResponse, status_code=201)
def create_listing(payload: ListingCreateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    price_min, price_max = estimate_price(payload.material, payload.quantity_kg, payload.quality)
    listing = Listing(
        seller_id=user.id,
        waste_id=uuid.UUID(payload.waste_id) if payload.waste_id else None,
        material=payload.material,
        quantity_kg=payload.quantity_kg,
        quality=payload.quality,
        contamination_level=payload.contamination_level,
        latitude=payload.latitude,
        longitude=payload.longitude,
        price_min=price_min,
        price_max=price_max,
    )
    db.add(listing)
    db.flush()
    publish_event(db, "ListingCreated", {"listing_id": str(listing.id)})
    db.commit()
    db.refresh(listing)

    from packages.feature_flags.service import is_enabled
    if is_enabled("async_recycler_matching") and listing.latitude is not None:
        try:
            from wasteos_worker.tasks.marketplace.recycler_matching import match_recyclers
            match_recyclers.delay(str(listing.id))
        except Exception:
            pass  # worker not importable from this process context; fine in the real deployment

    return listing


@router.get("/listings", response_model=list[ListingResponse])
def browse_listings(db: Session = Depends(get_db), material: str | None = None, page: int = 1, page_size: int = 20):
    page_size = min(page_size, 100)
    q = db.query(Listing).filter(Listing.status == ListingStatus.active)
    if material:
        q = q.filter(Listing.material == material)
    return q.order_by(Listing.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def purchase_listing(
    payload: PurchaseRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if idempotency_key:
        cached = get_cached_response(db, idempotency_key)
        if cached:
            return cached

    # Lock the listing row to prevent a double-sell race between concurrent buyers.
    listing = (
        db.query(Listing)
        .filter(Listing.id == uuid.UUID(payload.listing_id))
        .with_for_update()
        .first()
    )
    if not listing:
        raise HTTPException(status_code=404, detail={"error": {"code": "LISTING_NOT_FOUND", "message": "Listing not found."}})
    if listing.status != ListingStatus.active:
        raise HTTPException(status_code=409, detail={"error": {"code": "MARKETPLACE_LISTING_UNAVAILABLE", "message": "Listing is no longer available."}})

    # Server computes/validates the final price — never trust a client-supplied value.
    final_price = listing.price_max or listing.price_min or 0.0

    transaction = Transaction(listing_id=listing.id, buyer_id=user.id, final_price=final_price, idempotency_key=idempotency_key)
    listing.status = ListingStatus.sold
    mark_verified(db, listing.id)
    db.add(transaction)
    db.flush()
    publish_event(db, "MaterialPurchased", {"transaction_id": str(transaction.id), "listing_id": str(listing.id)})

    from packages.database.models.reward import Reward
    from packages.rewards.rules import points_for
    from packages.notifications.service import notify
    seller = db.query(User).filter(User.id == listing.seller_id).first()
    points = points_for("waste_recycled")
    db.add(Reward(user_id=listing.seller_id, points=points, reason="waste_recycled", reference_id=listing.id))
    if seller:
        notify(db, seller, "listing_purchased", material=listing.material)

    response = TransactionResponse.model_validate(transaction).model_dump()
    if idempotency_key:
        store_response(db, idempotency_key, "/marketplace/transactions", response)
    db.commit()
    return response
