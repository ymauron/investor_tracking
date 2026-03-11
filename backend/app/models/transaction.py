import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Boolean, Text, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSON

from app.database import Base
from app.models.enums import (
    TherapeuticArea,
    TransactionType,
    TransactionSource,
    ClinicalStage,
    Sentiment,
)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    source: Mapped[TransactionSource] = mapped_column(
        ENUM(TransactionSource, name="transaction_source", create_type=True),
        nullable=False,
    )
    published_at: Mapped[datetime] = mapped_column(nullable=False)
    raw_description: Mapped[str | None] = mapped_column(Text)
    transaction_type: Mapped[TransactionType | None] = mapped_column(
        ENUM(TransactionType, name="transaction_type", create_type=True)
    )
    companies_mentioned: Mapped[dict | None] = mapped_column(JSON)
    deal_value_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    therapeutic_area: Mapped[TherapeuticArea | None] = mapped_column(
        ENUM(TherapeuticArea, name="therapeutic_area", create_type=True)
    )
    stage: Mapped[ClinicalStage | None] = mapped_column(
        ENUM(ClinicalStage, name="clinical_stage", create_type=True)
    )
    summary: Mapped[str | None] = mapped_column(Text)
    sentiment: Mapped[Sentiment | None] = mapped_column(
        ENUM(Sentiment, name="sentiment", create_type=True)
    )
    portfolio_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolio_companies.id", ondelete="SET NULL"),
    )
    management_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("management_companies.id", ondelete="SET NULL"),
    )
    is_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    portfolio_company: Mapped["PortfolioCompany | None"] = relationship()  # noqa: F821
    management_company: Mapped["ManagementCompany | None"] = relationship()  # noqa: F821

    __table_args__ = (
        Index("ix_transactions_published", "published_at"),
        Index("ix_transactions_type", "transaction_type"),
        Index("ix_transactions_source", "source"),
        Index("ix_transactions_area", "therapeutic_area"),
        Index("ix_transactions_portco", "portfolio_company_id"),
        Index("ix_transactions_mgmt", "management_company_id"),
    )
