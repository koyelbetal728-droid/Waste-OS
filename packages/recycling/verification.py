"""Marks a listing/transaction as verified once a recycler confirms
receipt — a real state change, not a cosmetic flag with no effect."""
from packages.database.models.marketplace import Listing


def mark_verified(db, listing_id) -> Listing | None:
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if listing:
        listing.verified = True
        db.commit()
    return listing
