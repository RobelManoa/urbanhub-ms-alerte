from src.domain.entities import TrafficWindow, ValidationResult


class TrafficValidationService:
    allowed_vehicle_types = {"car", "truck", "bus", "bike", "van", "motorcycle"}
    min_speed_kmh = 0
    max_speed_kmh = 140

    def validate(self, traffic_window: TrafficWindow) -> ValidationResult:
        issues: list[str] = []

        if not traffic_window.sensor_id.strip():
            issues.append("sensorId invalide")

        if not traffic_window.zone_id.strip():
            issues.append("zoneId invalide")

        if traffic_window.window_end <= traffic_window.window_start:
            issues.append("windowEnd doit etre posterieure a windowStart")

        if traffic_window.vehicle_count < 0:
            issues.append("vehicleCount invalide")

        if traffic_window.vehicle_count != len(traffic_window.vehicles):
            issues.append("vehicleCount ne correspond pas au nombre de vehicules")

        for index, vehicle in enumerate(traffic_window.vehicles, start=1):
            if vehicle.speed_kmh < self.min_speed_kmh or vehicle.speed_kmh > self.max_speed_kmh:
                issues.append(f"vehicule {index}: speedKmh hors plage")
            if vehicle.vehicle_type.lower() not in self.allowed_vehicle_types:
                issues.append(f"vehicule {index}: vehicleType inconnu")

        if issues:
            return ValidationResult(
                traffic_window=traffic_window,
                accepted=False,
                traffic_class="rejected",
                quality_score=0,
                issues=issues,
            )

        vehicle_speeds = [vehicle.speed_kmh for vehicle in traffic_window.vehicles]
        average_speed = sum(vehicle_speeds) / len(vehicle_speeds) if vehicle_speeds else 0.0
        slow_count = sum(speed < 30 for speed in vehicle_speeds)
        traffic_class = self._classify(average_speed, traffic_window.vehicle_count, slow_count)

        return ValidationResult(
            traffic_window=traffic_window,
            accepted=True,
            traffic_class=traffic_class,
            quality_score=self._compute_quality_score(traffic_class, traffic_window.vehicle_count),
            issues=[],
        )

    def _classify(self, average_speed: float, vehicle_count: int, slow_count: int) -> str:
        if average_speed < 25 or vehicle_count >= 12 or slow_count >= 5:
            return "high"
        if average_speed < 40 or vehicle_count >= 6 or slow_count >= 2:
            return "medium"
        return "low"

    def _compute_quality_score(self, traffic_class: str, vehicle_count: int) -> int:
        base_scores = {"low": 95, "medium": 80, "high": 60}
        score = base_scores.get(traffic_class, 0)
        if vehicle_count == 0:
            return min(score, 90)
        return score