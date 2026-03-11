from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    individual_id: UUID
    management_company_id: UUID | None = None
    fund_vehicle_id: UUID | None = None
    portfolio_company_id: UUID | None = None
    title: str
    is_current: bool = True
    start_date: date | None = None
    end_date: date | None = None
    seniority_level: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    title: str | None = None
    is_current: bool | None = None
    start_date: date | None = None
    end_date: date | None = None
    seniority_level: str | None = None


class RoleResponse(RoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleWithDetailsResponse(RoleResponse):
    firm_name: str | None = None
    individual_name: str | None = None
