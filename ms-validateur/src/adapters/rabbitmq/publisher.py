import json
import os

import pika
from pika.exceptions import AMQPConnectionError

from src.domain.entities import ValidationResult
from src.ports.publisher_port import PublisherPort


class RabbitMQPublisher(PublisherPort):
    def __init__(self) -> None:
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.queue_name = os.getenv("RABBITMQ_OUTPUT_QUEUE", "validated_queue")

    def publish(self, validation_result: ValidationResult) -> None:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        except (AMQPConnectionError, OSError) as exc:
            print(
                f"RabbitMQ indisponible sur '{self.rabbitmq_host}': {exc}. "
                "Impossible de publier les donnees validees."
            )
            return

        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(validation_result.to_dict()),
        )
        connection.close()