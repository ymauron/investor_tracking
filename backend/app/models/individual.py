import uuid
from datetime import datetime

from sqlalchemy import String, Text, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.database import Base
from app.models.enums import TherapeuticArea


class Individual(Base):
    __tablename__ = "individuals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    linkedin_url: Mapped[str | None] = mapped_column(String(500))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    primary_therapeutic_area: Mapped[TherapeuticArea | None] = mapped_column(
        ENUM(TherapeuticArea, name="therapeutic_area", create_type=False)
    )
    relationship_status: Mapped[str | None] = mapped_column(String(100))
    personal_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    education: Mapped[list["IndividualEducation"]] = relationship(
        back_populates="individual", cascade="all, delete-orphan"
    )
    roles: Mapped[list["Role"]] = relationship(  # noqa: F821
        back_populates="individual", cascade="all, delete-orphan"
    )
    movement_events: Mapped[list["MovementEvent"]] = relationship(  # noqa: F821
        back_populates="individual", cascade="all, delete-orphan"
    )
    deal_participations: Mapped[list["DealParticipant"]] = relationship(  # noqa: F821
        back_populates="individual", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_individuals_name", "last_name", "first_name"),
    )


class IndividualEducation(Base):
    __tablename__ = "individual_education"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    individual_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("individuals.id", ondelete="CASCADE"),
        nullable=False,
    )
    institution: Mapped[str] = mapped_column(String(200), nullable=False)
    degree_type: Mapped[str] = mapped_column(
        ENUM(
            "ba", "bs", "mba", "md", "phd", "md_phd", "jd", "mph", "ms", "other",
            name="degree_type", create_type=False,
        ),
        nullable=False,
    )
    field_of_study: Mapped[str | None] = mapped_column(String(200))
    graduation_year: Mapped[int | None] = mapped_column()

    individual: Mapped["Individual"] = relationship(back_populates="education")

    __table_args__ = (
        Index("ix_education_individual", "individual_id"),
    )
