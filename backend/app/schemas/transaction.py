from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import (
    TherapeuticArea,
    TransactionType,
    TransactionSource,
    ClinicalStage,
    Sentiment,
)


class TransactionBase(BaseModel):
    title: str
    url: str
    source: TransactionSource
    published_at: datetime
    raw_description: str | None = None
    transaction_type: TransactionType | None = None
    companies_mentioned: list[str] | None = None
    deal_value_mm: Decimal | None = None
    therapeutic_area: TherapeuticArea | None = None
    stage: ClinicalStage | None = None
    summary: str | None = None
    sentiment: Sentiment | None = None
    portfolio_company_id: UUID | None = None
    management_company_id: UUID | None = None
    is_reviewed: bool = False


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    transaction_type: TransactionType | None = None
    therapeutic_area: TherapeuticArea | None = None
    stage: ClinicalStage | None = None
    summary: str | None = None
    sentiment: Sentiment | None = None
    portfolio_company_id: UUID | None = None
    management_company_id: UUID | None = None
    is_reviewed: bool | None = None


class TransactionResponse(TransactionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    portfolio_company_name: str | None = None
    management_company_name: str | None = None

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    page: int
    per_page: int


class CrawlStatsResponse(BaseModel):
    new: int
    skipped: int
    errors: int


class TransactionStatsResponse(BaseModel):
    total: int
    by_type: dict[str, int]
    by_source: dict[str, int]
    by_area: dict[str, int]
    this_week: int
    this_month: int
