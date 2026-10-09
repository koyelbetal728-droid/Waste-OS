import wasteos_worker.celery_app as celery_app_module
from packages.ai.vision.pipeline import run_classification

celery_app = celery_app_module.celery_app


@celery_app.task(name="waste.classify_waste_image")
def classify_waste_image(waste_id: str, image_path: str):
    """AI classification pipeline: read from shared storage -> model ->
    domain rules (recyclability/hazard) -> persisted result -> passport
    event. Runs off the request/response cycle so heavy inference never
    blocks the API.

    The actual logic lives in packages/ai/vision/pipeline.py so the API can
    run the exact same pipeline inline when the worker queue is unavailable."""
    return run_classification(waste_id, image_path)
