import json
from unittest.mock import Mock

import pika

from src.adapters.database.repository import MongoIoTRepository
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.domain.entities import NormalizedIoTWindow, NormalizedVehicle


def test_repository_save_inserts_normalized_document():
    collection = Mock()
    repository = MongoIoTRepository(collection)
    payload = NormalizedIoTWindow(
        sensor_id="sensor-1",
        zone_id="zone-A",
        window_start="2026-04-11T10:00:00Z",
        window_end="2026-04-11T10:00:15Z",
        vehicles=[NormalizedVehicle(speed_kmh=45, vehicle_type="car")],
        vehicle_count=1,
    )

    repository.save(payload)

    collection.insert_one.assert_called_once_with(
        {
            "sensorId": "sensor-1",
            "zoneId": "zone-A",
            "windowStart": "2026-04-11T10:00:00Z",
            "windowEnd": "2026-04-11T10:00:15Z",
            "vehicles": [{"speedKmh": 45, "vehicleType": "car"}],
            "vehicleCount": 1,
        }
    )


def test_publisher_declares_queue_and_publishes_json(monkeypatch):
    publisher = RabbitMQPublisher()
    fake_channel = Mock()
    fake_connection = Mock()
    fake_connection.channel.return_value = fake_channel

    captured = {}

    def fake_connection_parameters(host):
        captured["host"] = host
        return "params"

    def fake_blocking_connection(params):
        captured["params"] = params
        return fake_connection

    monkeypatch.setattr(pika, "ConnectionParameters", fake_connection_parameters)
    monkeypatch.setattr(pika, "BlockingConnection", fake_blocking_connection)

    payload = NormalizedIoTWindow(
        sensor_id="sensor-1",
        zone_id="zone-A",
        window_start="2026-04-11T10:00:00Z",
        window_end="2026-04-11T10:00:15Z",
        vehicles=[NormalizedVehicle(speed_kmh=45, vehicle_type="car")],
        vehicle_count=1,
    )

    publisher.publish(payload)

    assert captured["host"] == publisher.rabbitmq_host
    assert captured["params"] == "params"
    fake_channel.queue_declare.assert_called_once_with(queue=publisher.queue_name)
    fake_channel.basic_publish.assert_called_once_with(
        exchange="",
        routing_key=publisher.queue_name,
        body=json.dumps(payload.to_dict()),
    )
    fake_connection.close.assert_called_once_with()
