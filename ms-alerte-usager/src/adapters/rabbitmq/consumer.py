# src/adapters/rabbitmq/consumer.py

import json
import os
import pika
from pika.exceptions import AMQPConnectionError
from src.domain.entities import Alert
from src.application.process_alert_usecase import ProcessAlertUseCase


class RabbitMQConsumer:

    def __init__(self, use_case: ProcessAlertUseCase):
        self.use_case = use_case
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.queue_name = os.getenv("RABBITMQ_QUEUE", "alert_queue")

    def callback(self, ch, method, properties, body):
        data = json.loads(body)

        alert = Alert(
            type=data.get("type"),
            message=data.get("message"),
            severity=data.get("severity"),
            source=data.get("source")
        )

        self.use_case.execute(alert)

    def start_consuming(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.rabbitmq_host)
            )
        except (AMQPConnectionError, OSError) as exc:
            print(
                f"RabbitMQ indisponible sur '{self.rabbitmq_host}': {exc}. "
                "Definis RABBITMQ_HOST ou demarre RabbitMQ puis relance."
            )
            return

        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name)

        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )

        print("Waiting for messages...")
        channel.start_consuming()