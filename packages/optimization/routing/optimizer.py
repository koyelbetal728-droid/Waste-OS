"""Deterministic route optimizer for collector stops.
Nearest-neighbor construction + 2-opt improvement — a real, working
heuristic (not ML/LLM-generated). Good enough for tens of stops; swap for
OR-Tools if you need capacity/time-window constraints at scale."""
from packages.marketplace.matching import haversine_km


def _route_distance(route: list[dict]) -> float:
    return sum(
        haversine_km(route[i]["latitude"], route[i]["longitude"], route[i + 1]["latitude"], route[i + 1]["longitude"])
        for i in range(len(route) - 1)
    )


def optimize_route(depot: dict, stops: list[dict]) -> dict:
    """`depot`/`stops`: {"id"?, "latitude", "longitude"}.
    Returns ordered stops (depot -> ... -> depot) and total distance in km."""
    if not stops:
        return {"ordered_stops": [], "total_distance_km": 0.0}

    remaining = stops[:]
    route = [depot]
    current = depot
    while remaining:
        nearest = min(remaining, key=lambda s: haversine_km(current["latitude"], current["longitude"], s["latitude"], s["longitude"]))
        route.append(nearest)
        remaining.remove(nearest)
        current = nearest
    route.append(depot)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if _route_distance(new_route) < _route_distance(route):
                    route = new_route
                    improved = True

    return {"ordered_stops": route[1:-1], "total_distance_km": round(_route_distance(route), 2)}
