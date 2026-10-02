from celery import Celery
from packages.core.config import settings

celery_app = Celery("wasteos", broker=settings.redis_url, backend=settings.redis_url)
celery_app.autodiscover_tasks(["wasteos_worker.tasks.waste", "wasteos_worker.tasks.events"])
