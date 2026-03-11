from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class LPCommitmentBase(BaseModel):
    fund_vehicle_id: UUID
    commitment_amount_mm: Decimal | None = None
    commitment_date: date | None = None
    status: str | None = None
    notes: str | None = None


class LPCommitmentCreate(LPCommitmentBase):
    pass


class LPCommitmentUpdate(BaseModel):
    commitment_amount_mm: Decimal | None = None
    commitment_date: date | None = None
    status: str | None = None
    notes: str | None = None


class LPCommitmentResponse(LPCommitmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
