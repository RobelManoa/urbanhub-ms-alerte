from dataclasses import dataclass


@dataclass
class RawVehicleRecord:
    """Represente une mesure brute associee a un vehicule detecte."""

    speed: str
    vehicle_type: str


@dataclass
class RawIoTWindow:
    """Represente la fenetre brute recue depuis RabbitMQ."""

    sensor_id: str
    location: str
    started_at: str
    ended_at: str
    data: list[RawVehicleRecord]


@dataclass
class NormalizedVehicle:
    """Represente un vehicule apres nettoyage et conversion des champs."""

    speed_kmh: int
    vehicle_type: str


@dataclass
class NormalizedIoTWindow:
    """Represente le document normalise a stocker et republier."""

    sensor_id: str
    zone_id: str
    window_start: str
    window_end: str
    vehicles: list[NormalizedVehicle]
    vehicle_count: int

    def to_dict(self) -> dict:
        """Convertit l'objet normalise au format dictionnaire cible.

        Returns:
            dict: Representation du document avec les noms de champs attendus
                par MongoDB et RabbitMQ.
        """
        return {
            "sensorId": self.sensor_id,
            "zoneId": self.zone_id,
            "windowStart": self.window_start,
            "windowEnd": self.window_end,
            "vehicles": [
                {
                    "speedKmh": vehicle.speed_kmh,
                    "vehicleType": vehicle.vehicle_type,
                }
                for vehicle in self.vehicles
            ],
            "vehicleCount": self.vehicle_count,
        }
