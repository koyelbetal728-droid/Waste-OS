from packages.collection.assignment import assign_nearest_collector


def test_empty_collector_list_returns_none():
    assert assign_nearest_collector(22.5, 88.3, []) is None


def test_assigns_nearest_of_multiple_collectors():
    collectors = [
        {"id": "far", "latitude": 28.6, "longitude": 77.2},
        {"id": "near", "latitude": 22.51, "longitude": 88.31},
    ]
    result = assign_nearest_collector(22.5726, 88.3639, collectors)
    assert result["id"] == "near"
