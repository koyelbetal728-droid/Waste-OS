# Production

Not provisioned in this scaffold — no cloud account/infrastructure exists
in this environment to provision against. Before going to production:

1. Managed PostgreSQL with PostGIS extension enabled, managed Redis.
2. Real object storage (S3/GCS) — implement packages/storage/object_storage.py
   against your provider; flip STORAGE_BACKEND=object_storage.
3. Secrets manager (see infra/secrets/README.md) instead of .env.
4. TLS termination in front of infra/reverse_proxy/nginx.conf.
5. A real Prometheus + Grafana setup (see infra/monitoring/ notes on what's
   still a placeholder there).
6. Replace the in-memory rate limiter (wasteos_api/middleware/rate_limit.py)
   with a Redis-backed one before running multiple API replicas.
