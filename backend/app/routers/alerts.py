from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.alert import AlertRule, AlertNotification
from app.schemas.alert import (
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertRuleResponse,
    AlertNotificationResponse,
    UnreadCountResponse,
)

router = APIRouter()


# --- Alert Rules ---


@router.get("/rules", response_model=list[AlertRuleResponse])
def list_alert_rules(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return db.query(AlertRule).order_by(AlertRule.created_at.desc()).all()


@router.post("/rules", response_model=AlertRuleResponse, status_code=201)
def create_alert_rule(
    data: AlertRuleCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    rule = AlertRule(**data.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.put("/rules/{rule_id}", response_model=AlertRuleResponse)
def update_alert_rule(
    rule_id: UUID,
    data: AlertRuleUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/rules/{rule_id}", status_code=204)
def delete_alert_rule(
    rule_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    db.delete(rule)
    db.commit()


# --- Notifications ---


@router.get("/notifications/count", response_model=UnreadCountResponse)
def unread_count(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    count = (
        db.query(AlertNotification)
        .filter(AlertNotification.is_read.is_(False))
        .count()
    )
    return UnreadCountResponse(count=count)


@router.get("/notifications", response_model=list[AlertNotificationResponse])
def list_notifications(
    unread_only: bool = False,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = (
        db.query(AlertNotification)
        .options(
            joinedload(AlertNotification.transaction),
            joinedload(AlertNotification.alert_rule),
        )
    )
    if unread_only:
        query = query.filter(AlertNotification.is_read.is_(False))

    notifs = (
        query.order_by(AlertNotification.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return [
        AlertNotificationResponse(
            id=n.id,
            transaction_id=n.transaction_id,
            alert_rule_id=n.alert_rule_id,
            is_read=n.is_read,
            created_at=n.created_at,
            transaction=n.transaction,
            alert_rule_name=n.alert_rule.name,
        )
        for n in notifs
    ]


@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    notif = db.query(AlertNotification).filter(AlertNotification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    return {"ok": True}


@router.put("/notifications/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    db.query(AlertNotification).filter(
        AlertNotification.is_read.is_(False)
    ).update({"is_read": True})
    db.commit()
    return {"ok": True}
