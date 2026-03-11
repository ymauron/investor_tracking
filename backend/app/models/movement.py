import uuid
from datetime import date, datetime

from sqlalchemy import String, Boolean, Text, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.database import Base
from app.models.enums import MoveType, ConfidenceLevel


class MovementEvent(Base):
    __tablename__ = "movement_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    individual_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("individuals.id", ondelete="CASCADE"),
        nullable=False,
    )
    origin_role_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
    )
    destination_role_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
    )
    departure_date: Mapped[date | None] = mapped_column(Date)
    joining_date: Mapped[date | None] = mapped_column(Date)
    move_type: Mapped[MoveType] = mapped_column(
        ENUM(MoveType, name="move_type", create_type=False), nullable=False
    )
    is_spinout: Mapped[bool] = mapped_column(Boolean, default=False)
    reason: Mapped[str | None] = mapped_column(Text)
    carry_economics_notes: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[ConfidenceLevel] = mapped_column(
        ENUM(ConfidenceLevel, name="confidence_level", create_type=False),
        default=ConfidenceLevel.rumor,
    )
    source_of_intel: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    individual: Mapped["Individual"] = relationship(  # noqa: F821
        back_populates="movement_events"
    )
    origin_role: Mapped["Role | None"] = relationship(  # noqa: F821
        foreign_keys=[origin_role_id]
    )
    destination_role: Mapped["Role | None"] = relationship(  # noqa: F821
        foreign_keys=[destination_role_id]
    )
    tags: Mapped[list["MovementEventTag"]] = relationship(
        back_populates="movement_event", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_movements_individual", "individual_id"),
        Index("ix_movements_departure", "departure_date"),
        Index("ix_movements_joining", "joining_date"),
    )


class MovementEventTag(Base):
    __tablename__ = "movement_event_tags"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    movement_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("movement_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    tag: Mapped[str] = mapped_column(String(100), nullable=False)

    movement_event: Mapped["MovementEvent"] = relationship(back_populates="tags")

    __table_args__ = (
        Index("ix_movement_tags_event", "movement_event_id"),
        Index("ix_movement_tags_tag", "tag"),
    )
