# src/adapters/database/repository.py

from src.ports.repository_port import AlertRepositoryPort
from src.adapters.database.models import Alert as AlertModel, Notification, User
from sqlalchemy.orm import Session


class SQLAlchemyAlertRepository(AlertRepositoryPort):

    def __init__(self, session: Session):
        self.session = session

    def save_alert(self, alert):
        db_alert = AlertModel(
            type=alert.type,
            message=alert.message,
            severity=alert.severity,
            source=alert.source
        )
        self.session.add(db_alert)
        self.session.commit()

    def get_users_to_notify(self, alert):
        return self.session.query(User).all()

    def save_notification(self, notification_data: dict):
        notif = Notification(**notification_data)
        self.session.add(notif)
        self.session.commit()