from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.models.base import Base, TimestampMixin


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'building', 'review', 'published', 'archived')",
            name="ck_courses_status",
        ),
        CheckConstraint(
            "difficulty IN ('beginner', 'intermediate', 'advanced')",
            name="ck_courses_difficulty",
        ),
        Index("idx_courses_creator", "creator_id"),
        Index(
            "idx_courses_status",
            "status",
            postgresql_where=text("status = 'published'"),
        ),
        Index("idx_courses_language", "language"),
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
    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("creators.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(280), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="draft"
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    stripe_product_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    stripe_price_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    topic_brief: Mapped[dict] = mapped_column(JSONB, nullable=False)
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, default="en"
    )
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_duration_min: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )
    difficulty: Mapped[str | None] = mapped_column(
        String(20), nullable=True, default="beginner"
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    organization = relationship("Organization", back_populates="courses")
    creator = relationship("Creator", back_populates="courses")
    versions = relationship(
        "CourseVersion", back_populates="course", lazy="selectin"
    )
    modules = relationship(
        "Module", back_populates="course", lazy="selectin", order_by="Module.position"
    )
