from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from packages.core.exceptions import WasteOSError


async def wasteos_exception_handler(request: Request, exc: WasteOSError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "request_id": request_id}},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Flatten FastAPI's default {"detail": ...} into the documented
    {"error": {"code","message"}} contract so every error response (including
    auth 401/409 raised as plain HTTPExceptions) is uniform and easy for the
    frontend to read."""
    detail = exc.detail
    request_id = getattr(request.state, "request_id", None)
    if isinstance(detail, dict) and "error" in detail and isinstance(detail["error"], dict):
        payload = dict(detail["error"])
    elif isinstance(detail, str):
        payload = {"code": "HTTP_ERROR", "message": detail}
    else:
        payload = {"code": "HTTP_ERROR", "message": str(detail)}
    payload["request_id"] = request_id
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": payload},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "request_id": request_id}},
    )
