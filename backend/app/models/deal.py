import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Boolean, Text, Date, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.database import Base
from app.models.enums import TherapeuticArea, ConfidenceLevel


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    portfolio_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolio_companies.id", ondelete="SET NULL"),
    )
    therapeutic_area: Mapped[TherapeuticArea | None] = mapped_column(
        ENUM(TherapeuticArea, name="therapeutic_area", create_type=False)
    )
    deal_date: Mapped[date | None] = mapped_column(Date)
    deal_type: Mapped[str | None] = mapped_column(String(50))
    deal_size_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    description: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[ConfidenceLevel] = mapped_column(
        ENUM(ConfidenceLevel, name="confidence_level", create_type=False),
        default=ConfidenceLevel.confirmed,
    )
    source: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    portfolio_company: Mapped["PortfolioCompany | None"] = relationship()  # noqa: F821
    participants: Mapped[list["DealParticipant"]] = relationship(
        back_populates="deal", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_deals_date", "deal_date"),
        Index("ix_deals_area", "therapeutic_area"),
    )


class DealParticipant(Base):
    __tablename__ = "deal_participants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("deals.id", ondelete="CASCADE"),
        nullable=False,
    )
    individual_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("individuals.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
    )
    is_lead: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped["Deal"] = relationship(back_populates="participants")
    individual: Mapped["Individual"] = relationship(  # noqa: F821
        back_populates="deal_participations"
    )
    role: Mapped["Role | None"] = relationship()  # noqa: F821

    __table_args__ = (
        Index("ix_deal_parts_deal", "deal_id"),
        Index("ix_deal_parts_individual", "individual_id"),
    )
