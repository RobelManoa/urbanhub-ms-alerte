import os
import sys
from pathlib import Path

from pymongo import MongoClient

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.adapters.database.repository import MongoIoTRepository
from src.adapters.rabbitmq.consumer import RabbitMQConsumer
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.normalize_iot_data_usecase import NormalizeIoTDataUseCase

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "urbanhub")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "iot_collecte")


def main():
    """Initialise les dependances du service puis demarre le consumer.

    Returns:
        None
    """
    mongo_client = MongoClient(MONGODB_URI)
    collection = mongo_client[MONGODB_DATABASE][MONGODB_COLLECTION]

    repository = MongoIoTRepository(collection)
    publisher = RabbitMQPublisher()
    use_case = NormalizeIoTDataUseCase(repository, publisher)
    consumer = RabbitMQConsumer(use_case)

    consumer.start_consuming()


if __name__ == "__main__":
    main()
