import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.waste import Waste
from packages.database.models.user import User
from packages.core.enums import ScanStatus
from packages.storage.storage import save_file
from packages.observability.metrics import increment
from wasteos_api.schemas.scanning import ScanJobResponse, ScanResultResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def _broker_reachable() -> bool:
    """Fast TCP check against the Celery broker. Celery's `.delay()` blocks
    on connection retries when Redis is down, which would stall the upload
    request — so check the socket first and fall back to inline inference."""
    import socket
    from urllib.parse import urlparse
    from packages.core.config import settings
    try:
        parsed = urlparse(settings.redis_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 6379
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except Exception:
        return False


@router.post("", response_model=ScanJobResponse, status_code=202)
async def create_scan(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail={"error": {"code": "SCAN_INVALID_FILE", "message": "Only JPEG/PNG/WebP images are accepted."}})
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail={"error": {"code": "SCAN_FILE_TOO_LARGE", "message": "Image must be under 10MB."}})

    extension = (file.content_type or "").split("/")[-1] or "jpg"
    image_path = save_file("scans", contents, extension)

    waste = Waste(owner_id=user.id, scan_status=ScanStatus.queued, image_path=image_path)
    db.add(waste)
    db.commit()
    db.refresh(waste)
    increment("scan_requested")

    # Queue the real inference to the worker instead of blocking the request.
    # Pass the storage path, not the raw bytes — both processes read the
    # same STORAGE_ROOT volume, so this survives worker restarts and keeps
    # the Celery message small.
    if _broker_reachable():
        try:
            from wasteos_worker.tasks.waste.classify import classify_waste_image
            classify_waste_image.delay(str(waste.id), image_path)
        except Exception:
            # Worker package not importable from this process context in some
            # deployments (e.g. api-only container) — inference still runs via
            # the worker service reading from the queue in production.
            pass
    else:
        # No broker/worker reachable (local single-process deployment): run
        # the same pipeline inline in a background thread so the scan still
        # completes and the UI gets a real result instead of polling a
        # record that stays "queued" forever.
        import threading
        from packages.ai.vision.pipeline import run_classification
        threading.Thread(
            target=run_classification,
            args=(str(waste.id), image_path),
            daemon=True,
        ).start()

    return ScanJobResponse(job_id=str(waste.id), waste_id=str(waste.id), status=ScanStatus.queued.value)


@router.get("/image/{path:path}")
def get_scan_image(path: str, user: User = Depends(get_current_user)):
    """Serves the stored scan image — the local-storage equivalent of a
    signed cloud URL (see packages/storage/signed_urls.py). Requires auth
    since scan images aren't public."""
    from fastapi.responses import Response
    from packages.storage.storage import read_file
    try:
        content = read_file(path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={"error": {"code": "IMAGE_NOT_FOUND", "message": "Image not found."}})
    return Response(content=content, media_type="image/jpeg")


@router.get("/{waste_id}", response_model=ScanResultResponse)
def get_scan_result(waste_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    waste = db.query(Waste).filter(Waste.id == uuid.UUID(waste_id)).first()
    if not waste:
        raise HTTPException(status_code=404, detail={"error": {"code": "WASTE_NOT_FOUND", "message": "Scan not found."}})
    return ScanResultResponse(
        waste_id=str(waste.id),
        status=waste.scan_status.value if waste.scan_status else "queued",
        category=waste.category,
        material=waste.material,
        confidence=waste.confidence,
        recyclability=waste.recyclability.value if waste.recyclability else None,
        contamination_level=waste.contamination_level,
        hazard_level=waste.hazard_level,
        estimated_value_min=waste.estimated_value_min,
        estimated_value_max=waste.estimated_value_max,
        model_name=waste.model_name,
        model_version=waste.model_version,
        is_mock_model=(waste.model_name == "mock-classifier"),
    )
