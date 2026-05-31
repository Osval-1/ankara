"""crop doctor domain models

Revision ID: 0001
Revises:
Create Date: 2026-05-31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE TYPE crop_enum AS ENUM ('cassava','maize','plantain','tomato','cocoa')")
    op.execute(
        "CREATE TYPE cropclass_enum AS ENUM ("
        "'cassava_healthy','cassava_cmd','cassava_cbsd','cassava_pest','cassava_unknown',"
        "'maize_healthy','maize_streak','maize_blight','maize_rust','maize_unknown',"
        "'plantain_healthy','plantain_bbs','plantain_fusarium','plantain_weevil','plantain_unknown',"
        "'tomato_healthy','tomato_blight','tomato_leaf_curl','tomato_mosaic','tomato_unknown',"
        "'cocoa_healthy','cocoa_blackpod','cocoa_swollen_shoot','cocoa_mirids','cocoa_unknown')"
    )
    op.execute("CREATE TYPE channel_enum AS ENUM ('whatsapp','telegram','mobile','web')")
    op.execute("CREATE TYPE language_enum AS ENUM ('fr','en')")
    op.execute("CREATE TYPE confidencelevel_enum AS ENUM ('low','medium','high')")

    op.create_table(
        "farmer",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("channel_id", sa.String(128), nullable=False),
        sa.Column("channel", postgresql.ENUM(name="channel_enum", create_type=False), nullable=False),
        sa.Column("region", sa.String(100), nullable=True),
        sa.Column("language", postgresql.ENUM(name="language_enum", create_type=False), nullable=False),
        sa.Column("consent_given_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("retain_photos", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("channel_id"),
    )
    op.create_index("ix_farmer_channel_id", "farmer", ["channel_id"])

    op.create_table(
        "model_version",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("crop", postgresql.ENUM(name="crop_enum", create_type=False), nullable=False),
        sa.Column("version", sa.String(50), nullable=False),
        sa.Column("dataset_version", sa.String(50), nullable=False),
        sa.Column("code_commit", sa.String(40), nullable=False),
        sa.Column("accuracy", sa.Float(), nullable=True),
        sa.Column("ece", sa.Float(), nullable=True),
        sa.Column("artifact_path", sa.String(512), nullable=False),
        sa.Column("deployed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_version_crop", "model_version", ["crop"])
    op.create_index("ix_model_version_is_active", "model_version", ["is_active"])

    op.create_table(
        "interaction",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("channel", postgresql.ENUM(name="channel_enum", create_type=False), nullable=False),
        sa.Column("crop", postgresql.ENUM(name="crop_enum", create_type=False), nullable=False),
        sa.Column("predicted_class", postgresql.ENUM(name="cropclass_enum", create_type=False), nullable=False),
        sa.Column("confidence_raw", sa.Float(), nullable=False),
        sa.Column("confidence_level", postgresql.ENUM(name="confidencelevel_enum", create_type=False), nullable=False),
        sa.Column("advice_template_version", sa.Integer(), nullable=True),
        sa.Column("image_ref", sa.String(512), nullable=True),
        sa.Column("farmer_id", sa.Integer(), sa.ForeignKey("farmer.id"), nullable=True),
        sa.Column("region", sa.String(100), nullable=True),
        sa.Column("escalated", sa.Boolean(), nullable=False),
        sa.Column("model_version_id", sa.Integer(), sa.ForeignKey("model_version.id"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "advice_template",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("crop", postgresql.ENUM(name="crop_enum", create_type=False), nullable=False),
        sa.Column("crop_class", postgresql.ENUM(name="cropclass_enum", create_type=False), nullable=False),
        sa.Column("language", postgresql.ENUM(name="language_enum", create_type=False), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(100), nullable=False),
        sa.Column("opening", sa.Text(), nullable=False),
        sa.Column("steps", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("consult_message", sa.Text(), nullable=False),
        sa.Column("reviewed_by", sa.String(100), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "extension_worker",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("region", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("whatsapp_available", sa.Boolean(), nullable=False),
        sa.Column("crops", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_extension_worker_region", "extension_worker", ["region"])
    op.create_index("ix_extension_worker_active", "extension_worker", ["active"])


def downgrade() -> None:
    op.drop_table("extension_worker")
    op.drop_table("advice_template")
    op.drop_table("interaction")
    op.drop_table("model_version")
    op.drop_table("farmer")
    op.execute("DROP TYPE confidencelevel_enum")
    op.execute("DROP TYPE language_enum")
    op.execute("DROP TYPE channel_enum")
    op.execute("DROP TYPE cropclass_enum")
    op.execute("DROP TYPE crop_enum")
