from datetime import datetime, timezone

from src.config.sensor_thresholds import SENSOR_THRESHOLDS


class SensorValidationService:
    thresholds = SENSOR_THRESHOLDS

    def validate(self, sensor: str, value: float) -> dict:
        normalized_sensor = sensor.strip().lower()
        threshold = self.thresholds.get(normalized_sensor)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

        if not threshold or value < 0:
            return {
                "valid": False,
                "level": "unknow",
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
            "valid": level != "critical",
            "level": level,
            "sensor": normalized_sensor,
            "value": value,
            "threshold": alert_threshold,
            "timestamp": timestamp,
        }