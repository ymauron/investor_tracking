import uuid
from datetime import date, datetime

from sqlalchemy import String, Boolean, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    individual_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("individuals.id", ondelete="CASCADE"),
        nullable=False,
    )
    management_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("management_companies.id", ondelete="CASCADE"),
    )
    fund_vehicle_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fund_vehicles.id", ondelete="CASCADE"),
    )
    portfolio_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolio_companies.id", ondelete="CASCADE"),
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    seniority_level: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    individual: Mapped["Individual"] = relationship(back_populates="roles")  # noqa: F821
    management_company: Mapped["ManagementCompany | None"] = relationship(  # noqa: F821
        back_populates="roles"
    )
    fund_vehicle: Mapped["FundVehicle | None"] = relationship(  # noqa: F821
        back_populates="roles"
    )
    portfolio_company: Mapped["PortfolioCompany | None"] = relationship(  # noqa: F821
        back_populates="roles"
    )

    __table_args__ = (
        Index("ix_roles_individual", "individual_id"),
        Index("ix_roles_mgmt_co", "management_company_id"),
        Index("ix_roles_current", "is_current"),
    )
