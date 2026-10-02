FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir celery redis sqlalchemy psycopg2-binary pydantic pydantic-settings numpy scikit-learn pillow
COPY apps/worker /app/apps/worker
COPY packages /app/packages
ENV PYTHONPATH=/app
WORKDIR /app/apps/worker
CMD ["celery", "-A", "wasteos_worker.celery_app", "worker", "--loglevel=INFO"]
