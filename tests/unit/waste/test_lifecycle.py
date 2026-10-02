import pytest
from packages.waste.lifecycle import transition
from packages.core.enums import WasteLifecycleStage as S
from packages.core.exceptions import InvalidStateTransitionError


def test_valid_transition_created_to_identified():
    assert transition(S.created, S.identified) == S.identified


def test_valid_transition_processing_to_recycled():
    assert transition(S.processing, S.recycled) == S.recycled


def test_invalid_transition_skips_stages():
    with pytest.raises(InvalidStateTransitionError):
        transition(S.created, S.collected)


def test_invalid_transition_backwards():
    with pytest.raises(InvalidStateTransitionError):
        transition(S.processing, S.created)


def test_terminal_stage_has_no_outgoing_transitions():
    with pytest.raises(InvalidStateTransitionError):
        transition(S.recycled, S.reused)
