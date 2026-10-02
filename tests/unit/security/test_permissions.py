from packages.security.permissions import has_permission
from packages.core.enums import UserRole


def test_admin_has_every_permission():
    assert has_permission(UserRole.admin, "anything:at_all") is True


def test_citizen_can_create_waste():
    assert has_permission(UserRole.citizen, "waste:create") is True


def test_citizen_cannot_manage_admin():
    assert has_permission(UserRole.citizen, "admin:manage") is False


def test_collector_can_update_pickup_status():
    assert has_permission(UserRole.collector, "pickup:update_status") is True
