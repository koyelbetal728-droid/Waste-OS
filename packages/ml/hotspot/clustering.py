"""Locked-architecture location for hotspot clustering. Delegates to the
real implementation in packages/geospatial/hotspot.py (kept there since
distance math is shared with recycler matching) — this module is the
documented ML-package entry point per the architecture spec."""
from packages.geospatial.hotspot import detect_hotspots  # noqa: F401
