# ADR 005: Storage abstraction

**Decision:** `packages/storage/storage.py` is a facade over local-disk vs
object-storage backends, selected by `STORAGE_BACKEND` env var.
**Status:** Only the local backend is implemented; object_storage.py raises
clearly rather than silently writing nowhere. See infra/deployment/production.md.
