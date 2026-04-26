import json
import os

import pika
from pika.exceptions import AMQPConnectionError

from src.domain.entities import RawIoTWindow, RawVehicleRecord
from src.ports.event_consumer_port import EventConsumerPort
from src.application.normalize_iot_data_usecase import NormalizeIoTDataUseCase


class RabbitMQConsumer(EventConsumerPort):
    """Consomme les donnees IoT brutes depuis RabbitMQ."""

    def __init__(self, use_case: NormalizeIoTDataUseCase):
        """Prepare le consumer avec son cas d'usage et sa file d'entree.

        Args:
            use_case (NormalizeIoTDataUseCase): Cas d'usage qui transforme,
                stocke et republie les donnees.

        Returns:
            None
        """
        self.use_case = use_case
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.queue_name = os.getenv("RABBITMQ_INPUT_QUEUE", "iot_raw_queue")

    def callback(self, ch, method, properties, body):
        """Convertit le message brut en objet domaine puis lance le traitement.

        Args:
            ch: Canal RabbitMQ fourni par Pika.
            method: Metadonnees du message RabbitMQ.
            properties: Proprietes AMQP du message.
            body (bytes): Contenu JSON du message brut.

        Returns:
            None

        Raises:
            json.JSONDecodeError: Si le message n'est pas un JSON valide.
            ValueError: Si les dates contenues dans le message ne peuvent pas
                etre converties par le cas d'usage.
        """
        data = json.loads(body)
        payload = RawIoTWindow(
            sensor_id=data.get("id", ""),
            location=data.get("loc", ""),
            started_at=data.get("ts-d", ""),
            ended_at=data.get("ts-e", ""),
            data=[
                RawVehicleRecord(
                    speed=item.get("spd", ""),
                    vehicle_type=item.get("veh", ""),
                )
                for item in data.get("data", [])
            ],
        )
        self.use_case.execute(payload)

    def start_consuming(self):
        """Ouvre la connexion RabbitMQ et ecoute la file des donnees brutes.

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
                "Definis RABBITMQ_HOST ou demarre RabbitMQ puis relance."
            )
            return

        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True,
        )

        print("Waiting for IoT messages...")
        channel.start_consuming()
