from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Affiliate(Base, TimestampMixin):
    __tablename__ = "affiliates"

    __table_args__ = (
        CheckConstraint(
            "commission_pct BETWEEN 0 AND 100",
            name="ck_affiliates_commission_pct",
        ),
        UniqueConstraint(
            "course_id", "creator_id", name="uq_affiliates_course_creator"
        ),
        Index("idx_affiliates_course", "course_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("creators.id", ondelete="CASCADE"), nullable=False
    )
    affiliate_name: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    commission_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=10
    )
    cookie_window_days: Mapped[int] = mapped_column(
        Integer, nullable=False, default=30
    )
    referral_link: Mapped[str] = mapped_column(Text, nullable=False)
    total_clicks: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )
    total_conversions: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )
    total_earned: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True, default=0
    )

    course = relationship("Course")
    creator = relationship("Creator", back_populates="affiliates")
