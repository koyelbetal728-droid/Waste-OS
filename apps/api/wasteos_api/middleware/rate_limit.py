"""In-memory sliding-window rate limiter (per-process). Good enough for a
a single-instance local deployment; swap the counter store for Redis
(INCR + EXPIRE) before running multiple API replicas."""
import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from packages.core.config import settings

_hits: dict[str, list[float]] = defaultdict(list)

RATE_LIMITED_PREFIXES = {
    "/api/v1/auth/login": (10, 60),
    "/api/v1/auth/register": (5, 60),
    "/api/v1/scanning": (20, 60),
}

_ALLOWED_ORIGINS = {o.strip() for o in settings.cors_origins.split(",") if o.strip()}


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Never rate-limit CORS preflight (OPTIONS); browsers fire one before
        # every real request, which would otherwise exhaust the auth budgets.
        if request.method == "OPTIONS":
            return await call_next(request)
        path = request.url.path
        for prefix, (limit, window_seconds) in RATE_LIMITED_PREFIXES.items():
            if path.startswith(prefix):
                key = f"{prefix}:{request.client.host if request.client else 'unknown'}"
                now = time.time()
                _hits[key] = [t for t in _hits[key] if now - t < window_seconds]
                if len(_hits[key]) >= limit:
                    headers = {}
                    origin = request.headers.get("origin", "")
                    if origin and origin in _ALLOWED_ORIGINS:
                        headers["access-control-allow-origin"] = origin
                        headers["access-control-allow-credentials"] = "true"
                    return JSONResponse(
                        status_code=429,
                        headers=headers,
                        content={"error": {"code": "RATE_LIMITED", "message": "Too many requests, slow down."}},
                    )
                _hits[key].append(now)
                break
        return await call_next(request)
