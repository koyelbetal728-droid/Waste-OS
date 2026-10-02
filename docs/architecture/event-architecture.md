# Event Architecture

Transactional outbox pattern: a business change and its `OutboxEvent` row commit in the same DB transaction (see `packages/events/outbox.py`). A worker task (`apps/worker/.../process_outbox.py`) marks events published; real consumers (notifications, analytics) subscribe from there.

Events currently emitted: `PickupRequested`, `PickupStatusChanged`, `ListingCreated`, `MaterialPurchased`, `ReportCreated`.
