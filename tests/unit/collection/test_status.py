import pytest
from packages.collection.status import transition_pickup
from packages.core.enums import PickupStatus as S
from packages.core.exceptions import InvalidStateTransitionError


def test_requested_can_be_assigned():
    assert transition_pickup(S.requested, S.assigned) == S.assigned


def test_requested_can_be_cancelled():
    assert transition_pickup(S.requested, S.cancelled) == S.cancelled


def test_cannot_skip_from_requested_to_collected():
    with pytest.raises(InvalidStateTransitionError):
        transition_pickup(S.requested, S.collected)


def test_collected_can_only_go_to_verified():
    assert transition_pickup(S.collected, S.verified) == S.verified
    with pytest.raises(InvalidStateTransitionError):
        transition_pickup(S.collected, S.en_route)
