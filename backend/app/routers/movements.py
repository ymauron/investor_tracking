from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.movement import MovementEvent, MovementEventTag
from app.models.enums import ConfidenceLevel
from app.schemas.movement import (
    MovementEventCreate,
    MovementEventUpdate,
    MovementEventResponse,
)

router = APIRouter()


def _to_response(event: MovementEvent) -> MovementEventResponse:
    return MovementEventResponse(
        id=event.id,
        individual_id=event.individual_id,
        origin_role_id=event.origin_role_id,
        destination_role_id=event.destination_role_id,
        departure_date=event.departure_date,
        joining_date=event.joining_date,
        move_type=event.move_type,
        is_spinout=event.is_spinout,
        reason=event.reason,
        carry_economics_notes=event.carry_economics_notes,
        confidence=event.confidence,
        source_of_intel=event.source_of_intel,
        tags=[t.tag for t in event.tags],
        created_at=event.created_at,
        updated_at=event.updated_at,
    )


@router.get("/", response_model=list[MovementEventResponse])
def list_movements(
    individual_id: UUID | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    tag: str | None = None,
    confidence: ConfidenceLevel | None = None,
    is_spinout: bool | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(MovementEvent)
    if individual_id:
        query = query.filter(MovementEvent.individual_id == individual_id)
    if from_date:
        query = query.filter(MovementEvent.joining_date >= from_date)
    if to_date:
        query = query.filter(MovementEvent.joining_date <= to_date)
    if tag:
        query = query.join(MovementEventTag).filter(MovementEventTag.tag == tag)
    if confidence:
        query = query.filter(MovementEvent.confidence == confidence)
    if is_spinout is not None:
        query = query.filter(MovementEvent.is_spinout == is_spinout)
    events = (
        query.order_by(MovementEvent.joining_date.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return [_to_response(e) for e in events]


@router.get("/{movement_id}", response_model=MovementEventResponse)
def get_movement(
    movement_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    event = db.query(MovementEvent).filter(MovementEvent.id == movement_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Movement event not found")
    return _to_response(event)


@router.post("/", response_model=MovementEventResponse, status_code=201)
def create_movement(
    data: MovementEventCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    tags = data.tags or []
    event = MovementEvent(
        individual_id=data.individual_id,
        origin_role_id=data.origin_role_id,
        destination_role_id=data.destination_role_id,
        departure_date=data.departure_date,
        joining_date=data.joining_date,
        move_type=data.move_type,
        is_spinout=data.is_spinout,
        reason=data.reason,
        carry_economics_notes=data.carry_economics_notes,
        confidence=data.confidence,
        source_of_intel=data.source_of_intel,
    )
    for tag_name in tags:
        event.tags.append(MovementEventTag(tag=tag_name))
    db.add(event)
    db.commit()
    db.refresh(event)
    return _to_response(event)


@router.put("/{movement_id}", response_model=MovementEventResponse)
def update_movement(
    movement_id: UUID,
    data: MovementEventUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    event = db.query(MovementEvent).filter(MovementEvent.id == movement_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Movement event not found")
    update_data = data.model_dump(exclude_unset=True)
    tags = update_data.pop("tags", None)
    for key, value in update_data.items():
        setattr(event, key, value)
    if tags is not None:
        db.query(MovementEventTag).filter(
            MovementEventTag.movement_event_id == movement_id
        ).delete()
        for tag_name in tags:
            event.tags.append(MovementEventTag(tag=tag_name))
    db.commit()
    db.refresh(event)
    return _to_response(event)


@router.delete("/{movement_id}", status_code=204)
def delete_movement(
    movement_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    event = db.query(MovementEvent).filter(MovementEvent.id == movement_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Movement event not found")
    db.delete(event)
    db.commit()
