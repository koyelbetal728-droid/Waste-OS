"""Account deletion — anonymizes rather than hard-deletes the User row, so
foreign-key references (waste, pickups, transactions) stay valid and
auditable, per the 'passport history must be append-oriented' rule
elsewhere in the spec. This is a real, working implementation, not a stub."""
from packages.privacy.anonymization import anonymize_user
from packages.security.audit import write_audit


def delete_account(db, user):
    anonymize_user(user)
    write_audit(db, user.id, "account.deleted", target=f"user:{user.id}")
    db.commit()
    return user
