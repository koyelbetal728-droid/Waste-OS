# Waste Classification

**Pipeline:** upload → storage → Celery → `packages/ai/vision/classifier.get_classifier()` → domain rules (`packages/waste/recyclability.py`, `hazard.py`) → persisted result.

**Current model:** `MockClassifier` (packages/ai/vision/classifier.py) until a real model is trained and promoted. Train one with:

```
docker compose exec api python -m scripts.train_models
```

against images under `data/raw/waste/<category>/*.jpg`. This trains a logistic regression over color-histogram features (`packages/ml/classification/`) — a real, honest baseline, not a claimed CNN. Evaluate with `scripts/evaluate_models.py`; promote via `packages/ml/model_registry/registry.promote_to_production`.

Once promoted, `get_classifier()` automatically switches to `RegistryClassifier` — no code changes needed elsewhere.
