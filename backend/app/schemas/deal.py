from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import TherapeuticArea, ConfidenceLevel


class DealParticipantBase(BaseModel):
    individual_id: UUID
    role_id: UUID | None = None
    is_lead: bool = False


class DealParticipantResponse(DealParticipantBase):
    id: UUID
    deal_id: UUID

    class Config:
        from_attributes = True


class DealBase(BaseModel):
    name: str
    portfolio_company_id: UUID | None = None
    therapeutic_area: TherapeuticArea | None = None
    deal_date: date | None = None
    deal_type: str | None = None
    deal_size_mm: Decimal | None = None
    description: str | None = None
    confidence: ConfidenceLevel = ConfidenceLevel.confirmed
    source: str | None = None


class DealCreate(DealBase):
    participants: list[DealParticipantBase] | None = None


class DealUpdate(BaseModel):
    name: str | None = None
    portfolio_company_id: UUID | None = None
    therapeutic_area: TherapeuticArea | None = None
    deal_date: date | None = None
    deal_type: str | None = None
    deal_size_mm: Decimal | None = None
    description: str | None = None
    confidence: ConfidenceLevel | None = None
    source: str | None = None


class DealResponse(DealBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    participants: list[DealParticipantResponse] = []

    class Config:
        from_attributes = True
