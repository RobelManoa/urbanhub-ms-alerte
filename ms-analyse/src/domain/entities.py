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

