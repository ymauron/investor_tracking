from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.enums import FirmType, TherapeuticArea
from app.schemas.graph import GraphData, TimelineData
from app.services.graph_builder import build_network_graph
from app.services.timeline import build_timeline_data

router = APIRouter()


@router.get("/network", response_model=GraphData)
def get_network_graph(
    firm_type: FirmType | None = None,
    therapeutic_area: TherapeuticArea | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    lp_committed_only: bool = False,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return build_network_graph(
        db,
        firm_type=firm_type,
        therapeutic_area=therapeutic_area,
        from_date=from_date,
        to_date=to_date,
        lp_committed_only=lp_committed_only,
    )


@router.get("/timeline", response_model=TimelineData)
def get_timeline(
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return build_timeline_data(db, from_date=from_date, to_date=to_date)
