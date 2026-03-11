import logging

from sqlalchemy.orm import Session

from app.models.alert import AlertRule, AlertNotification
from app.models.transaction import Transaction

logger = logging.getLogger(__name__)


def check_alerts(db: Session, transaction: Transaction) -> list[AlertNotification]:
    rules = db.query(AlertRule).filter(AlertRule.is_active.is_(True)).all()
    notifications = []

    for rule in rules:
        if not _matches_rule(rule, transaction):
            continue

        notif = AlertNotification(
            transaction_id=transaction.id,
            alert_rule_id=rule.id,
            is_read=False,
        )
        db.add(notif)
        notifications.append(notif)

    return notifications


def _matches_rule(rule: AlertRule, txn: Transaction) -> bool:
    if rule.therapeutic_area and txn.therapeutic_area != rule.therapeutic_area:
        return False

    if rule.transaction_type and txn.transaction_type != rule.transaction_type:
        return False

    if rule.keyword:
        keyword_lower = rule.keyword.lower()
        text = f"{txn.title} {txn.raw_description or ''}".lower()
        if keyword_lower not in text:
            return False

    if rule.company_name:
        company_lower = rule.company_name.lower()
        mentioned = txn.companies_mentioned or []
        if not any(company_lower in c.lower() for c in mentioned):
            title_desc = f"{txn.title} {txn.raw_description or ''}".lower()
            if company_lower not in title_desc:
                return False

    return True
