"""Short-lived signed URL generation. Local backend has no real URL host,
so this returns an internal API path the frontend can hit instead of
exposing STORAGE_ROOT directly — never serve raw filesystem paths."""


def get_signed_url(relative_path: str, expires_in_seconds: int = 300) -> str:
    # Local dev: route through the API's own file-serving endpoint instead
    # of a real signed cloud URL.
    return f"/api/v1/scanning/image/{relative_path}"
