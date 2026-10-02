FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir sqlalchemy psycopg2-binary pydantic pydantic-settings redis
COPY apps/scheduler /app/apps/scheduler
COPY packages /app/packages
ENV PYTHONPATH=/app
WORKDIR /app/apps/scheduler
CMD ["python", "-m", "wasteos_scheduler.scheduler"]
