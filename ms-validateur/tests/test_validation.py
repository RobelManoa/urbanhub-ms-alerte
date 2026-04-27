import json
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from datetime import datetime, timezone

from src.adapters.rabbitmq.consumer import RabbitMQConsumer
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.validate_traffic_use_case import ValidateTrafficUseCase
from src.domain.entities import TrafficWindow, VehicleReading
from src.domain.sensor_validation import SensorValidationService
from src.domain.services import TrafficValidationService
from src.main import app


def _build_window(vehicle_count: int = 3) -> TrafficWindow:
    window_start = datetime(2026, 4, 11, 10, 0, 0, tzinfo=timezone.utc)
    window_end = datetime(2026, 4, 11, 10, 0, 15, tzinfo=timezone.utc)
    return TrafficWindow(
        sensor_id="sensor-1",
        zone_id="zone-A",
        window_start=window_start,
        window_end=window_end,
        vehicles=[
            VehicleReading(speed_kmh=45, vehicle_type="car"),
            VehicleReading(speed_kmh=40, vehicle_type="truck"),
            VehicleReading(speed_kmh=20, vehicle_type="car"),
        ][:vehicle_count],
        vehicle_count=vehicle_count,
    )


def test_healthcheck_returns_ok() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_validation_service_classifies_traffic() -> None:
    service = TrafficValidationService()
    result = service.validate(_build_window())

    assert result.accepted is True
    assert result.traffic_class == "medium"
    assert result.quality_score == 80
    assert result.to_dict()["validation"]["status"] == "accepted"


def test_use_case_does_not_publish_invalid_payload() -> None:
    service = TrafficValidationService()
    publisher = Mock()
    window = TrafficWindow(
        sensor_id="sensor-2",
        zone_id="zone-B",
        window_start=datetime(2026, 4, 11, 10, 0, 15, tzinfo=timezone.utc),
        window_end=datetime(2026, 4, 11, 10, 0, 0, tzinfo=timezone.utc),
        vehicles=[VehicleReading(speed_kmh=20, vehicle_type="car")],
        vehicle_count=2,
    )

    result = service.validate(window)

    assert result.accepted is False
    assert any("windowEnd" in issue for issue in result.issues)
    publisher.publish.assert_not_called()


def test_validate_endpoint_returns_enriched_payload() -> None:
    fake_result = TrafficValidationService().validate(_build_window())
    fake_use_case = Mock()
    fake_use_case.execute.return_value = fake_result

    with patch("src.main.traffic_validation_use_case", fake_use_case):
        with TestClient(app) as client:
            response = client.post(
                "/traffic/validate",
                json={
                    "sensorId": "sensor-1",
                    "zoneId": "zone-A",
                    "windowStart": "2026-04-11T10:00:00Z",
                    "windowEnd": "2026-04-11T10:00:15Z",
                    "vehicles": [
                        {"speedKmh": 45, "vehicleType": "car"},
                        {"speedKmh": 40, "vehicleType": "truck"},
                        {"speedKmh": 20, "vehicleType": "car"},
                    ],
                    "vehicleCount": 3,
                },
            )

    assert response.status_code == 200
    assert response.json()["validation"]["trafficClass"] == "medium"
    fake_use_case.execute.assert_called_once()


def test_use_case_publishes_when_payload_is_valid() -> None:
    publisher = Mock()
    use_case = ValidateTrafficUseCase(
        validation_service=TrafficValidationService(),
        publisher=publisher,
    )

    result = use_case.execute(_build_window())

    assert result.accepted is True
    publisher.publish.assert_called_once_with(result)


def test_rabbitmq_consumer_callback_transforms_and_executes_use_case() -> None:
    use_case = Mock()
    consumer = RabbitMQConsumer(use_case)
    body = json.dumps(
        {
            "sensorId": "sensor-1",
            "zoneId": "zone-A",
            "windowStart": "2026-04-11T10:00:00Z",
            "windowEnd": "2026-04-11T10:00:15Z",
            "vehicles": [{"speedKmh": 35, "vehicleType": "car"}],
            "vehicleCount": 1,
        }
    ).encode()

    consumer.callback(None, None, None, body)

    use_case.execute.assert_called_once()
    arg = use_case.execute.call_args.args[0]
    assert arg.sensor_id == "sensor-1"
    assert arg.vehicle_count == 1


def test_rabbitmq_consumer_start_consuming_handles_connection_error() -> None:
    use_case = Mock()
    consumer = RabbitMQConsumer(use_case)

    with patch("src.adapters.rabbitmq.consumer.pika.BlockingConnection", side_effect=OSError("down")):
        consumer.start_consuming()


def test_rabbitmq_publisher_publishes_validation_result() -> None:
    validation_result = TrafficValidationService().validate(_build_window())
    fake_channel = Mock()
    fake_connection = Mock()
    fake_connection.channel.return_value = fake_channel

    with patch("src.adapters.rabbitmq.publisher.pika.BlockingConnection", return_value=fake_connection):
        publisher = RabbitMQPublisher()
        publisher.publish(validation_result)

    fake_channel.queue_declare.assert_called_once()
    fake_channel.basic_publish.assert_called_once()
    fake_connection.close.assert_called_once()


def test_rabbitmq_publisher_handles_connection_error() -> None:
    validation_result = TrafficValidationService().validate(_build_window())

    with patch("src.adapters.rabbitmq.publisher.pika.BlockingConnection", side_effect=OSError("down")):
        publisher = RabbitMQPublisher()
        publisher.publish(validation_result)


def test_sensor_validation_service_normal_level_for_co2() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="co2", value=500)

    assert result["valid"] is True
    assert result["level"] == "normal"
    assert result["threshold"] == 800
    assert result["sensor"] == "co2"


def test_sensor_validation_service_moderate_and_critical_levels() -> None:
    service = SensorValidationService()

    moderate = service.validate(sensor="temperature", value=37)
    critical = service.validate(sensor="noise", value=90)

    assert moderate["level"] == "moderate"
    assert moderate["threshold"] == 40
    assert critical["level"] == "critical"
    assert critical["threshold"] == 85


def test_sensor_validation_service_supports_additional_sensor_humidity() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="humidity", value=62)

    assert result["valid"] is True
    assert result["level"] == "moderate"
    assert result["threshold"] == 75


def test_validate_endpoint_matches_contract() -> None:
    with TestClient(app) as client:
        response = client.post("/validate", json={"sensor": "co2", "value": 500})

    assert response.status_code == 200
    payload = response.json()
    assert payload["valid"] is True
    assert payload["level"] == "normal"
    assert payload["sensor"] == "co2"
    assert payload["value"] == 500
    assert payload["threshold"] == 800
    assert payload["timestamp"].endswith("Z")


def test_validate_endpoint_returns_unknown_for_unsupported_sensor() -> None:
    with TestClient(app) as client:
        response = client.post("/validate", json={"sensor": "voc", "value": 42})

    assert response.status_code == 200
    payload = response.json()
    assert payload["valid"] is False
    assert payload["level"] == "unknown"
    assert payload["threshold"] is None