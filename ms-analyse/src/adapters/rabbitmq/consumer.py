import json
import os
from datetime import datetime

import pika
from pika.exceptions import AMQPConnectionError

from src.application.use_cases.analyze_traffic_use_case import AnalyzeTrafficUseCase
from src.domain.entities import TrafficWindow, VehicleReading


class RabbitMQConsumer:
    """Consume normalized traffic windows published by ms-collecte-iot."""

    def __init__(self, use_case: AnalyzeTrafficUseCase) -> None:
        self.use_case = use_case
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.queue_name = os.getenv("RABBITMQ_INPUT_QUEUE", "collecte_queue")

    def callback(self, ch, method, properties, body) -> None:
        data = json.loads(body)
        payload = TrafficWindow(
            sensor_id=data.get("sensorId", ""),
            zone_id=data.get("zoneId", ""),
            window_start=datetime.fromisoformat(
                data.get("windowStart", "").replace("Z", "+00:00")
            ),
            window_end=datetime.fromisoformat(
                data.get("windowEnd", "").replace("Z", "+00:00")
            ),
            vehicles=[
                VehicleReading(
                    speed_kmh=item.get("speedKmh", 0),
                    vehicle_type=item.get("vehicleType", ""),
                )
                for item in data.get("vehicles", [])
            ],
            vehicle_count=data.get("vehicleCount", 0),
        )
        self.use_case.execute(payload)

    def start_consuming(self) -> None:
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

        print("Waiting for traffic messages...")
        channel.start_consuming()
