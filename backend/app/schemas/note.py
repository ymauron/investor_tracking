from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import EntityType


class NoteBase(BaseModel):
    entity_type: EntityType
    entity_id: UUID
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    content: str


class NoteResponse(NoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
