from datetime import datetime, timezone
from unittest.mock import Mock

from src.adapters.api.schemas import TrafficAnalysisRequest
from src.application.use_cases.analyze_traffic_use_case import AnalyzeTrafficUseCase
from src.domain.entities import TrafficWindow, VehicleReading


def test_schema_to_domain_maps_payload() -> None:
    payload = TrafficAnalysisRequest(
        sensorId="sensor-1",
        zoneId="zone-A",
        windowStart=datetime(2026, 4, 11, 10, 0, tzinfo=timezone.utc),
        windowEnd=datetime(2026, 4, 11, 10, 0, 15, tzinfo=timezone.utc),
        vehicles=[{"speedKmh": 45, "vehicleType": "car"}],
        vehicleCount=1,
    )

    domain_payload = payload.to_domain()

    assert domain_payload.sensor_id == "sensor-1"
    assert domain_payload.zone_id == "zone-A"
    assert domain_payload.vehicles[0].vehicle_type == "car"
    assert domain_payload.vehicles[0].speed_kmh == 45


def test_use_case_publishes_and_persists_analysis_result() -> None:
    analysis_service = Mock()
    publisher = Mock()
    repository = Mock()
    expected = {"outputs": [{"destination": "dashboard", "payload": {"zoneId": "zone-A"}}]}
    analysis_service.analyze.return_value = expected
    use_case = AnalyzeTrafficUseCase(analysis_service, publisher, repository)
    traffic_window = TrafficWindow(
        sensor_id="sensor-1",
        zone_id="zone-A",
        window_start=datetime(2026, 4, 11, 10, 0, tzinfo=timezone.utc),
        window_end=datetime(2026, 4, 11, 10, 0, 15, tzinfo=timezone.utc),
        vehicles=[VehicleReading(speed_kmh=45, vehicle_type="car")],
        vehicle_count=1,
    )

    result = use_case.execute(traffic_window)

    assert result == expected
    analysis_service.analyze.assert_called_once_with(traffic_window)
    publisher.publish.assert_called_once_with(expected)
    repository.save.assert_called_once_with(expected)
