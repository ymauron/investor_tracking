from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.firm import PortfolioCompany
from app.models.enums import TherapeuticArea
from app.schemas.firm import (
    PortfolioCompanyCreate,
    PortfolioCompanyUpdate,
    PortfolioCompanyResponse,
)

router = APIRouter()


@router.get("/", response_model=list[PortfolioCompanyResponse])
def list_portfolio_companies(
    search: str | None = None,
    therapeutic_area: TherapeuticArea | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(PortfolioCompany)
    if search:
        query = query.filter(PortfolioCompany.name.ilike(f"%{search}%"))
    if therapeutic_area:
        query = query.filter(PortfolioCompany.therapeutic_area == therapeutic_area)
    return query.order_by(PortfolioCompany.name).offset((page - 1) * per_page).limit(per_page).all()


@router.get("/{portco_id}", response_model=PortfolioCompanyResponse)
def get_portfolio_company(
    portco_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    portco = db.query(PortfolioCompany).filter(PortfolioCompany.id == portco_id).first()
    if not portco:
        raise HTTPException(status_code=404, detail="Portfolio company not found")
    return portco


@router.post("/", response_model=PortfolioCompanyResponse, status_code=201)
def create_portfolio_company(
    data: PortfolioCompanyCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    portco = PortfolioCompany(**data.model_dump())
    db.add(portco)
    db.commit()
    db.refresh(portco)
    return portco


@router.put("/{portco_id}", response_model=PortfolioCompanyResponse)
def update_portfolio_company(
    portco_id: UUID,
    data: PortfolioCompanyUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    portco = db.query(PortfolioCompany).filter(PortfolioCompany.id == portco_id).first()
    if not portco:
        raise HTTPException(status_code=404, detail="Portfolio company not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(portco, key, value)
    db.commit()
    db.refresh(portco)
    return portco


@router.delete("/{portco_id}", status_code=204)
def delete_portfolio_company(
    portco_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    portco = db.query(PortfolioCompany).filter(PortfolioCompany.id == portco_id).first()
    if not portco:
        raise HTTPException(status_code=404, detail="Portfolio company not found")
    db.delete(portco)
    db.commit()
