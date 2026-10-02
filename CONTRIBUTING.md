# Contributing to WasteOS

1. Inspect the existing code before adding a file — search for equivalent
   functionality first (see the "never duplicate" rule the architecture
   was built against).
2. Domain logic goes in `packages/<domain>/`, never directly in FastAPI
   route handlers.
3. New endpoints must use `require_permission(...)` — see
   `docs/security/authorization.md`.
4. Add a real pytest test under `tests/unit/` for any new pure-logic
   function. `make test` runs the suite.
5. Run `ruff check` before pushing (see `.github/workflows/lint.yml`).
6. Never fabricate AI/ML results — if a model isn't trained yet, return a
   clearly labeled placeholder/unavailable state instead (see
   `packages/ai/vision/classifier.py` for the pattern).
