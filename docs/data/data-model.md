# Data Model

Core entities and their tables (see `packages/database/models/`):

User, Organization, Waste, Pickup, Passport, Reward, Listing, Transaction,
Hotspot, Report, Facility, Vehicle, Ward, WasteTypeConfig, AuditLog,
OutboxEvent, IdempotencyKey.

Schema is defined once in the SQLAlchemy models and mirrored in
`db/migrations/versions/0001_initial_schema.py` (Alembic). Run:

```
docker compose exec api alembic -c db/migrations/alembic.ini upgrade head
```

(The API also calls `Base.metadata.create_all` on startup for local dev
convenience — use the real migration in anything resembling production.)
