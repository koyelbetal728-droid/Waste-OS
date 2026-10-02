"""Full HTTP-level integration test using FastAPI's TestClient against the
real app (real DB required — see conftest.py)."""
import pytest
from tests.integration.conftest import requires_db, _db_reachable

if _db_reachable():
    from fastapi.testclient import TestClient
    from wasteos_api.main import app
    client = TestClient(app)


@requires_db
def test_register_then_login_returns_token():
    email = "itest-flow@example.com"
    reg = client.post("/api/v1/auth/register", json={
        "email": email, "password": "testpass123", "full_name": "Flow Test", "role": "citizen",
    })
    assert reg.status_code in (201, 409)  # 409 if re-run against a persistent test DB

    login = client.post("/api/v1/auth/login", json={"email": email, "password": "testpass123"})
    assert login.status_code == 200
    assert "access_token" in login.json()


@requires_db
def test_login_with_wrong_password_is_rejected():
    login = client.post("/api/v1/auth/login", json={"email": "nonexistent@example.com", "password": "wrong"})
    assert login.status_code == 401
    assert login.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"
