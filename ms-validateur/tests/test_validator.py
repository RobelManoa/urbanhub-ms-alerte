from src.domain.sensor_validation import SensorValidationService


def test_normal() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="co2", value=500)

    assert result["level"] == "normal"
    assert result["valid"] is True


def test_moderate() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="temperature", value=37)

    assert result["level"] == "moderate"
    assert result["valid"] is True


def test_critical() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="noise", value=85)

    assert result["level"] == "critical"
    assert result["valid"] is False


def test_unknow() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="voc", value=42)

    assert result["level"] == "unknow"
    assert result["valid"] is False
