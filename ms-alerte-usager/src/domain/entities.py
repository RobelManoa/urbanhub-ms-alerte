# src/domain/entities.py

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alert:
    type: str
    message: str
    severity: str
    source: str
    created_at: datetime = datetime.utcnow()