import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from packages.observability.correlation import set_request_id


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        set_request_id(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
