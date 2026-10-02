"""Assigns the nearest available collector to a pickup — real distance
calculation, not a random/round-robin placeholder."""
from packages.marketplace.matching import haversine_km


def assign_nearest_collector(pickup_lat: float, pickup_lon: float, collectors: list[dict]) -> dict | None:
    """`collectors`: [{"id", "latitude", "longitude"}]. Returns the nearest
    one, or None if the list is empty."""
    if not collectors:
        return None
    return min(collectors, key=lambda c: haversine_km(pickup_lat, pickup_lon, c["latitude"], c["longitude"]))
