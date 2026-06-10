from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Progress(Base):
    __tablename__ = "progress"

    __table_args__ = (
        CheckConstraint(
            "watch_depth_pct BETWEEN 0 AND 100",
            name="ck_progress_watch_depth",
        ),
        UniqueConstraint(
            "enrollment_id", "lesson_id", name="uq_progress_enrollment_lesson"
        ),
        Index("idx_progress_enrollment", "enrollment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    enrollment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    watch_depth_pct: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True, default=0
    )
    time_spent_sec: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    enrollment = relationship("Enrollment", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress_set")
