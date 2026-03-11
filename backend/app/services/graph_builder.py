from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.firm import ManagementCompany, FundVehicle
from app.models.individual import Individual
from app.models.role import Role
from app.models.lp_commitment import LPCommitment
from app.models.enums import FirmType, TherapeuticArea
from app.schemas.graph import GraphNode, GraphLink, GraphData


def build_network_graph(
    db: Session,
    firm_type: FirmType | None = None,
    therapeutic_area: TherapeuticArea | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    lp_committed_only: bool = False,
) -> GraphData:
    # Get LP-committed fund vehicle IDs -> management company IDs
    lp_mgmt_co_ids: set[UUID] = set()
    lp_fund_ids = {
        row.fund_vehicle_id
        for row in db.query(LPCommitment.fund_vehicle_id).all()
    }
    if lp_fund_ids:
        lp_mgmt_cos = (
            db.query(FundVehicle.management_company_id)
            .filter(FundVehicle.id.in_(lp_fund_ids))
            .all()
        )
        lp_mgmt_co_ids = {row.management_company_id for row in lp_mgmt_cos}

    # Query firms
    firm_query = db.query(ManagementCompany)
    if firm_type:
        firm_query = firm_query.filter(ManagementCompany.firm_type == firm_type)
    if lp_committed_only:
        firm_query = firm_query.filter(ManagementCompany.id.in_(lp_mgmt_co_ids))
    firms = firm_query.all()
    firm_ids = {f.id for f in firms}

    # Query roles (links between individuals and firms)
    role_query = db.query(Role).filter(Role.management_company_id.in_(firm_ids))
    if from_date:
        role_query = role_query.filter(
            (Role.end_date >= from_date) | (Role.end_date.is_(None))
        )
    if to_date:
        role_query = role_query.filter(
            (Role.start_date <= to_date) | (Role.start_date.is_(None))
        )
    roles = role_query.all()

    # Collect individual IDs from roles
    individual_ids = {r.individual_id for r in roles}

    # Query individuals
    ind_query = db.query(Individual).filter(Individual.id.in_(individual_ids))
    if therapeutic_area:
        ind_query = ind_query.filter(
            Individual.primary_therapeutic_area == therapeutic_area
        )
    individuals = ind_query.all()
    valid_individual_ids = {i.id for i in individuals}

    # Build nodes
    nodes: list[GraphNode] = []
    for firm in firms:
        nodes.append(
            GraphNode(
                id=f"firm-{firm.id}",
                name=firm.name,
                type="firm",
                firm_type=firm.firm_type.value if firm.firm_type else None,
                has_lp_commitment=firm.id in lp_mgmt_co_ids,
                val=max(
                    1,
                    len([r for r in roles if r.management_company_id == firm.id and r.is_current]),
                ),
            )
        )

    for ind in individuals:
        nodes.append(
            GraphNode(
                id=f"person-{ind.id}",
                name=f"{ind.first_name} {ind.last_name}",
                type="person",
                therapeutic_area=(
                    ind.primary_therapeutic_area.value
                    if ind.primary_therapeutic_area
                    else None
                ),
                val=1,
            )
        )

    # Build links
    links: list[GraphLink] = []
    for role in roles:
        if role.individual_id not in valid_individual_ids:
            continue
        if role.management_company_id not in firm_ids:
            continue
        links.append(
            GraphLink(
                source=f"person-{role.individual_id}",
                target=f"firm-{role.management_company_id}",
                is_current=role.is_current,
                title=role.title,
            )
        )

    return GraphData(nodes=nodes, links=links)
