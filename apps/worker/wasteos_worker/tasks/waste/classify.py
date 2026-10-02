import uuid
from wasteos_worker.celery_app import celery_app
from packages.database.session import SessionLocal
from packages.database.models.waste import Waste
from packages.database.models.passport import Passport
from packages.core.enums import ScanStatus, WasteLifecycleStage
from packages.ai.vision.classifier import get_classifier
from packages.waste.recyclability import determine_recyclability_db
from packages.waste.hazard import screen_hazard
from packages.storage.storage import read_file
from datetime import datetime


@celery_app.task(name="waste.classify_waste_image")
def classify_waste_image(waste_id: str, image_path: str):
    """AI classification pipeline: read from shared storage -> model ->
    domain rules (recyclability/hazard) -> persisted result -> passport
    event. Runs off the request/response cycle so heavy inference never
    blocks the API."""
    db = SessionLocal()
    try:
        waste = db.query(Waste).filter(Waste.id == uuid.UUID(waste_id)).first()
        if not waste:
            return
        waste.scan_status = ScanStatus.processing
        db.commit()

        image_bytes = read_file(image_path)
        classifier = get_classifier()
        result = classifier.predict(image_bytes)

        waste.category = result.category
        waste.material = result.material
        waste.confidence = result.confidence
        waste.contamination_level = result.contamination_level
        waste.model_name = result.model_name
        waste.model_version = result.model_version
        waste.hazard_level = screen_hazard(result.category, result.confidence)
        waste.recyclability = determine_recyclability_db(
            db, result.material, result.contamination_level, result.confidence
        )
        waste.lifecycle_stage = WasteLifecycleStage.identified
        waste.scan_status = ScanStatus.completed

        # Simple, clearly-estimated (not guaranteed) price range placeholder.
        if waste.recyclability.value == "recyclable":
            waste.estimated_value_min = 5.0
            waste.estimated_value_max = 15.0

        passport = db.query(Passport).filter(Passport.waste_id == waste.id).first()
        if not passport:
            passport = Passport(waste_id=waste.id, events=[])
            db.add(passport)
        events = list(passport.events or [])
        events.append({
            "stage": "identified",
            "timestamp": datetime.utcnow().isoformat(),
            "actor": "ai-classifier",
            "metadata": {"model": result.model_name, "version": result.model_version},
        })
        passport.events = events

        db.commit()
    except Exception:
        waste = db.query(Waste).filter(Waste.id == uuid.UUID(waste_id)).first()
        if waste:
            waste.scan_status = ScanStatus.failed
            db.commit()
        raise
    finally:
        db.close()
