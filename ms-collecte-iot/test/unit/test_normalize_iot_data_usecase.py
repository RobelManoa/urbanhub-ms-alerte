from unittest.mock import Mock

from src.application.normalize_iot_data_usecase import NormalizeIoTDataUseCase
from src.domain.entities import RawIoTWindow, RawVehicleRecord


def test_execute_normalizes_persists_and_publishes_payload():
    repository = Mock()
    publisher = Mock()
    use_case = NormalizeIoTDataUseCase(repository, publisher)

    payload = RawIoTWindow(
        sensor_id="sensor-1",
        location="A",
        started_at="11/04/26 10:00:00",
        ended_at="11/04/26 10:00:15",
        data=[
            RawVehicleRecord(speed="45km/h", vehicle_type="car"),
            RawVehicleRecord(speed="40km/h", vehicle_type="truck"),
            RawVehicleRecord(speed="20km/h", vehicle_type="car"),
            RawVehicleRecord(speed="38km/h", vehicle_type="bike"),
        ],
    )

    result = use_case.execute(payload)

    assert result.to_dict() == {
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
    }
    repository.save.assert_called_once_with(result)
    publisher.publish.assert_called_once_with(result)


def test_execute_ignores_invalid_speed_and_unknown_vehicle_type():
    repository = Mock()
    publisher = Mock()
    use_case = NormalizeIoTDataUseCase(repository, publisher)

    payload = RawIoTWindow(
        sensor_id="sensor-2",
        location="B",
        started_at="12/04/26 09:00:00",
        ended_at="12/04/26 09:00:15",
        data=[
            RawVehicleRecord(speed="unknown", vehicle_type="car"),
            RawVehicleRecord(speed="30km/h", vehicle_type="scooter"),
        ],
    )

    result = use_case.execute(payload)

    assert result.to_dict()["vehicles"] == []
    assert result.to_dict()["vehicleCount"] == 0
    repository.save.assert_called_once_with(result)
    publisher.publish.assert_called_once_with(result)
