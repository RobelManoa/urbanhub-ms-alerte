from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class VehicleReading:
    speed_kmh: float
    vehicle_type: str


@dataclass(frozen=True)
class TrafficWindow:
    sensor_id: str
    zone_id: str
    window_start: datetime
    window_end: datetime
    vehicles: list[VehicleReading]
    vehicle_count: int

    def to_dict(self) -> dict:
        return {
            "sensorId": self.sensor_id,
            "zoneId": self.zone_id,
            "windowStart": self.window_start.isoformat(),
            "windowEnd": self.window_end.isoformat(),
            "vehicles": [
                {
                    "speedKmh": vehicle.speed_kmh,
                    "vehicleType": vehicle.vehicle_type,
                }
                for vehicle in self.vehicles
            ],
            "vehicleCount": self.vehicle_count,
        }


@dataclass(frozen=True)
class ValidationResult:
    traffic_window: TrafficWindow
    accepted: bool
    traffic_class: str
    quality_score: int
    issues: list[str]

    def to_dict(self) -> dict:
        payload = self.traffic_window.to_dict()
        payload["validation"] = {
            "status": "accepted" if self.accepted else "rejected",
            "trafficClass": self.traffic_class,
            "qualityScore": self.quality_score,
            "issues": self.issues,
        }
        return payload