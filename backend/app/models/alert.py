import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.database import Base
from app.models.enums import TherapeuticArea, TransactionType


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    therapeutic_area: Mapped[TherapeuticArea | None] = mapped_column(
        ENUM(TherapeuticArea, name="therapeutic_area", create_type=True)
    )
    transaction_type: Mapped[TransactionType | None] = mapped_column(
        ENUM(TransactionType, name="transaction_type", create_type=True)
    )
    keyword: Mapped[str | None] = mapped_column(String(200))
    company_name: Mapped[str | None] = mapped_column(String(300))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    notifications: Mapped[list["AlertNotification"]] = relationship(
        back_populates="alert_rule", cascade="all, delete-orphan"
    )


class AlertNotification(Base):
    __tablename__ = "alert_notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
    )
    alert_rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("alert_rules.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    transaction: Mapped["Transaction"] = relationship()  # noqa: F821
    alert_rule: Mapped["AlertRule"] = relationship(back_populates="notifications")

    __table_args__ = (
        Index("ix_alert_notif_transaction", "transaction_id"),
        Index("ix_alert_notif_rule", "alert_rule_id"),
        Index("ix_alert_notif_unread", "is_read"),
    )
