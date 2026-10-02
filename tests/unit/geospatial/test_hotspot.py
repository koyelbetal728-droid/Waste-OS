from packages.geospatial.hotspot import detect_hotspots


def test_no_points_returns_no_hotspots():
    assert detect_hotspots([]) == []


def test_scattered_points_below_threshold_returns_no_hotspots():
    points = [{"latitude": 22.5, "longitude": 88.3}, {"latitude": 23.5, "longitude": 89.3}]
    assert detect_hotspots(points, min_reports=3) == []


def test_tight_cluster_above_threshold_is_detected():
    points = [
        {"latitude": 22.5726, "longitude": 88.3639},
        {"latitude": 22.5730, "longitude": 88.3642},
        {"latitude": 22.5728, "longitude": 88.3640},
        {"latitude": 22.5725, "longitude": 88.3638},
    ]
    hotspots = detect_hotspots(points, radius_km=0.5, min_reports=3)
    assert len(hotspots) == 1
    assert hotspots[0]["report_count"] == 4
