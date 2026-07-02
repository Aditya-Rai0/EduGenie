from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class QuizAttempt(Base, TimestampMixin):
    __tablename__ = "quiz_attempts"

    __table_args__ = (
        CheckConstraint(
            "score BETWEEN 0 AND 100",
            name="ck_quiz_attempts_score",
        ),
        UniqueConstraint(
            "enrollment_id",
            "quiz_id",
            "attempt_number",
            name="uq_quiz_attempts_enrollment_quiz_attempt",
        ),
        Index("idx_quiz_attempts_enrollment", "enrollment_id"),
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
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    answers: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, nullable=False
    )
    duration_sec: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    enrollment = relationship("Enrollment", back_populates="quiz_attempts")
    quiz = relationship("Quiz")
