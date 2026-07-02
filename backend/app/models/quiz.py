from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Quiz(Base, TimestampMixin):
    __tablename__ = "quizzes"

    __table_args__ = (
        CheckConstraint(
            "pass_threshold BETWEEN 0 AND 100",
            name="ck_quizzes_pass_threshold",
        ),
        CheckConstraint(
            "module_id IS NOT NULL OR lesson_id IS NOT NULL",
            name="ck_quizzes_module_or_lesson",
        ),
        Index("idx_quizzes_module", "module_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    module_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"), nullable=True
    )
    lesson_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True
    )
    pass_threshold: Mapped[int] = mapped_column(
        Integer, nullable=False, default=70
    )
    max_attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3
    )
    questions: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, nullable=False, default=list, server_default="[]"
    )

    module = relationship("Module", back_populates="quizzes")
