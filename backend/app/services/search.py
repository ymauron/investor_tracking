from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.individual import Individual
from app.models.firm import ManagementCompany
from app.models.deal import Deal
from app.models.transaction import Transaction


def global_search(db: Session, query: str, limit: int = 20) -> dict:
    pattern = f"%{query}%"

    individuals = (
        db.query(Individual)
        .filter(
            or_(
                Individual.first_name.ilike(pattern),
                Individual.last_name.ilike(pattern),
                Individual.email.ilike(pattern),
            )
        )
        .limit(limit)
        .all()
    )

    firms = (
        db.query(ManagementCompany)
        .filter(ManagementCompany.name.ilike(pattern))
        .limit(limit)
        .all()
    )

    deals = (
        db.query(Deal)
        .filter(Deal.name.ilike(pattern))
        .limit(limit)
        .all()
    )

    return {
        "individuals": [
            {
                "id": str(i.id),
                "type": "individual",
                "name": f"{i.first_name} {i.last_name}",
                "detail": i.primary_therapeutic_area.value if i.primary_therapeutic_area else None,
            }
            for i in individuals
        ],
        "firms": [
            {
                "id": str(f.id),
                "type": "firm",
                "name": f.name,
                "detail": f.firm_type.value if f.firm_type else None,
            }
            for f in firms
        ],
        "deals": [
            {
                "id": str(d.id),
                "type": "deal",
                "name": d.name,
                "detail": d.deal_type,
            }
            for d in deals
        ],
        "transactions": [
            {
                "id": str(t.id),
                "type": "transaction",
                "name": t.title,
                "detail": t.transaction_type.value if t.transaction_type else None,
            }
            for t in db.query(Transaction)
            .filter(Transaction.title.ilike(pattern))
            .limit(limit)
            .all()
        ],
    }
