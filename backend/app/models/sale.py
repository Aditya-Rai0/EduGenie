from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Sale(Base, TimestampMixin):
    __tablename__ = "sales"

    __table_args__ = (
        CheckConstraint(
            "channel IN ('direct', 'affiliate', 'promo')",
            name="ck_sales_channel",
        ),
        Index("idx_sales_course", "course_id"),
        Index("idx_sales_stripe", "stripe_payment_intent_id"),
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
    enrollment_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("enrollments.id"), nullable=True
    )
    stripe_payment_intent_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    platform_fee: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True, default=0
    )
    creator_earnings: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True, default=0
    )
    channel: Mapped[str | None] = mapped_column(
        String(20), nullable=True, default="direct"
    )
    promo_code: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    refunded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    course = relationship("Course", back_populates="sales")
