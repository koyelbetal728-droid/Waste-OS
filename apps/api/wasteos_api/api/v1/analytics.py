"""Platform-wide analytics (distinct from /municipality/analytics, which is
organization-scoped). Aggregates are computed live from real rows — no
cached/fabricated numbers."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from packages.database.session import get_db
from packages.database.models.waste import Waste
from packages.database.models.marketplace import Transaction
from packages.core.enums import RecyclabilityStatus

router = APIRouter()


@router.get("")
def platform_analytics(db: Session = Depends(get_db)):
    total_waste = db.query(Waste).count()
    recycled = db.query(Waste).filter(Waste.recyclability == RecyclabilityStatus.recyclable).count()

    by_category = dict(
        db.query(Waste.category, func.count(Waste.id))
        .filter(Waste.category.isnot(None))
        .group_by(Waste.category)
        .all()
    )

    total_transactions = db.query(Transaction).count()
    total_transaction_value = db.query(func.coalesce(func.sum(Transaction.final_price), 0)).scalar()

    return {
        "total_waste_records": total_waste,
        "recycled_count": recycled,
        "recycling_rate": round((recycled / total_waste) * 100, 1) if total_waste else 0.0,
        "by_category": by_category,
        "marketplace_transactions": total_transactions,
        "marketplace_total_value": float(total_transaction_value),
    }
