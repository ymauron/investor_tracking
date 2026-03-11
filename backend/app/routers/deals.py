from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.deal import Deal, DealParticipant
from app.models.enums import TherapeuticArea
from app.schemas.deal import DealCreate, DealUpdate, DealResponse

router = APIRouter()


@router.get("", response_model=list[DealResponse])
def list_deals(
    therapeutic_area: TherapeuticArea | None = None,
    individual_id: UUID | None = None,
    deal_type: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(Deal).options(joinedload(Deal.participants))
    if therapeutic_area:
        query = query.filter(Deal.therapeutic_area == therapeutic_area)
    if individual_id:
        query = query.join(DealParticipant).filter(
            DealParticipant.individual_id == individual_id
        )
    if deal_type:
        query = query.filter(Deal.deal_type == deal_type)
    if from_date:
        query = query.filter(Deal.deal_date >= from_date)
    if to_date:
        query = query.filter(Deal.deal_date <= to_date)
    deals = (
        query.order_by(Deal.deal_date.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    # Deduplicate due to joinedload + join
    seen = set()
    unique_deals = []
    for d in deals:
        if d.id not in seen:
            seen.add(d.id)
            unique_deals.append(d)
    return unique_deals


@router.get("/{deal_id}", response_model=DealResponse)
def get_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    deal = (
        db.query(Deal)
        .options(joinedload(Deal.participants))
        .filter(Deal.id == deal_id)
        .first()
    )
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("", response_model=DealResponse, status_code=201)
def create_deal(
    data: DealCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    participants = data.participants or []
    deal = Deal(
        name=data.name,
        portfolio_company_id=data.portfolio_company_id,
        therapeutic_area=data.therapeutic_area,
        deal_date=data.deal_date,
        deal_type=data.deal_type,
        deal_size_mm=data.deal_size_mm,
        description=data.description,
        confidence=data.confidence,
        source=data.source,
    )
    for p in participants:
        deal.participants.append(
            DealParticipant(
                individual_id=p.individual_id,
                role_id=p.role_id,
                is_lead=p.is_lead,
            )
        )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


@router.put("/{deal_id}", response_model=DealResponse)
def update_deal(
    deal_id: UUID,
    data: DealUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(deal, key, value)
    db.commit()
    db.refresh(deal)
    return deal


@router.delete("/{deal_id}", status_code=204)
def delete_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(deal)
    db.commit()
