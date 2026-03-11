from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.auth import hash_password
from app.config import settings
from app.database import SessionLocal, engine, Base
from app.models import *  # noqa: F401,F403 — ensure all models are registered
from app.models.user import User
from app.routers import (
    auth,
    individuals,
    firms,
    funds,
    portfolio_companies,
    roles,
    movements,
    deals,
    lp_commitments,
    notes,
    graph,
    search,
)


def seed_admin_user():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == settings.admin_username).first()
        if not existing:
            admin = User(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_password),
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_admin_user()
    yield


app = FastAPI(
    title="Investor Tracking",
    description="Healthcare investor movement tracking application",
    version="0.1.0",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(individuals.router, prefix="/api/v1/individuals", tags=["individuals"])
app.include_router(firms.router, prefix="/api/v1/firms", tags=["firms"])
app.include_router(funds.router, prefix="/api/v1/funds", tags=["funds"])
app.include_router(
    portfolio_companies.router,
    prefix="/api/v1/portfolio-companies",
    tags=["portfolio-companies"],
)
app.include_router(roles.router, prefix="/api/v1/roles", tags=["roles"])
app.include_router(movements.router, prefix="/api/v1/movements", tags=["movements"])
app.include_router(deals.router, prefix="/api/v1/deals", tags=["deals"])
app.include_router(
    lp_commitments.router, prefix="/api/v1/lp-commitments", tags=["lp-commitments"]
)
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["graph"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
