"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-21
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    op.create_table(
        "organizations",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "users",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False),
        sa.Column("organization_id", pg.UUID(as_uuid=True), sa.ForeignKey("organizations.id"), nullable=True),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("green_points", sa.String, default="0"),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "waste",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("owner_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category", sa.String), sa.Column("material", sa.String), sa.Column("quantity_kg", sa.Float),
        sa.Column("latitude", sa.Float), sa.Column("longitude", sa.Float),
        sa.Column("lifecycle_stage", sa.String), sa.Column("scan_status", sa.String), sa.Column("recyclability", sa.String),
        sa.Column("contamination_level", sa.String), sa.Column("hazard_level", sa.String),
        sa.Column("confidence", sa.Float), sa.Column("model_name", sa.String), sa.Column("model_version", sa.String),
        sa.Column("image_path", sa.String), sa.Column("raw_ai_output", pg.JSON),
        sa.Column("estimated_value_min", sa.Float), sa.Column("estimated_value_max", sa.Float),
        sa.Column("created_at", sa.DateTime), sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "pickups",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("citizen_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("collector_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("waste_id", pg.UUID(as_uuid=True), sa.ForeignKey("waste.id"), nullable=True),
        sa.Column("status", sa.String), sa.Column("latitude", sa.Float), sa.Column("longitude", sa.Float),
        sa.Column("preferred_time", sa.DateTime), sa.Column("idempotency_key", sa.String, unique=True, nullable=True),
        sa.Column("created_at", sa.DateTime), sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "passports",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("waste_id", pg.UUID(as_uuid=True), sa.ForeignKey("waste.id"), nullable=False, unique=True),
        sa.Column("qr_token", sa.String, unique=True),
        sa.Column("events", pg.JSON), sa.Column("created_at", sa.DateTime), sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "rewards",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("points", sa.Integer, nullable=False), sa.Column("reason", sa.String, nullable=False),
        sa.Column("reference_id", pg.UUID(as_uuid=True), nullable=True), sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "listings",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("seller_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("waste_id", pg.UUID(as_uuid=True), sa.ForeignKey("waste.id"), nullable=True),
        sa.Column("material", sa.String, nullable=False), sa.Column("quantity_kg", sa.Float, nullable=False),
        sa.Column("quality", sa.String), sa.Column("contamination_level", sa.String),
        sa.Column("latitude", sa.Float), sa.Column("longitude", sa.Float),
        sa.Column("price_min", sa.Float), sa.Column("price_max", sa.Float),
        sa.Column("status", sa.String), sa.Column("verified", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime), sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "transactions",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("listing_id", pg.UUID(as_uuid=True), sa.ForeignKey("listings.id"), nullable=False),
        sa.Column("buyer_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("final_price", sa.Float, nullable=False), sa.Column("idempotency_key", sa.String, unique=True, nullable=True),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "hotspots",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("latitude", sa.Float, nullable=False), sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("severity", sa.String), sa.Column("report_count", sa.Integer), sa.Column("ward", sa.String),
        sa.Column("detected_at", sa.DateTime),
    )

    op.create_table(
        "reports",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("reporter_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category", sa.String, nullable=False), sa.Column("latitude", sa.Float), sa.Column("longitude", sa.Float),
        sa.Column("status", sa.String), sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "facilities",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", pg.UUID(as_uuid=True), sa.ForeignKey("organizations.id"), nullable=True),
        sa.Column("name", sa.String, nullable=False), sa.Column("type", sa.String, nullable=False),
        sa.Column("accepted_materials", sa.String), sa.Column("capacity_kg", sa.Float),
        sa.Column("latitude", sa.Float, nullable=False), sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("operational", sa.Boolean, default=True), sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "vehicles",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", pg.UUID(as_uuid=True), sa.ForeignKey("organizations.id"), nullable=True),
        sa.Column("label", sa.String, nullable=False), sa.Column("capacity_kg", sa.Float),
        sa.Column("status", sa.String), sa.Column("latitude", sa.Float), sa.Column("longitude", sa.Float),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "wards",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", pg.UUID(as_uuid=True), sa.ForeignKey("organizations.id"), nullable=True),
        sa.Column("name", sa.String, nullable=False), sa.Column("population", sa.String),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "waste_type_configs",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String, unique=True, nullable=False), sa.Column("category", sa.String, nullable=False),
        sa.Column("recyclable_default", sa.Boolean, default=True), sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String, nullable=False), sa.Column("target", sa.String),
        sa.Column("metadata_json", pg.JSON), sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "outbox_events",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String, nullable=False), sa.Column("payload", pg.JSON, nullable=False),
        sa.Column("published", sa.Boolean, default=False), sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "idempotency_keys",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("key", sa.String, unique=True, nullable=False, index=True), sa.Column("endpoint", sa.String, nullable=False),
        sa.Column("response_body", pg.JSON), sa.Column("created_at", sa.DateTime),
    )


def downgrade():
    for table in [
        "idempotency_keys", "outbox_events", "audit_logs", "waste_type_configs", "wards", "vehicles",
        "facilities", "reports", "hotspots", "transactions", "listings", "rewards", "passports",
        "pickups", "waste", "users", "organizations",
    ]:
        op.drop_table(table)
