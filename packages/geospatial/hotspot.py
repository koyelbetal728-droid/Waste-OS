"""Lightweight density-based hotspot clustering (pure-Python, no sklearn
dependency required for the scaffold). Groups nearby reports within
`radius_km` and flags clusters at/above `min_reports` as hotspots.
Swap for DBSCAN/HDBSCAN + PostGIS once packages/ml/hotspot is trained."""
from packages.marketplace.matching import haversine_km


def detect_hotspots(points: list[dict], radius_km: float = 0.5, min_reports: int = 3) -> list[dict]:
    """`points`: [{latitude, longitude}]. Returns cluster centers with severity."""
    visited = [False] * len(points)
    hotspots = []
    for i, p in enumerate(points):
        if visited[i]:
            continue
        cluster = [p]
        visited[i] = True
        for j, q in enumerate(points):
            if visited[j]:
                continue
            if haversine_km(p["latitude"], p["longitude"], q["latitude"], q["longitude"]) <= radius_km:
                cluster.append(q)
                visited[j] = True
        if len(cluster) >= min_reports:
            avg_lat = sum(c["latitude"] for c in cluster) / len(cluster)
            avg_lon = sum(c["longitude"] for c in cluster) / len(cluster)
            severity = "high" if len(cluster) >= 8 else "medium" if len(cluster) >= 5 else "low"
            hotspots.append({
                "latitude": avg_lat, "longitude": avg_lon,
                "report_count": len(cluster), "severity": severity,
            })
    return hotspots
