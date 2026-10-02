Structured JSON logs are written to stdout by every service (see
packages/observability/logging.py). No log aggregation backend (ELK/Loki)
is wired up in this scaffold — `docker compose logs -f <service>` for local
dev; pipe stdout to your aggregator of choice in production.
