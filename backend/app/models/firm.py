import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Text, Integer, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.database import Base
from app.models.enums import FirmType, TherapeuticArea


class ManagementCompany(Base):
    __tablename__ = "management_companies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    firm_type: Mapped[FirmType] = mapped_column(
        ENUM(FirmType, name="firm_type", create_type=False), nullable=False
    )
    website: Mapped[str | None] = mapped_column(String(500))
    hq_city: Mapped[str | None] = mapped_column(String(100))
    hq_state: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    fund_vehicles: Mapped[list["FundVehicle"]] = relationship(
        back_populates="management_company", cascade="all, delete-orphan"
    )
    portfolio_companies: Mapped[list["PortfolioCompany"]] = relationship(
        back_populates="management_company", cascade="all, delete-orphan"
    )
    roles: Mapped[list["Role"]] = relationship(  # noqa: F821
        back_populates="management_company"
    )


class FundVehicle(Base):
    __tablename__ = "fund_vehicles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    management_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("management_companies.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    vintage_year: Mapped[int | None] = mapped_column(Integer)
    target_size_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    final_close_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    strategy_focus: Mapped[TherapeuticArea | None] = mapped_column(
        ENUM(TherapeuticArea, name="therapeutic_area", create_type=False)
    )
    status: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    management_company: Mapped["ManagementCompany"] = relationship(
        back_populates="fund_vehicles"
    )
    lp_commitments: Mapped[list["LPCommitment"]] = relationship(  # noqa: F821
        back_populates="fund_vehicle", cascade="all, delete-orphan"
    )
    roles: Mapped[list["Role"]] = relationship(  # noqa: F821
        back_populates="fund_vehicle"
    )

    __table_args__ = (
        Index("ix_fund_vehicles_mgmt_co", "management_company_id"),
    )


class PortfolioCompany(Base):
    __tablename__ = "portfolio_companies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    management_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("management_companies.id", ondelete="CASCADE"),
        nullable=False,
    )
    fund_vehicle_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fund_vehicles.id", ondelete="SET NULL"),
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    therapeutic_area: Mapped[TherapeuticArea | None] = mapped_column(
        ENUM(TherapeuticArea, name="therapeutic_area", create_type=False)
    )
    stage: Mapped[str | None] = mapped_column(String(50))
    website: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    management_company: Mapped["ManagementCompany"] = relationship(
        back_populates="portfolio_companies"
    )
    fund_vehicle: Mapped["FundVehicle | None"] = relationship()
    roles: Mapped[list["Role"]] = relationship(  # noqa: F821
        back_populates="portfolio_company"
    )

    __table_args__ = (
        Index("ix_portco_mgmt_co", "management_company_id"),
        Index("ix_portco_fund", "fund_vehicle_id"),
    )
