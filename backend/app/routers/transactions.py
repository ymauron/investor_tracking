from datetime import date, datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.transaction import Transaction
from app.models.enums import TransactionType, TransactionSource, TherapeuticArea, ClinicalStage
from app.schemas.transaction import (
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse,
    CrawlStatsResponse,
    TransactionStatsResponse,
)

router = APIRouter()


def _to_response(txn: Transaction) -> dict:
    data = {
        "id": txn.id,
        "title": txn.title,
        "url": txn.url,
        "source": txn.source,
        "published_at": txn.published_at,
        "raw_description": txn.raw_description,
        "transaction_type": txn.transaction_type,
        "companies_mentioned": txn.companies_mentioned,
        "deal_value_mm": txn.deal_value_mm,
        "therapeutic_area": txn.therapeutic_area,
        "stage": txn.stage,
        "summary": txn.summary,
        "sentiment": txn.sentiment,
        "portfolio_company_id": txn.portfolio_company_id,
        "management_company_id": txn.management_company_id,
        "is_reviewed": txn.is_reviewed,
        "created_at": txn.created_at,
        "updated_at": txn.updated_at,
        "portfolio_company_name": txn.portfolio_company.name if txn.portfolio_company else None,
        "management_company_name": txn.management_company.name if txn.management_company else None,
    }
    return data


@router.get("/stats", response_model=TransactionStatsResponse)
def transaction_stats(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    total = db.query(func.count(Transaction.id)).scalar() or 0

    by_type_rows = (
        db.query(Transaction.transaction_type, func.count(Transaction.id))
        .group_by(Transaction.transaction_type)
        .all()
    )
    by_type = {(r[0].value if r[0] else "unknown"): r[1] for r in by_type_rows}

    by_source_rows = (
        db.query(Transaction.source, func.count(Transaction.id))
        .group_by(Transaction.source)
        .all()
    )
    by_source = {r[0].value: r[1] for r in by_source_rows}

    by_area_rows = (
        db.query(Transaction.therapeutic_area, func.count(Transaction.id))
        .filter(Transaction.therapeutic_area.isnot(None))
        .group_by(Transaction.therapeutic_area)
        .all()
    )
    by_area = {r[0].value: r[1] for r in by_area_rows}

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    this_week = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.published_at >= week_ago)
        .scalar() or 0
    )
    this_month = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.published_at >= month_ago)
        .scalar() or 0
    )

    return TransactionStatsResponse(
        total=total,
        by_type=by_type,
        by_source=by_source,
        by_area=by_area,
        this_week=this_week,
        this_month=this_month,
    )


@router.post("/crawl", response_model=CrawlStatsResponse)
def trigger_crawl(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    from app.services.crawler import crawl_all_feeds
    from app.services.matcher import clear_cache

    clear_cache()
    stats = crawl_all_feeds(db)
    return CrawlStatsResponse(**stats)


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    transaction_type: TransactionType | None = None,
    source: TransactionSource | None = None,
    therapeutic_area: TherapeuticArea | None = None,
    stage: ClinicalStage | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    search: str | None = None,
    linked_only: bool = False,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(Transaction)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if source:
        query = query.filter(Transaction.source == source)
    if therapeutic_area:
        query = query.filter(Transaction.therapeutic_area == therapeutic_area)
    if stage:
        query = query.filter(Transaction.stage == stage)
    if from_date:
        query = query.filter(Transaction.published_at >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.filter(Transaction.published_at <= datetime.combine(to_date, datetime.max.time()))
    if search:
        query = query.filter(Transaction.title.ilike(f"%{search}%"))
    if linked_only:
        query = query.filter(
            (Transaction.portfolio_company_id.isnot(None))
            | (Transaction.management_company_id.isnot(None))
        )

    total = query.count()
    items = (
        query.order_by(Transaction.published_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return TransactionListResponse(
        items=[_to_response(t) for t in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return _to_response(txn)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(txn, key, value)
    db.commit()
    db.refresh(txn)
    return _to_response(txn)


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(txn)
    db.commit()
