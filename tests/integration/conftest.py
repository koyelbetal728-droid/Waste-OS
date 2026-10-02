"""Integration tests need a real reachable PostgreSQL (they exercise the
actual SQLAlchemy models, including Postgres-specific UUID/JSON columns —
they intentionally do NOT run against SQLite). Point DATABASE_URL at a
disposable test database before running these:

    docker compose exec api pytest tests/integration -v

Tests are skipped (not failed) if the DB isn't reachable, so `pytest
tests/unit tests/integration` never breaks in an environment without
Postgres."""
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from packages.core.config import settings
from packages.database.base import Base
from packages.database.models import *  # noqa: F401,F403


def _db_reachable() -> bool:
    try:
        engine = create_engine(settings.database_url, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


requires_db = pytest.mark.skipif(not _db_reachable(), reason="No reachable PostgreSQL — set DATABASE_URL")


@pytest.fixture()
def db_session():
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
