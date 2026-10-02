"""Real matching task: ranks recycler facilities for a listing by distance
+ material acceptance. Runs async so listing creation doesn't block on it."""
from wasteos_worker.celery_app import celery_app
from packages.database.session import SessionLocal
from packages.database.models.marketplace import Listing
from packages.database.models.facility import Facility, FacilityType
from packages.ml.matching.ranking import rank


@celery_app.task(name="marketplace.match_recyclers")
def match_recyclers(listing_id: str):
    db = SessionLocal()
    try:
        listing = db.query(Listing).filter(Listing.id == listing_id).first()
        if not listing or listing.latitude is None:
            return []
        facilities = db.query(Facility).filter(
            Facility.type == FacilityType.recycler_facility, Facility.operational == True  # noqa: E712
        ).all()
        candidates = [
            {"id": str(f.id), "name": f.name, "latitude": f.latitude, "longitude": f.longitude}
            for f in facilities
            if not f.accepted_materials or listing.material in f.accepted_materials
        ]
        return rank(listing.latitude, listing.longitude, candidates)
    finally:
        db.close()
