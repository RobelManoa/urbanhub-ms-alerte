import json
from unittest.mock import Mock

import pika
import pytest
from pika.exceptions import AMQPConnectionError

from src.adapters.rabbitmq.consumer import RabbitMQConsumer
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.normalize_iot_data_usecase import NormalizeIoTDataUseCase
from src.domain.entities import NormalizedIoTWindow, NormalizedVehicle


def test_normalized_window_to_dict_with_multiple_vehicles():
    payload = NormalizedIoTWindow(
        sensor_id="sensor-9",
        zone_id="zone-Z",
        window_start="2026-04-11T10:00:00Z",
        window_end="2026-04-11T10:00:15Z",
        vehicles=[
            NormalizedVehicle(speed_kmh=12, vehicle_type="car"),
            NormalizedVehicle(speed_kmh=32, vehicle_type="bus"),
        ],
        vehicle_count=2,
    )

    assert payload.to_dict() == {
        "sensorId": "sensor-9",
        "zoneId": "zone-Z",
        "windowStart": "2026-04-11T10:00:00Z",
        "windowEnd": "2026-04-11T10:00:15Z",
        "vehicles": [
            {"speedKmh": 12, "vehicleType": "car"},
            {"speedKmh": 32, "vehicleType": "bus"},
        ],
        "vehicleCount": 2,
    }


def test_parse_speed_extracts_number_and_returns_none_when_missing():
    assert NormalizeIoTDataUseCase._parse_speed("105km/h") == 105
    assert NormalizeIoTDataUseCase._parse_speed(None) is None


def test_format_timestamp_raises_value_error_for_invalid_date():
    with pytest.raises(ValueError):
        NormalizeIoTDataUseCase._format_timestamp("invalid-date")


def test_consumer_callback_raises_for_invalid_json():
    consumer = RabbitMQConsumer(Mock())

    with pytest.raises(json.JSONDecodeError):
        consumer.callback(None, None, None, b"{invalid json")


def test_publisher_handles_connection_error_and_does_not_raise(monkeypatch, capsys):
    publisher = RabbitMQPublisher()

    def fake_blocking_connection(_):
        raise AMQPConnectionError("cannot connect")

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

    output = capsys.readouterr().out
    assert "RabbitMQ indisponible" in output


def test_publisher_handles_os_error_and_does_not_raise(monkeypatch, capsys):
    publisher = RabbitMQPublisher()

    def fake_blocking_connection(_):
        raise OSError("network error")

    monkeypatch.setattr(pika, "BlockingConnection", fake_blocking_connection)

    payload = NormalizedIoTWindow(
        sensor_id="sensor-1",
        zone_id="zone-A",
        window_start="2026-04-11T10:00:00Z",
        window_end="2026-04-11T10:00:15Z",
        vehicles=[],
        vehicle_count=0,
    )

    publisher.publish(payload)

    output = capsys.readouterr().out
    assert "Impossible de publier le message normalise." in output
