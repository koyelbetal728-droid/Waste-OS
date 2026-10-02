from fastapi import Request
from fastapi.responses import JSONResponse
from packages.core.exceptions import WasteOSError


async def wasteos_exception_handler(request: Request, exc: WasteOSError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "request_id": request_id}},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "request_id": request_id}},
    )
