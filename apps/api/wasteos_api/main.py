from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from packages.core.config import settings
from packages.core.exceptions import WasteOSError
from packages.database.base import Base
from packages.database.session import engine
from wasteos_api.api.router import api_router
from wasteos_api.middleware.request_id import RequestIDMiddleware
from wasteos_api.middleware.security_headers import SecurityHeadersMiddleware
from wasteos_api.middleware.rate_limit import RateLimitMiddleware
from wasteos_api.middleware.error_handler import wasteos_exception_handler, unhandled_exception_handler

app = FastAPI(title="WasteOS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

app.add_exception_handler(WasteOSError, wasteos_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    # Dev convenience only: create tables if missing. Use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)
