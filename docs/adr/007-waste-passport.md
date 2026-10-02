# ADR 007: Append-only Waste Passport

**Decision:** Passport lifecycle events are appended to a JSON list, never
overwritten in place.
**Why:** A passport is meant to be an auditable chain of custody; rewriting
history would defeat that purpose.
