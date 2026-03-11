from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.individual import Individual, IndividualEducation
from app.models.role import Role
from app.models.movement import MovementEvent
from app.models.deal import DealParticipant
from app.models.note import Note
from app.models.enums import TherapeuticArea, EntityType
from app.schemas.individual import (
    IndividualCreate,
    IndividualUpdate,
    IndividualListResponse,
    IndividualDetailResponse,
)
from app.schemas.role import RoleResponse
from app.schemas.movement import MovementEventResponse
from app.schemas.deal import DealParticipantResponse
from app.schemas.note import NoteResponse

router = APIRouter()


@router.get("", response_model=list[IndividualListResponse])
def list_individuals(
    search: str | None = None,
    therapeutic_area: TherapeuticArea | None = None,
    firm_id: UUID | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(Individual)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Individual.first_name.ilike(pattern),
                Individual.last_name.ilike(pattern),
                Individual.email.ilike(pattern),
            )
        )
    if therapeutic_area:
        query = query.filter(Individual.primary_therapeutic_area == therapeutic_area)
    if firm_id:
        query = query.join(Role).filter(
            Role.management_company_id == firm_id, Role.is_current == True
        )
    query = query.order_by(Individual.last_name, Individual.first_name)
    return query.offset((page - 1) * per_page).limit(per_page).all()


@router.get("/{individual_id}", response_model=IndividualDetailResponse)
def get_individual(
    individual_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    individual = (
        db.query(Individual)
        .options(joinedload(Individual.education))
        .filter(Individual.id == individual_id)
        .first()
    )
    if not individual:
        raise HTTPException(status_code=404, detail="Individual not found")
    return individual


@router.post("", response_model=IndividualDetailResponse, status_code=201)
def create_individual(
    data: IndividualCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    individual = Individual(
        first_name=data.first_name,
        last_name=data.last_name,
        linkedin_url=data.linkedin_url,
        email=data.email,
        phone=data.phone,
        primary_therapeutic_area=data.primary_therapeutic_area,
        relationship_status=data.relationship_status,
        personal_notes=data.personal_notes,
    )
    if data.education:
        for edu in data.education:
            individual.education.append(
                IndividualEducation(
                    institution=edu.institution,
                    degree_type=edu.degree_type,
                    field_of_study=edu.field_of_study,
                    graduation_year=edu.graduation_year,
                )
            )
    db.add(individual)
    db.commit()
    db.refresh(individual)
    return individual


@router.put("/{individual_id}", response_model=IndividualDetailResponse)
def update_individual(
    individual_id: UUID,
    data: IndividualUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    individual = db.query(Individual).filter(Individual.id == individual_id).first()
    if not individual:
        raise HTTPException(status_code=404, detail="Individual not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(individual, key, value)
    db.commit()
    db.refresh(individual)
    return individual


@router.delete("/{individual_id}", status_code=204)
def delete_individual(
    individual_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    individual = db.query(Individual).filter(Individual.id == individual_id).first()
    if not individual:
        raise HTTPException(status_code=404, detail="Individual not found")
    db.delete(individual)
    db.commit()


@router.get("/{individual_id}/roles", response_model=list[RoleResponse])
def get_individual_roles(
    individual_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(Role)
        .filter(Role.individual_id == individual_id)
        .order_by(Role.is_current.desc(), Role.start_date.desc())
        .all()
    )


@router.get("/{individual_id}/movements", response_model=list[MovementEventResponse])
def get_individual_movements(
    individual_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    events = (
        db.query(MovementEvent)
        .filter(MovementEvent.individual_id == individual_id)
        .order_by(MovementEvent.joining_date.desc())
        .all()
    )
    return [
        MovementEventResponse(
            **{
                k: v
                for k, v in e.__dict__.items()
                if not k.startswith("_")
            },
            tags=[t.tag for t in e.tags],
        )
        for e in events
    ]


@router.get("/{individual_id}/deals", response_model=list[DealParticipantResponse])
def get_individual_deals(
    individual_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(DealParticipant)
        .filter(DealParticipant.individual_id == individual_id)
        .all()
    )


@router.get("/{individual_id}/notes", response_model=list[NoteResponse])
def get_individual_notes(
    individual_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(Note)
        .filter(
            Note.entity_type == EntityType.individual,
            Note.entity_id == individual_id,
        )
        .order_by(Note.created_at.desc())
        .all()
    )
