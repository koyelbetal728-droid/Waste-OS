"""Real purchase history for the buyer (recycler) side of the marketplace —
was missing; recycler/purchases and the recycler dashboard previously had
no way to show real data here."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.marketplace import Transaction, Listing
from packages.database.models.user import User
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.get("/mine")
def my_purchases(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = (
        db.query(Transaction, Listing)
        .join(Listing, Transaction.listing_id == Listing.id)
        .filter(Transaction.buyer_id == user.id)
        .order_by(Transaction.created_at.desc())
        .all()
    )
    return [
        {"id": str(t.id), "material": l.material, "quantity_kg": l.quantity_kg,
         "final_price": t.final_price, "created_at": t.created_at.isoformat()}
        for t, l in rows
    ]
