# ADR 008: Idempotency keys

**Decision:** Mutating endpoints that create a resource (pickups, marketplace
transactions) accept an `Idempotency-Key` header; a retried request with the
same key returns the original response instead of creating a duplicate.
