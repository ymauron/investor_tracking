from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import MoveType, ConfidenceLevel


class MovementEventBase(BaseModel):
    individual_id: UUID
    origin_role_id: UUID | None = None
    destination_role_id: UUID | None = None
    departure_date: date | None = None
    joining_date: date | None = None
    move_type: MoveType
    is_spinout: bool = False
    reason: str | None = None
    carry_economics_notes: str | None = None
    confidence: ConfidenceLevel = ConfidenceLevel.rumor
    source_of_intel: str | None = None
    tags: list[str] | None = None


class MovementEventCreate(MovementEventBase):
    pass


class MovementEventUpdate(BaseModel):
    departure_date: date | None = None
    joining_date: date | None = None
    move_type: MoveType | None = None
    is_spinout: bool | None = None
    reason: str | None = None
    carry_economics_notes: str | None = None
    confidence: ConfidenceLevel | None = None
    source_of_intel: str | None = None
    tags: list[str] | None = None


class MovementEventResponse(BaseModel):
    id: UUID
    individual_id: UUID
    origin_role_id: UUID | None = None
    destination_role_id: UUID | None = None
    departure_date: date | None = None
    joining_date: date | None = None
    move_type: MoveType
    is_spinout: bool
    reason: str | None = None
    carry_economics_notes: str | None = None
    confidence: ConfidenceLevel
    source_of_intel: str | None = None
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
