import uuid
from typing import Annotated

from pydantic import BaseModel, BeforeValidator


def _coerce_uuid(value):
    """UUID columns serialize as uuid.UUID objects through SQLAlchemy, and
    pydantic v2 does not coerce UUID -> str on response models with
    from_attributes=True (it raises "Input should be a valid string",
    producing a 500 ResponseValidationError). This validator stringifies
    any uuid.UUID before the str type check runs."""
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


# Use for every id / *_id exposed in API responses.
UUIDStr = Annotated[str, BeforeValidator(_coerce_uuid)]


class Pagination(BaseModel):
    page: int = 1
    page_size: int = 20
    total: int = 0
