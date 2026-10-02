# Incident Runbook (starting point)

1. Check `GET /api/v1/health` — reports Postgres + Redis reachability.
2. Check `GET /api/v1/metrics` for request/error counts.
3. If the classifier is misbehaving: `GET /api/v1/classification/model-status`
   tells you whether it's the mock model or a specific trained version —
   roll back with `packages.ml.model_registry.registry.rollback(name)`.
4. If hotspot detection is stuck: it's lock-guarded (packages/locking) —
   check Redis for a `lock:hotspot_detection` key past its TTL.
