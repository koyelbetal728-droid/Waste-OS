# ADR 009: Redis distributed locks

**Decision:** Any operation that must not run concurrently across multiple
processes (hotspot detection, scheduled jobs) acquires a real Redis
`SET NX EX` lock (packages/locking/redis_lock.py) rather than relying on
single-instance assumptions.
