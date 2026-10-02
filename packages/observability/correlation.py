"""Reads the request-id set by RequestIDMiddleware so any log line can be
tied back to the originating HTTP request."""
import contextvars

request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)


def set_request_id(request_id: str):
    request_id_var.set(request_id)


def get_request_id() -> str | None:
    return request_id_var.get()
