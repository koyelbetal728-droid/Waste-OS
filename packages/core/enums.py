import enum


class UserRole(str, enum.Enum):
    citizen = "citizen"
    collector = "collector"
    recycler = "recycler"
    business = "business"
    municipality = "municipality"
    admin = "admin"


class WasteLifecycleStage(str, enum.Enum):
    created = "created"
    identified = "identified"
    collected = "collected"
    sorted = "sorted"
    transported = "transported"
    processing = "processing"
    recycled = "recycled"
    reused = "reused"
    treated = "treated"
    recovered = "recovered"


class PickupStatus(str, enum.Enum):
    requested = "requested"
    assigned = "assigned"
    accepted = "accepted"
    en_route = "en_route"
    arrived = "arrived"
    collected = "collected"
    verified = "verified"
    cancelled = "cancelled"
    failed = "failed"


class ScanStatus(str, enum.Enum):
    queued = "queued"
    processing = "processing"
    detecting = "detecting"
    classifying = "classifying"
    analyzing = "analyzing"
    completed = "completed"
    failed = "failed"


class RecyclabilityStatus(str, enum.Enum):
    recyclable = "recyclable"
    conditionally_recyclable = "conditionally_recyclable"
    not_recyclable = "not_recyclable"
    unknown = "unknown"
