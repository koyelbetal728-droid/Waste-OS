FROM python:3.11-slim
WORKDIR /app
COPY apps/api/pyproject.toml apps/api/pyproject.toml
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy psycopg2-binary \
    pydantic pydantic-settings python-jose[cryptography] \
    alembic redis celery python-multipart numpy scikit-learn pillow ultralytics
COPY apps/api /app/apps/api
COPY packages /app/packages
COPY models /app/models
ENV PYTHONPATH=/app
WORKDIR /app/apps/api
CMD ["uvicorn", "wasteos_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
