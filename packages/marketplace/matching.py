"""Rank candidate recyclers/buyers for a listing.
No hard-coded single recycler — ranks by material match, then distance."""
from math import radians, sin, cos, sqrt, atan2


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def rank_recyclers(listing_lat: float, listing_lon: float, recyclers: list[dict]) -> list[dict]:
    """`recyclers` items: {id, name, accepted_materials, latitude, longitude}."""
    ranked = []
    for r in recyclers:
        distance = haversine_km(listing_lat, listing_lon, r["latitude"], r["longitude"])
        ranked.append({**r, "distance_km": round(distance, 2)})
    return sorted(ranked, key=lambda r: r["distance_km"])
