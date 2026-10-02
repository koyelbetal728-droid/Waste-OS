"""Identifies which User fields are PII — single source of truth so
anonymization/deletion/export code doesn't drift from each other."""

PII_FIELDS = {"email", "full_name"}
