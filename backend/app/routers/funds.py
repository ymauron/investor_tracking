from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.firm import FundVehicle
from app.models.lp_commitment import LPCommitment
from app.schemas.firm import FundVehicleCreate, FundVehicleUpdate, FundVehicleResponse
from app.schemas.lp_commitment import LPCommitmentResponse

router = APIRouter()


@router.get("/", response_model=list[FundVehicleResponse])
def list_funds(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return db.query(FundVehicle).order_by(FundVehicle.vintage_year.desc()).all()


@router.get("/{fund_id}", response_model=FundVehicleResponse)
def get_fund(
    fund_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    fund = db.query(FundVehicle).filter(FundVehicle.id == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund


@router.post("/", response_model=FundVehicleResponse, status_code=201)
def create_fund(
    data: FundVehicleCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    fund = FundVehicle(**data.model_dump())
    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund


@router.put("/{fund_id}", response_model=FundVehicleResponse)
def update_fund(
    fund_id: UUID,
    data: FundVehicleUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    fund = db.query(FundVehicle).filter(FundVehicle.id == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(fund, key, value)
    db.commit()
    db.refresh(fund)
    return fund


@router.delete("/{fund_id}", status_code=204)
def delete_fund(
    fund_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    fund = db.query(FundVehicle).filter(FundVehicle.id == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    db.delete(fund)
    db.commit()


@router.get("/{fund_id}/lp-status", response_model=list[LPCommitmentResponse])
def get_fund_lp_status(
    fund_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(LPCommitment)
        .filter(LPCommitment.fund_vehicle_id == fund_id)
        .all()
    )
