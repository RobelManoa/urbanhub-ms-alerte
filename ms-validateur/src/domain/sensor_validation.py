from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class SensorThreshold:
    moderate: float
    critical: float
    unit: str


class SensorValidationService:
    thresholds = {
        "co2": SensorThreshold(moderate=800, critical=1000, unit="ppm"),
        "temperature": SensorThreshold(moderate=35, critical=40, unit="C"),
        "noise": SensorThreshold(moderate=70, critical=85, unit="dB"),
        "humidity": SensorThreshold(moderate=60, critical=75, unit="%"),
    }

    def validate(self, sensor: str, value: float) -> dict:
        normalized_sensor = sensor.strip().lower()
        threshold = self.thresholds.get(normalized_sensor)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

        if not threshold or value < 0:
            return {
                "valid": False,
                "level": "unknown",
                "sensor": normalized_sensor,
                "value": value,
                "threshold": None,
                "timestamp": timestamp,
            }

        if value < threshold.moderate:
            level = "normal"
            alert_threshold = threshold.moderate
        elif value < threshold.critical:
            level = "moderate"
            alert_threshold = threshold.critical
        else:
            level = "critical"
            alert_threshold = threshold.critical

        return {
            "valid": True,
            "level": level,
            "sensor": normalized_sensor,
            "value": value,
            "threshold": alert_threshold,
            "timestamp": timestamp,
        }