from packages.marketplace.matching import haversine_km, rank_recyclers


def test_haversine_zero_distance_for_same_point():
    assert haversine_km(22.57, 88.36, 22.57, 88.36) == 0


def test_haversine_known_distance_kolkata_to_delhi_roughly():
    # Kolkata to Delhi is roughly 1300-1500km as the crow flies.
    dist = haversine_km(22.5726, 88.3639, 28.6139, 77.2090)
    assert 1200 < dist < 1600


def test_rank_recyclers_orders_by_distance():
    recyclers = [
        {"id": "far", "latitude": 28.6139, "longitude": 77.2090},
        {"id": "near", "latitude": 22.58, "longitude": 88.37},
    ]
    ranked = rank_recyclers(22.5726, 88.3639, recyclers)
    assert ranked[0]["id"] == "near"
    assert ranked[0]["distance_km"] < ranked[1]["distance_km"]
