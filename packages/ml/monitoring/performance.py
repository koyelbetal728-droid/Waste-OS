"""Tracks realized inference latency/error rate — feed this from the
worker task once labeled outcomes are available."""


def summarize_latencies(latencies_ms: list[float]) -> dict:
    if not latencies_ms:
        return {"count": 0}
    sorted_l = sorted(latencies_ms)
    n = len(sorted_l)
    return {
        "count": n,
        "p50_ms": sorted_l[n // 2],
        "p95_ms": sorted_l[int(n * 0.95)] if n > 1 else sorted_l[0],
        "max_ms": sorted_l[-1],
    }
