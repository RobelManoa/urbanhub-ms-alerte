import json
import os

import pika
from pika.exceptions import AMQPConnectionError

from src.ports.publisher_port import PublisherPort


class RabbitMQPublisher(PublisherPort):
    """Publish analysis outputs to RabbitMQ channels."""

    def __init__(self) -> None:
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.publishable_channels = {
            "alert_queue",
            "analysis.user.notification",
            "log.events",
            "analysis.traffic.kpi",
        }

    def publish(self, analysis_result: dict) -> None:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.rabbitmq_host)
            )
        except (AMQPConnectionError, OSError) as exc:
            print(
                f"RabbitMQ indisponible sur '{self.rabbitmq_host}': {exc}. "
                "Impossible de publier les sorties d'analyse."
            )
            return

        channel = connection.channel()
        for output in analysis_result.get("outputs", []):
            routing_key = output.get("channel")
            if routing_key not in self.publishable_channels:
                continue

            channel.queue_declare(queue=routing_key)
            channel.basic_publish(
                exchange="",
                routing_key=routing_key,
                body=json.dumps(output["payload"]),
            )

        connection.close()
