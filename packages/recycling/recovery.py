"""Advances a waste item's lifecycle to a terminal recovery stage once a
recycler confirms processing — reuses the same deterministic state machine
as the rest of the app rather than writing the stage directly."""
from packages.waste.lifecycle import transition
from packages.core.enums import WasteLifecycleStage


def mark_recycled(waste) -> WasteLifecycleStage:
    waste.lifecycle_stage = transition(waste.lifecycle_stage, WasteLifecycleStage.recycled)
    return waste.lifecycle_stage
