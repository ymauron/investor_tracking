from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import TherapeuticArea, DegreeType


class EducationBase(BaseModel):
    institution: str
    degree_type: str
    field_of_study: str | None = None
    graduation_year: int | None = None


class EducationCreate(EducationBase):
    pass


class EducationResponse(EducationBase):
    id: UUID
    individual_id: UUID

    class Config:
        from_attributes = True


class IndividualBase(BaseModel):
    first_name: str
    last_name: str
    linkedin_url: str | None = None
    email: str | None = None
    phone: str | None = None
    primary_therapeutic_area: TherapeuticArea | None = None
    relationship_status: str | None = None
    personal_notes: str | None = None


class IndividualCreate(IndividualBase):
    education: list[EducationCreate] | None = None


class IndividualUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    linkedin_url: str | None = None
    email: str | None = None
    phone: str | None = None
    primary_therapeutic_area: TherapeuticArea | None = None
    relationship_status: str | None = None
    personal_notes: str | None = None


class IndividualListResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    primary_therapeutic_area: TherapeuticArea | None = None
    relationship_status: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class IndividualDetailResponse(IndividualBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    education: list[EducationResponse] = []

    class Config:
        from_attributes = True
