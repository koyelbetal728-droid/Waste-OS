# ADR 006: Transactional outbox

**Decision:** Business state changes and their corresponding event write
to the same DB transaction (packages/events/outbox.py), rather than
publishing to a message broker directly from request handlers.
**Why:** Guarantees the event is never lost even if the broker is
temporarily unreachable — a worker/scheduler job flips `published=True`
once it's actually dispatched.
