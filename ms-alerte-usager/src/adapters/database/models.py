# src/adapters/database/models.py

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid
from datetime import datetime
import enum

Base = declarative_base()


# -------------------------
# ENUMS (bonne pratique)
# -------------------------

class SeverityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ChannelEnum(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class StatusEnum(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


# -------------------------
# USER
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    notifications = relationship("Notification", back_populates="user")


# -------------------------
# ALERT
# -------------------------

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(Enum(SeverityEnum), nullable=False)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    notifications = relationship("Notification", back_populates="alert")


# -------------------------
# NOTIFICATION
# -------------------------

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    channel = Column(Enum(ChannelEnum), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    sent_at = Column(DateTime, nullable=True)

    alert = relationship("Alert", back_populates="notifications")
    user = relationship("User", back_populates="notifications")


# -------------------------
# EVENT LOG (audit 🔥)
# -------------------------

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)