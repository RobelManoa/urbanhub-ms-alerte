# src/ports/notification_port.py

from abc import ABC, abstractmethod
from src.domain.entities import Alert


class NotificationPort(ABC):

    @abstractmethod
    def send(self, alert: Alert, channel: str, destination: str):
        pass