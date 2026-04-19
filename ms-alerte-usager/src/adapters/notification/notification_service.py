# src/adapters/notification/notification_service.py

from src.ports.notification_port import NotificationPort


class NotificationService(NotificationPort):

    def send(self, alert, channel: str, destination: str):
        print(f"[{channel.upper()}] Sending '{alert.message}' to {destination}")