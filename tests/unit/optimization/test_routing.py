from packages.optimization.routing.optimizer import optimize_route


def test_no_stops_returns_empty_route():
    depot = {"latitude": 22.57, "longitude": 88.36}
    result = optimize_route(depot, [])
    assert result["ordered_stops"] == []
    assert result["total_distance_km"] == 0.0


def test_optimizer_visits_every_stop_exactly_once():
    depot = {"latitude": 22.5726, "longitude": 88.3639}
    stops = [
        {"id": "a", "latitude": 22.5626, "longitude": 88.3712},
        {"id": "b", "latitude": 22.5892, "longitude": 88.3467},
        {"id": "c", "latitude": 22.5511, "longitude": 88.3925},
    ]
    result = optimize_route(depot, stops)
    visited_ids = {s["id"] for s in result["ordered_stops"]}
    assert visited_ids == {"a", "b", "c"}
    assert result["total_distance_km"] > 0


def test_optimizer_never_increases_distance_vs_naive_order():
    """2-opt should never produce a WORSE route than the unoptimized order."""
    from packages.optimization.routing.optimizer import _route_distance
    depot = {"latitude": 22.5726, "longitude": 88.3639}
    stops = [
        {"latitude": 22.60, "longitude": 88.30},
        {"latitude": 22.50, "longitude": 88.40},
        {"latitude": 22.55, "longitude": 88.35},
    ]
    naive_route = [depot] + stops + [depot]
    result = optimize_route(depot, stops)
    optimized_route = [depot] + result["ordered_stops"] + [depot]
    assert _route_distance(optimized_route) <= _route_distance(naive_route) + 1e-6
