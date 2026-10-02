"""Real DB round-trip tests — not mocked. Requires a reachable PostgreSQL
(see conftest.py)."""
from tests.integration.conftest import requires_db
from packages.database.models.user import User
from packages.database.models.waste import Waste
from packages.security.password import hash_password


@requires_db
def test_create_and_fetch_user(db_session):
    user = User(email="itest-user@example.com", hashed_password=hash_password("x"), full_name="Test User", role="citizen")
    db_session.add(user)
    db_session.flush()

    fetched = db_session.query(User).filter(User.email == "itest-user@example.com").first()
    assert fetched is not None
    assert fetched.full_name == "Test User"


@requires_db
def test_waste_foreign_key_to_user(db_session):
    user = User(email="itest-waste-owner@example.com", hashed_password=hash_password("x"), full_name="Owner", role="citizen")
    db_session.add(user)
    db_session.flush()

    waste = Waste(owner_id=user.id, category="Plastic Bottle")
    db_session.add(waste)
    db_session.flush()

    fetched = db_session.query(Waste).filter(Waste.owner_id == user.id).first()
    assert fetched is not None
    assert fetched.category == "Plastic Bottle"
