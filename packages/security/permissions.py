"""Simple RBAC: which roles may act on which resource types.
Extend as new domain endpoints are added — never rely on the frontend alone."""
from packages.core.enums import UserRole

ROLE_PERMISSIONS = {
    UserRole.citizen: {"waste:create", "waste:read_own", "pickup:create", "pickup:read_own"},
    UserRole.collector: {"pickup:read_assigned", "pickup:update_status"},
    UserRole.recycler: {"marketplace:read", "marketplace:purchase", "facility:create"},
    UserRole.business: {"waste:create", "waste:read_own", "pickup:create"},
    UserRole.municipality: {"analytics:read", "hotspots:read", "municipality:read", "facility:create"},
    UserRole.admin: {"*"},
}


def has_permission(role: UserRole, permission: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, set())
    return "*" in perms or permission in perms
