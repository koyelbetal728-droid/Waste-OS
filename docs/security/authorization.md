# Authorization (RBAC)

Roles: citizen, collector, recycler, business, municipality, admin (`packages/core/enums.UserRole`).

Permission strings live in `packages/security/permissions.ROLE_PERMISSIONS`. Every mutating endpoint uses `require_permission(...)` (see `wasteos_api/dependencies.py`) — never relies on the frontend hiding a button.

Admin has wildcard `*`. Extend the permission map when adding a new endpoint; don't invent ad-hoc role checks in route handlers.
