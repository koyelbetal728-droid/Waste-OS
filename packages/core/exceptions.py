class WasteOSError(Exception):
    """Base application error with a stable machine-readable code."""

    code = "WASTEOS_ERROR"
    status_code = 400

    def __init__(self, message: str, code: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code


class NotFoundError(WasteOSError):
    code = "NOT_FOUND"
    status_code = 404


class ForbiddenError(WasteOSError):
    code = "FORBIDDEN"
    status_code = 403


class ValidationErrorApp(WasteOSError):
    code = "VALIDATION_ERROR"
    status_code = 422


class InvalidStateTransitionError(WasteOSError):
    code = "INVALID_STATE_TRANSITION"
    status_code = 409
