# src/ports/repository_port.py

from abc import ABC, abstractmethod
from src.domain.entities import Alert


class AlertRepositoryPort(ABC):

    @abstractmethod
    def save_alert(self, alert: Alert):
        pass

    @abstractmethod
    def get_users_to_notify(self, alert: Alert):
        pass

    @abstractmethod
    def save_notification(self, notification_data: dict):
        pass