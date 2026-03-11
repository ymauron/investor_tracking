from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.services.search import global_search

router = APIRouter()


@router.get("/")
def search(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return global_search(db, q)
