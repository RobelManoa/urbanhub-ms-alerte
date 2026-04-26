from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.entities import TrafficWindow, VehicleReading


class VehicleReadingRequest(BaseModel):
    speedKmh: float = Field(ge=0)
    vehicleType: str = Field(min_length=1)


class TrafficAnalysisRequest(BaseModel):
    sensorId: str = Field(min_length=1)
    zoneId: str = Field(min_length=1)
    windowStart: datetime
    windowEnd: datetime
    vehicles: list[VehicleReadingRequest]
    vehicleCount: int = Field(ge=0)

    def to_domain(self) -> TrafficWindow:
        return TrafficWindow(
            sensor_id=self.sensorId,
            zone_id=self.zoneId,
            window_start=self.windowStart,
            window_end=self.windowEnd,
            vehicles=[
                VehicleReading(
                    speed_kmh=vehicle.speedKmh,
                    vehicle_type=vehicle.vehicleType,
                )
                for vehicle in self.vehicles
            ],
            vehicle_count=self.vehicleCount,
        )

