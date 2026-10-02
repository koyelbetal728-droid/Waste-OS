# Disaster Recovery Plan

- **Database**: rely on your managed Postgres provider's point-in-time
  recovery. No custom backup automation is implemented in this scaffold —
  `scripts/backup_database.py` / `restore_database.py` are referenced by
  the locked architecture but not yet written; add them wrapping `pg_dump`
  / `pg_restore` before relying on this for production.
- **Object storage**: not configured (see infra/deployment/production.md).
- **Model registry**: `models/registry/registry.json` + `models/artifacts/`
  should be backed up alongside the database — losing them means retraining
  from scratch, not losing user data.
