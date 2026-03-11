from datetime import date

from sqlalchemy.orm import Session, joinedload

from app.models.movement import MovementEvent
from app.models.role import Role
from app.models.firm import ManagementCompany
from app.models.individual import Individual
from app.schemas.graph import TimelineEvent, TimelineData


def build_timeline_data(
    db: Session,
    from_date: date | None = None,
    to_date: date | None = None,
) -> TimelineData:
    query = (
        db.query(MovementEvent)
        .join(Individual, MovementEvent.individual_id == Individual.id)
        .options(
            joinedload(MovementEvent.individual),
            joinedload(MovementEvent.origin_role).joinedload(Role.management_company),
            joinedload(MovementEvent.destination_role).joinedload(Role.management_company),
            joinedload(MovementEvent.tags),
        )
    )
    if from_date:
        query = query.filter(
            (MovementEvent.joining_date >= from_date)
            | (MovementEvent.departure_date >= from_date)
        )
    if to_date:
        query = query.filter(
            (MovementEvent.joining_date <= to_date)
            | (MovementEvent.departure_date <= to_date)
        )
    events = query.order_by(MovementEvent.joining_date.desc()).all()

    timeline_events: list[TimelineEvent] = []
    for e in events:
        event_date = e.joining_date or e.departure_date
        if not event_date:
            continue

        origin_firm = None
        origin_title = None
        if e.origin_role:
            origin_title = e.origin_role.title
            if e.origin_role.management_company:
                origin_firm = e.origin_role.management_company.name

        dest_firm = None
        dest_title = None
        if e.destination_role:
            dest_title = e.destination_role.title
            if e.destination_role.management_company:
                dest_firm = e.destination_role.management_company.name

        timeline_events.append(
            TimelineEvent(
                id=str(e.id),
                individual_id=str(e.individual_id),
                individual_name=f"{e.individual.first_name} {e.individual.last_name}",
                date=event_date.isoformat(),
                origin_firm=origin_firm,
                destination_firm=dest_firm,
                origin_title=origin_title,
                destination_title=dest_title,
                move_type=e.move_type.value,
                is_spinout=e.is_spinout,
                tags=[t.tag for t in e.tags],
            )
        )

    return TimelineData(events=timeline_events)
