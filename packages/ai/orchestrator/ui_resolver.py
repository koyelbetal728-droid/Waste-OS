"""Resolves a classified intent into a structured UI directive: which
component the frontend should render, and the REAL data to render it with
(queried live from the DB — never fabricated). This is the core of the
generative-UI assistant: the backend decides the *shape* of the response,
the frontend just renders whatever shape it's told.

Response contract (every resolver returns this):
    {"type": "<component-key>", "title": str, "data": {...}}

Frontend component keys: stat_grid, chart_bar, list, form, timeline, text.
"""
from sqlalchemy import func
from packages.database.models.waste import Waste
from packages.database.models.reward import Reward
from packages.database.models.hotspot import Hotspot
from packages.database.models.marketplace import Listing, ListingStatus
from packages.core.enums import RecyclabilityStatus
from packages.ai.rag.retriever import retrieve
from packages.ai.llm.ollama_client import generate
from packages.ai.orchestrator.safety import sanitize_advisory


def resolve_waste_stats(db, user, message) -> dict:
    rows = db.query(Waste).filter(Waste.owner_id == user.id).all()
    total = len(rows)
    recycled = sum(1 for w in rows if w.recyclability == RecyclabilityStatus.recyclable)
    by_category: dict[str, int] = {}
    for w in rows:
        if w.category:
            by_category[w.category] = by_category.get(w.category, 0) + 1

    return {
        "type": "stat_grid",
        "title": "Your waste, at a glance",
        "data": {
            "stats": [
                {"label": "Total scanned", "value": total},
                {"label": "Recyclable", "value": recycled},
                {"label": "Categories", "value": len(by_category)},
            ],
            "follow_up": {"type": "chart_bar", "title": "By category",
                          "data": {"labels": list(by_category.keys()), "values": list(by_category.values()), "unit": "items"}}
            if by_category else None,
        },
    }


def resolve_recycling_rate(db, user, message) -> dict:
    total = db.query(Waste).filter(Waste.owner_id == user.id).count()
    recycled = db.query(Waste).filter(Waste.owner_id == user.id, Waste.recyclability == RecyclabilityStatus.recyclable).count()
    rate = round((recycled / total) * 100, 1) if total else 0.0
    return {
        "type": "stat_grid",
        "title": "Your recycling rate",
        "data": {"stats": [
            {"label": "Recycling rate", "value": rate, "suffix": "%"},
            {"label": "Recycled items", "value": recycled},
            {"label": "Total items", "value": total},
        ]},
    }


def resolve_schedule_pickup(db, user, message) -> dict:
    return {
        "type": "form",
        "title": "Schedule a pickup",
        "data": {
            "submit_endpoint": "/pickups",
            "submit_method": "POST",
            "fields": [
                {"name": "latitude", "label": "Latitude", "type": "number", "geolocation": True},
                {"name": "longitude", "label": "Longitude", "type": "number", "geolocation": True},
            ],
            "submit_label": "Request pickup",
        },
    }


def resolve_forecast(db, user, message) -> dict:
    from sqlalchemy import func, cast, Date
    from packages.ml.forecasting.inference import forecast_daily_waste

    rows = (
        db.query(cast(Waste.created_at, Date).label("day"), func.sum(Waste.quantity_kg).label("total_kg"))
        .filter(Waste.owner_id == user.id, Waste.quantity_kg.isnot(None))
        .group_by("day")
        .order_by("day")
        .all()
    )
    history = [{"date": str(r.day), "quantity_kg": float(r.total_kg)} for r in rows]

    if len(history) < 14:
        return {
            "type": "text",
            "title": "Waste forecast",
            "data": {"message": f"You have {len(history)} day(s) of recorded waste with quantities — "
                                 f"forecasting needs at least 14 days of real history. Log quantities when "
                                 f"you scan waste to build this up."},
        }

    forecast = forecast_daily_waste(history, days_ahead=7)
    return {
        "type": "chart_bar",
        "title": "Your 7-day forecast (from your real recorded history)",
        "data": {"labels": [f["date"][5:] for f in forecast], "values": [f["forecast_kg"] for f in forecast], "unit": "kg"},
    }


