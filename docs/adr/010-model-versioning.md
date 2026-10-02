# ADR 010: File-based model registry

**Decision:** `packages/ml/model_registry/registry.py` is a simple
JSON-file registry (register/promote/rollback) rather than a full MLOps
platform (MLflow, etc.).
**Why:** Proportionate to this scaffold's model count (2: classifier,
forecaster). Migrate to a real MLOps platform if the model count/team size
grows past what a JSON file can comfortably track.
