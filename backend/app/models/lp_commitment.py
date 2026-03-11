import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Date, Numeric, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class LPCommitment(Base):
    __tablename__ = "lp_commitments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fund_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fund_vehicles.id", ondelete="CASCADE"),
        nullable=False,
    )
    commitment_amount_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    commitment_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    fund_vehicle: Mapped["FundVehicle"] = relationship(  # noqa: F821
        back_populates="lp_commitments"
    )

    __table_args__ = (
        Index("ix_lp_fund", "fund_vehicle_id"),
    )
