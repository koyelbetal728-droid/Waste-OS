# ADR 003: Celery for async work

**Decision:** Vision inference, recycler matching, and notification
dispatch run in Celery workers, not inline in FastAPI request handlers.
**Why:** Inference latency is unpredictable; blocking the HTTP request on
it would make the API feel broken under load.
