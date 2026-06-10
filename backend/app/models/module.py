from __future__ import annotations

import uuid

from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Module(Base):
    __tablename__ = "modules"

    __table_args__ = (
        CheckConstraint(
            "bloom_level IN ('remember', 'understand', 'apply', 'analyze', 'evaluate', 'create')",
            name="ck_modules_bloom_level",
        ),
        UniqueConstraint(
            "course_id", "position", name="uq_modules_course_position"
        ),
        Index("idx_modules_course", "course_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    learning_objective: Mapped[str | None] = mapped_column(Text, nullable=True)
    bloom_level: Mapped[str | None] = mapped_column(
        String(20), nullable=True, default="remember"
    )
    estimated_duration_min: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=30
    )
    prerequisites: Mapped[list[uuid.UUID] | None] = mapped_column(
        ARRAY(PG_UUID(as_uuid=True)), nullable=True, default=list
    )

    course = relationship("Course", back_populates="modules")
    lessons = relationship(
        "Lesson", back_populates="module", lazy="selectin", order_by="Lesson.position"
    )
    quizzes = relationship(
        "Quiz", back_populates="module", lazy="selectin"
    )
