from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.firm import ManagementCompany, FundVehicle, PortfolioCompany
from app.models.role import Role
from app.models.individual import Individual
from app.models.enums import FirmType
from app.schemas.firm import (
    ManagementCompanyCreate,
    ManagementCompanyUpdate,
    ManagementCompanyResponse,
    FundVehicleResponse,
    PortfolioCompanyResponse,
)
from app.schemas.individual import IndividualListResponse

router = APIRouter()


@router.get("/", response_model=list[ManagementCompanyResponse])
def list_firms(
    search: str | None = None,
    firm_type: FirmType | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(ManagementCompany)
    if search:
        query = query.filter(ManagementCompany.name.ilike(f"%{search}%"))
    if firm_type:
        query = query.filter(ManagementCompany.firm_type == firm_type)
    query = query.order_by(ManagementCompany.name)
    return query.offset((page - 1) * per_page).limit(per_page).all()


@router.get("/{firm_id}", response_model=ManagementCompanyResponse)
def get_firm(
    firm_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    firm = db.query(ManagementCompany).filter(ManagementCompany.id == firm_id).first()
    if not firm:
        raise HTTPException(status_code=404, detail="Firm not found")
    return firm


@router.post("/", response_model=ManagementCompanyResponse, status_code=201)
def create_firm(
    data: ManagementCompanyCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    firm = ManagementCompany(**data.model_dump())
    db.add(firm)
    db.commit()
    db.refresh(firm)
    return firm


@router.put("/{firm_id}", response_model=ManagementCompanyResponse)
def update_firm(
    firm_id: UUID,
    data: ManagementCompanyUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    firm = db.query(ManagementCompany).filter(ManagementCompany.id == firm_id).first()
    if not firm:
        raise HTTPException(status_code=404, detail="Firm not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(firm, key, value)
    db.commit()
    db.refresh(firm)
    return firm


@router.delete("/{firm_id}", status_code=204)
def delete_firm(
    firm_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    firm = db.query(ManagementCompany).filter(ManagementCompany.id == firm_id).first()
    if not firm:
        raise HTTPException(status_code=404, detail="Firm not found")
    db.delete(firm)
    db.commit()


@router.get("/{firm_id}/people", response_model=list[IndividualListResponse])
def get_firm_people(
    firm_id: UUID,
    current_only: bool = True,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = (
        db.query(Individual)
        .join(Role)
        .filter(Role.management_company_id == firm_id)
    )
    if current_only:
        query = query.filter(Role.is_current == True)
    return query.order_by(Individual.last_name).all()


@router.get("/{firm_id}/funds", response_model=list[FundVehicleResponse])
def get_firm_funds(
    firm_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(FundVehicle)
        .filter(FundVehicle.management_company_id == firm_id)
        .order_by(FundVehicle.vintage_year.desc())
        .all()
    )


@router.get("/{firm_id}/portfolio", response_model=list[PortfolioCompanyResponse])
def get_firm_portfolio(
    firm_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(PortfolioCompany)
        .filter(PortfolioCompany.management_company_id == firm_id)
        .order_by(PortfolioCompany.name)
        .all()
    )
