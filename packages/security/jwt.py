from datetime import datetime, timedelta
from jose import jwt, JWTError
from packages.core.config import settings


def create_access_token(subject: str, role: str, organization_id: str | None = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "role": role, "organization_id": organization_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as e:
        raise ValueError("Invalid or expired token") from e
