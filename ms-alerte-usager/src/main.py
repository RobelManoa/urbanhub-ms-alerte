# ms-alerte-usager/src/main.py
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# === Configuration du PYTHONPATH ===
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.adapters.database.repository import SQLAlchemyAlertRepository
from src.adapters.database.models import Base
from src.adapters.notification.notification_service import NotificationService
from src.application.process_alert_usecase import ProcessAlertUseCase
from src.adapters.rabbitmq.consumer import RabbitMQConsumer

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/alerts")

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    repository = SQLAlchemyAlertRepository(session)
    notification_service = NotificationService()
    use_case = ProcessAlertUseCase(notification_service, repository)
    consumer = RabbitMQConsumer(use_case)

    consumer.start_consuming()