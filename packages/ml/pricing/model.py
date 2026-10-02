"""Locked-architecture location for the pricing model. Delegates to
packages/marketplace/pricing.py (kept there since the API imports it
directly for listing creation)."""
from packages.marketplace.pricing import estimate_price  # noqa: F401
