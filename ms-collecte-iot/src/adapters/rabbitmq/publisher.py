import json
import os

import pika
from pika.exceptions import AMQPConnectionError

from src.domain.entities import NormalizedIoTWindow
from src.ports.publisher_port import PublisherPort


class RabbitMQPublisher(PublisherPort):
    """Publie les donnees normalisees vers RabbitMQ."""

    def __init__(self):
        """Prepare la connexion logique et la file de sortie cible.

        Returns:
            None
        """
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.queue_name = os.getenv("RABBITMQ_OUTPUT_QUEUE", "collecte_queue")

    def publish(self, payload: NormalizedIoTWindow):
        """Publie un document normalise sur la file RabbitMQ de collecte.

        Args:
            payload (NormalizedIoTWindow): Document normalise a republier.

        Returns:
            None
        """
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.rabbitmq_host)
            )
        except (AMQPConnectionError, OSError) as exc:
            print(
                f"RabbitMQ indisponible sur '{self.rabbitmq_host}': {exc}. "
                "Impossible de publier le message normalise."
            )
            return

        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(payload.to_dict()),
        )
        connection.close()
