"""Deterministic waste lifecycle state machine.
AI predictions are inputs to this layer, never a replacement for it."""
from packages.core.enums import WasteLifecycleStage
from packages.core.exceptions import InvalidStateTransitionError

ALLOWED_TRANSITIONS = {
    WasteLifecycleStage.created: {WasteLifecycleStage.identified},
    WasteLifecycleStage.identified: {WasteLifecycleStage.collected},
    WasteLifecycleStage.collected: {WasteLifecycleStage.sorted},
    WasteLifecycleStage.sorted: {WasteLifecycleStage.transported},
    WasteLifecycleStage.transported: {WasteLifecycleStage.processing},
    WasteLifecycleStage.processing: {
        WasteLifecycleStage.recycled,
        WasteLifecycleStage.reused,
        WasteLifecycleStage.treated,
        WasteLifecycleStage.recovered,
    },
}


def transition(current: WasteLifecycleStage, target: WasteLifecycleStage) -> WasteLifecycleStage:
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise InvalidStateTransitionError(
            f"Cannot transition waste from '{current}' to '{target}'"
        )
    return target
