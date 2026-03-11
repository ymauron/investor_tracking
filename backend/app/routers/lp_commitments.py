from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.lp_commitment import LPCommitment
from app.schemas.lp_commitment import (
    LPCommitmentCreate,
    LPCommitmentUpdate,
    LPCommitmentResponse,
)

router = APIRouter()


@router.get("/", response_model=list[LPCommitmentResponse])
def list_lp_commitments(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return db.query(LPCommitment).all()


@router.post("/", response_model=LPCommitmentResponse, status_code=201)
def create_lp_commitment(
    data: LPCommitmentCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    commitment = LPCommitment(**data.model_dump())
    db.add(commitment)
    db.commit()
    db.refresh(commitment)
    return commitment


@router.put("/{commitment_id}", response_model=LPCommitmentResponse)
def update_lp_commitment(
    commitment_id: UUID,
    data: LPCommitmentUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    commitment = db.query(LPCommitment).filter(LPCommitment.id == commitment_id).first()
    if not commitment:
        raise HTTPException(status_code=404, detail="LP commitment not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(commitment, key, value)
    db.commit()
    db.refresh(commitment)
    return commitment


@router.delete("/{commitment_id}", status_code=204)
def delete_lp_commitment(
    commitment_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    commitment = db.query(LPCommitment).filter(LPCommitment.id == commitment_id).first()
    if not commitment:
        raise HTTPException(status_code=404, detail="LP commitment not found")
    db.delete(commitment)
    db.commit()
