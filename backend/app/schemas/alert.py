from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import TherapeuticArea, TransactionType
from app.schemas.transaction import TransactionResponse


class AlertRuleBase(BaseModel):
    name: str
    therapeutic_area: TherapeuticArea | None = None
    transaction_type: TransactionType | None = None
    keyword: str | None = None
    company_name: str | None = None
    is_active: bool = True


class AlertRuleCreate(AlertRuleBase):
    pass


class AlertRuleUpdate(BaseModel):
    name: str | None = None
    therapeutic_area: TherapeuticArea | None = None
    transaction_type: TransactionType | None = None
    keyword: str | None = None
    company_name: str | None = None
    is_active: bool | None = None


class AlertRuleResponse(AlertRuleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlertNotificationResponse(BaseModel):
    id: UUID
    transaction_id: UUID
    alert_rule_id: UUID
    is_read: bool
    created_at: datetime
    transaction: TransactionResponse
    alert_rule_name: str

    class Config:
        from_attributes = True


class UnreadCountResponse(BaseModel):
    count: int
