# WasteOS System Architecture

```
Next.js (apps/web) → FastAPI (apps/api) → Domain packages (packages/*) → PostgreSQL/PostGIS + Redis
                                                    ↓
                                          Celery worker (apps/worker) → AI/ML (packages/ai, packages/ml)
```

## Layers
- **apps/web** — Next.js frontend, one route group per role (citizen, collector, recycler, business, municipality, admin).
- **apps/api** — FastAPI. Routes validate + authorize, then call domain packages. No business logic in route handlers.
- **apps/worker** — Celery tasks for anything that shouldn't block an HTTP request (vision inference, outbox processing).
- **packages/database** — SQLAlchemy models + the one place schema lives (mirrored in db/migrations).
- **packages/<domain>** — waste, marketplace, collection, recycling, sustainability, special_waste: deterministic business rules. AI output is always passed through these before becoming a final recommendation.
- **packages/ai, packages/ml** — vision/LLM/RAG orchestration and the (real, small) trained-model pipeline. See docs/ai/.

## Why this shape
Matches the locked architecture from the original spec: monorepo, FastAPI + PostgreSQL/PostGIS + Redis + Celery + Next.js, no unnecessary microservices/Kafka/Kubernetes.
