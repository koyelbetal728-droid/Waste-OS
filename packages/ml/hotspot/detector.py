from packages.ml.hotspot.clustering import detect_hotspots


def run_detection(points: list[dict], radius_km: float = 0.5, min_reports: int = 3) -> list[dict]:
    return detect_hotspots(points, radius_km=radius_km, min_reports=min_reports)
