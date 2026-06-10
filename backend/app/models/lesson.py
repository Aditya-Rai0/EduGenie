from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Lesson(Base, TimestampMixin):
    __tablename__ = "lessons"

    __table_args__ = (
        UniqueConstraint(
            "module_id", "position", name="uq_lessons_module_position"
        ),
        Index("idx_lessons_module", "module_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    module_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    script_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    slides_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    captions_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_min: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=10
    )
    word_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )
    verify_flags: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0
    )

    module = relationship("Module", back_populates="lessons")
