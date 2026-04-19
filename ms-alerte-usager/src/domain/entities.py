# src/domain/entities.py

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Alert:
    type: str
    message: str
    severity: str
    source: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))