"""Recyclability decision engine — combines the AI prediction with deterministic
local rules. The AI model never gets the final word by itself.

`RECYCLABLE_MATERIALS` is the built-in default set. An admin can extend/override
it via the `waste_type_configs` table (see packages/database/models/waste_type.py,
`/api/v1/waste-types`); `determine_recyclability_db` checks that table first."""
from packages.core.enums import RecyclabilityStatus

RECYCLABLE_MATERIALS = {"PET", "HDPE", "Aluminium", "Glass", "Cardboard", "Paper"}
CONTAMINATION_BLOCKS_RECYCLING = {"high"}


def determine_recyclability(material: str | None, contamination_level: str | None,
                             confidence: float | None) -> RecyclabilityStatus:
    if not material or confidence is None or confidence < 0.5:
        return RecyclabilityStatus.unknown
    if contamination_level in CONTAMINATION_BLOCKS_RECYCLING:
        return RecyclabilityStatus.not_recyclable
    if material in RECYCLABLE_MATERIALS:
        if contamination_level == "medium":
            return RecyclabilityStatus.conditionally_recyclable
        return RecyclabilityStatus.recyclable
    return RecyclabilityStatus.not_recyclable


def determine_recyclability_db(db, material: str | None, contamination_level: str | None,
                                confidence: float | None) -> RecyclabilityStatus:
    """Same logic, but checks the admin-configurable waste_type_configs table
    first (falls back to the built-in default set if no config exists)."""
    from packages.database.models.waste_type import WasteTypeConfig

    if not material or confidence is None or confidence < 0.5:
        return RecyclabilityStatus.unknown
    if contamination_level in CONTAMINATION_BLOCKS_RECYCLING:
        return RecyclabilityStatus.not_recyclable

    config = db.query(WasteTypeConfig).filter(WasteTypeConfig.name == material).first()
    is_recyclable = config.recyclable_default if config else (material in RECYCLABLE_MATERIALS)

    if is_recyclable:
        if contamination_level == "medium":
            return RecyclabilityStatus.conditionally_recyclable
        return RecyclabilityStatus.recyclable
    return RecyclabilityStatus.not_recyclable
