"""OPT-IN ONLY — never runs automatically, never imported by the app.
Creates one local-development account per role so you can log in and test
each dashboard without registering manually every time. Not loaded by
docker compose, not seeded on startup, not referenced by any UI copy.

    python -m db.seeds.dev_accounts

Delete these accounts (or don't run this at all) before anything you'd
call a real deployment — they're a local dev convenience, not fixtures the
app depends on.
"""
from packages.database.session import SessionLocal
from packages.database.models.user import User
from packages.security.password import hash_password
from packages.core.enums import UserRole

DEV_ACCOUNTS = [
    ("citizen@wasteos.local", "Citizen Dev Account", UserRole.citizen),
    ("collector@wasteos.local", "Collector Dev Account", UserRole.collector),
    ("recycler@wasteos.local", "Recycler Dev Account", UserRole.recycler),
    ("municipality@wasteos.local", "Municipality Dev Account", UserRole.municipality),
    ("admin@wasteos.local", "Admin Dev Account", UserRole.admin),
]

if __name__ == "__main__":
    db = SessionLocal()
    for email, name, role in DEV_ACCOUNTS:
        if db.query(User).filter(User.email == email).first():
            continue
        db.add(User(email=email, full_name=name, role=role, hashed_password=hash_password("changeme123")))
    db.commit()
    print(f"Created {len(DEV_ACCOUNTS)} local dev accounts (password: changeme123). "
          f"These are NOT created automatically — you ran this script yourself.")
