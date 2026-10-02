"""Deterministic pickup status transitions — mirrors packages/waste/lifecycle.py's
pattern so pickups get the same "no invalid transition" guarantee."""
from packages.core.enums import PickupStatus
from packages.core.exceptions import InvalidStateTransitionError

ALLOWED_TRANSITIONS = {
    PickupStatus.requested: {PickupStatus.assigned, PickupStatus.cancelled},
    PickupStatus.assigned: {PickupStatus.accepted, PickupStatus.cancelled},
    PickupStatus.accepted: {PickupStatus.en_route, PickupStatus.cancelled},
    PickupStatus.en_route: {PickupStatus.arrived, PickupStatus.failed},
    PickupStatus.arrived: {PickupStatus.collected, PickupStatus.failed},
    PickupStatus.collected: {PickupStatus.verified},
}


def transition_pickup(current: PickupStatus, target: PickupStatus) -> PickupStatus:
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise InvalidStateTransitionError(f"Cannot transition pickup from '{current}' to '{target}'")
    return target
