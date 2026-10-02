# ADR 001: Monorepo

**Decision:** Single repo for web/api/worker/scheduler + shared `packages/`.
**Why:** Domain logic (waste rules, pricing, matching) is shared between the
API and the worker; a monorepo lets both import `packages/waste` directly
without publishing an internal package.
