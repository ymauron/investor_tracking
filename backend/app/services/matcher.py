import re
from difflib import SequenceMatcher
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.firm import ManagementCompany, PortfolioCompany

STRIP_SUFFIXES = re.compile(
    r"\b(inc\.?|llc|corp\.?|corporation|ltd\.?|limited|therapeutics|"
    r"biosciences|pharmaceuticals|pharma|bio|sciences|biotech|"
    r"holdings|group|partners|capital|ventures|management)\b",
    re.IGNORECASE,
)

MATCH_THRESHOLD = 0.80

_mgmt_cache: list[tuple[UUID, str, str]] | None = None
_portco_cache: list[tuple[UUID, str, str]] | None = None


def normalize(name: str) -> str:
    cleaned = STRIP_SUFFIXES.sub("", name.lower())
    cleaned = re.sub(r"[^\w\s]", "", cleaned)
    return " ".join(cleaned.split())


def _load_mgmt_cache(db: Session) -> list[tuple[UUID, str, str]]:
    global _mgmt_cache
    if _mgmt_cache is None:
        companies = db.query(ManagementCompany.id, ManagementCompany.name).all()
        _mgmt_cache = [(c.id, c.name, normalize(c.name)) for c in companies]
    return _mgmt_cache


def _load_portco_cache(db: Session) -> list[tuple[UUID, str, str]]:
    global _portco_cache
    if _portco_cache is None:
        companies = db.query(PortfolioCompany.id, PortfolioCompany.name).all()
        _portco_cache = [(c.id, c.name, normalize(c.name)) for c in companies]
    return _portco_cache


def clear_cache():
    global _mgmt_cache, _portco_cache
    _mgmt_cache = None
    _portco_cache = None


def _best_match(
    names: list[str], cache: list[tuple[UUID, str, str]]
) -> UUID | None:
    best_id = None
    best_score = 0.0

    for raw_name in names:
        norm = normalize(raw_name)
        if not norm:
            continue
        for entity_id, _, entity_norm in cache:
            if not entity_norm:
                continue
            if norm in entity_norm or entity_norm in norm:
                return entity_id
            score = SequenceMatcher(None, norm, entity_norm).ratio()
            if score > best_score:
                best_score = score
                best_id = entity_id

    if best_score >= MATCH_THRESHOLD:
        return best_id
    return None


def match_to_management_company(db: Session, names: list[str]) -> UUID | None:
    if not names:
        return None
    cache = _load_mgmt_cache(db)
    return _best_match(names, cache)


def match_to_portfolio_company(db: Session, names: list[str]) -> UUID | None:
    if not names:
        return None
    cache = _load_portco_cache(db)
    return _best_match(names, cache)
