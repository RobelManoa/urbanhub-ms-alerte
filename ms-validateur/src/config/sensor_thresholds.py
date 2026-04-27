from dataclasses import dataclass


@dataclass(frozen=True)
class SensorThreshold:
    moderate: float
    critical: float
    unit: str


SENSOR_THRESHOLDS = {
    "co2": SensorThreshold(moderate=800, critical=1000, unit="ppm"),
    "temperature": SensorThreshold(moderate=35, critical=40, unit="C"),
    "noise": SensorThreshold(moderate=70, critical=85, unit="dB"),
    "humidity": SensorThreshold(moderate=60, critical=75, unit="%"),
    "pressure": SensorThreshold(moderate=1000, critical=1200, unit="hPa"),
}