def resolve_hotspots(db, user, message) -> dict:
    hotspots = db.query(Hotspot).order_by(Hotspot.detected_at.desc()).limit(10).all()
    if not hotspots:
        return {"type": "text", "title": "Hotspots", "data": {"message": "No hotspots detected yet — run detection from the Municipality → Hotspots page once reports come in."}}
    return {
        "type": "list",
        "title": "Recent hotspots",
        "data": {"items": [
            {"title": f"{h.latitude:.3f}, {h.longitude:.3f}", "subtitle": f"{h.report_count} reports", "badge": h.severity}
            for h in hotspots
        ]},
    }


def resolve_rewards(db, user, message) -> dict:
    total = db.query(func.coalesce(func.sum(Reward.points), 0)).filter(Reward.user_id == user.id).scalar()
    entries = db.query(Reward).filter(Reward.user_id == user.id).order_by(Reward.created_at.desc()).limit(5).all()
    return {
        "type": "stat_grid",
        "title": "Your Green Points",
        "data": {
            "stats": [{"label": "Total points", "value": total}],
            "follow_up": {"type": "list", "title": "Recent activity", "data": {
                "items": [{"title": e.reason.replace("_", " ").title(), "subtitle": f"+{e.points} points", "badge": None} for e in entries]
            }} if entries else None,
        },
    }


def resolve_marketplace(db, user, message) -> dict:
    listings = db.query(Listing).filter(Listing.status == ListingStatus.active).order_by(Listing.created_at.desc()).limit(8).all()
    if not listings:
        return {"type": "text", "title": "Marketplace", "data": {"message": "No active listings right now."}}
    return {
        "type": "list",
        "title": "Active marketplace listings",
        "data": {"items": [
            {"title": l.material, "subtitle": f"{l.quantity_kg} kg · ₹{l.price_min}–₹{l.price_max}", "badge": l.status.value}
            for l in listings
        ]},
    }


def resolve_recyclability_check(db, user, message) -> dict:
    return {
        "type": "text",
        "title": "Recyclability check",
        "data": {"message": "I can check recyclability from a photo — use Scan Waste to upload an image and "
                             "I'll run it through the classifier and the recyclability rules."},
    }


def resolve_unknown(db, user, message) -> dict:
    """Falls back to real RAG retrieval + LLM (with a deterministic
    fallback if Ollama isn't running) — never fabricates a structural
    component for a request that doesn't match a known intent."""
    docs = retrieve(message)
    context = "\n".join(f"- {d['text']}" for d in docs)
    prompt = f"Context:\n{context}\n\nQuestion: {message}\nAnswer using only the context, in one or two sentences."
    answer = generate(prompt)
    if answer is None:
        answer = docs[0]["text"] if docs else (
            "I can help with waste stats, recycling rate, scheduling a pickup, hotspots, "
            "Green Points, or the marketplace — try asking about one of those."
        )
    return {"type": "text", "title": "Assistant", "data": {"message": sanitize_advisory(answer.strip())}}


RESOLVERS = {
    "waste_stats": resolve_waste_stats,
    "recycling_rate": resolve_recycling_rate,
    "schedule_pickup": resolve_schedule_pickup,
    "forecast": resolve_forecast,
    "hotspots": resolve_hotspots,
    "rewards": resolve_rewards,
    "marketplace": resolve_marketplace,
    "recyclability_check": resolve_recyclability_check,
    "unknown": resolve_unknown,
}


def resolve(intent: str, db, user, message: str) -> dict:
    resolver = RESOLVERS.get(intent, resolve_unknown)
    return resolver(db, user, message)
