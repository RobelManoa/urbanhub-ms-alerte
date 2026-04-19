# src/application/process_alert_usecase.py

from src.ports.notification_port import NotificationPort
from src.ports.repository_port import AlertRepositoryPort
from src.domain.entities import Alert


class ProcessAlertUseCase:

    def __init__(
        self,
        notification_port: NotificationPort,
        repository: AlertRepositoryPort
    ):
        self.notification_port = notification_port
        self.repository = repository

    def execute(self, alert: Alert):
        # Sauvegarde de l'alerte
        self.repository.save_alert(alert)

        # Récupérer les utilisateurs concernés
        users = self.repository.get_users_to_notify(alert)

        # Envoyer notifications
        for user in users:
            if user.email:
                self.notification_port.send(alert, "email", user.email)

            if user.phone:
                self.notification_port.send(alert, "sms", user.phone)