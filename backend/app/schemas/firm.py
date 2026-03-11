from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import FirmType, TherapeuticArea


class ManagementCompanyBase(BaseModel):
    name: str
    firm_type: FirmType
    website: str | None = None
    hq_city: str | None = None
    hq_state: str | None = None
    description: str | None = None


class ManagementCompanyCreate(ManagementCompanyBase):
    pass


class ManagementCompanyUpdate(BaseModel):
    name: str | None = None
    firm_type: FirmType | None = None
    website: str | None = None
    hq_city: str | None = None
    hq_state: str | None = None
    description: str | None = None


class ManagementCompanyResponse(ManagementCompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FundVehicleBase(BaseModel):
    management_company_id: UUID
    name: str
    vintage_year: int | None = None
    target_size_mm: Decimal | None = None
    final_close_mm: Decimal | None = None
    strategy_focus: TherapeuticArea | None = None
    status: str | None = None


class FundVehicleCreate(FundVehicleBase):
    pass


class FundVehicleUpdate(BaseModel):
    name: str | None = None
    vintage_year: int | None = None
    target_size_mm: Decimal | None = None
    final_close_mm: Decimal | None = None
    strategy_focus: TherapeuticArea | None = None
    status: str | None = None


class FundVehicleResponse(FundVehicleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PortfolioCompanyBase(BaseModel):
    management_company_id: UUID
    fund_vehicle_id: UUID | None = None
    name: str
    therapeutic_area: TherapeuticArea | None = None
    stage: str | None = None
    website: str | None = None
    description: str | None = None


class PortfolioCompanyCreate(PortfolioCompanyBase):
    pass


class PortfolioCompanyUpdate(BaseModel):
    name: str | None = None
    therapeutic_area: TherapeuticArea | None = None
    stage: str | None = None
    website: str | None = None
    description: str | None = None


class PortfolioCompanyResponse(PortfolioCompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
