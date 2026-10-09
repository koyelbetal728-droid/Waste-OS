"""Waste image classification pipeline - shared by the API and the worker.

Historically this logic lived inside the Celery task (apps/worker/.../classify.py).
That meant it only ran when a Redis broker + worker process were up, so in a
local single-process deployment the scan stayed "queued" forever and the
frontend eventually showed "Scan failed".

The task body now lives here. The worker task calls it directly, and the API
falls back to running it inline (background thread) when the queue is
unavailable, so scanning works with just the API + database running.
"""
import uuid
from packages.database.session import SessionLocal
from packages.database.models.waste import Waste
from packages.database.models.passport import Passport
from packages.core.enums import ScanStatus, WasteLifecycleStage
from packages.ai.vision.classifier import get_classifier
from packages.waste.recyclability import determine_recyclability_db
from packages.waste.hazard import screen_hazard
from packages.storage.storage import read_file
from datetime import datetime


def run_classification(waste_id: str, image_path: str) -> None:
    """Run the vision pipeline for one stored scan image and persist the result.

    Marks the record failed (instead of leaving it queued forever) if any step
    raises, so the UI can surface a real failure instead of timing out.
    """
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
        # Recyclable materials carry a small positive value; organic /
        # contaminated items are worth ~0. We still record a value range
        # whenever the model was reasonably confident (>=0.6) so the UI shows
        # an estimate instead of leaving it blank.
        if waste.recyclability.value == "recyclable":
            waste.estimated_value_min = 5.0
            waste.estimated_value_max = 15.0
        elif result.confidence >= 0.6:
            waste.estimated_value_min = 1.0
            waste.estimated_value_max = 5.0

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
        db.rollback()
        waste = db.query(Waste).filter(Waste.id == uuid.UUID(waste_id)).first()
        if waste:
            waste.scan_status = ScanStatus.failed
            db.commit()
        raise
    finally:
        db.close()
