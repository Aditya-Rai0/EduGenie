from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Creator(Base, TimestampMixin):
    __tablename__ = "creators"

    __table_args__ = (
        CheckConstraint(
            "plan_tier IN ('starter', 'creator', 'studio', 'enterprise')",
            name="ck_creators_plan_tier",
        ),
        Index("idx_creators_org", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    supabase_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False
    )
    plan_tier: Mapped[str] = mapped_column(
        String(20), nullable=False, default="starter"
    )
    voice_model_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    brand_settings: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    organization = relationship("Organization", back_populates="creators")
    courses = relationship(
        "Course", back_populates="creator", lazy="selectin"
    )
