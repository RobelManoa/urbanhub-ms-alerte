from collections import Counter
from datetime import datetime, timezone

from src.domain.entities import TrafficWindow


class TrafficAnalysisService:
    """Pure domain service that transforms raw traffic observations into insights."""

    def analyze(self, traffic_window: TrafficWindow) -> dict:
        vehicle_speeds = [vehicle.speed_kmh for vehicle in traffic_window.vehicles]
        observed_count = len(traffic_window.vehicles)
        average_speed = sum(vehicle_speeds) / observed_count if observed_count else 0.0
        max_speed = max(vehicle_speeds, default=0.0)
        min_speed = min(vehicle_speeds, default=0.0)
        slow_count = sum(speed < 30 for speed in vehicle_speeds)
        heavy_count = sum(
            vehicle.vehicle_type.lower() in {"truck", "bus"}
            for vehicle in traffic_window.vehicles
        )
        type_counter = Counter(vehicle.vehicle_type.lower() for vehicle in traffic_window.vehicles)
        dominant_vehicle_type = type_counter.most_common(1)[0][0] if type_counter else "unknown"
        window_seconds = max(
            int((traffic_window.window_end - traffic_window.window_start).total_seconds()),
            1,
        )
        flow_rate_per_minute = round((traffic_window.vehicle_count / window_seconds) * 60, 2)
        average_speed = round(average_speed, 2)
        occupancy_gap = traffic_window.vehicle_count - observed_count
        congestion_level = self._compute_congestion_level(
            average_speed=average_speed,
            vehicle_count=traffic_window.vehicle_count,
            slow_count=slow_count,
        )

        dashboard_result = {
            "zoneId": traffic_window.zone_id,
            "sensorId": traffic_window.sensor_id,
            "windowStart": traffic_window.window_start.isoformat(),
            "windowEnd": traffic_window.window_end.isoformat(),
            "trafficState": congestion_level,
            "averageSpeedKmh": average_speed,
            "minSpeedKmh": min_speed,
            "maxSpeedKmh": max_speed,
            "vehicleCount": traffic_window.vehicle_count,
            "observedVehicleCount": observed_count,
            "flowRatePerMinute": flow_rate_per_minute,
            "dominantVehicleType": dominant_vehicle_type,
            "heavyVehicleCount": heavy_count,
            "slowVehicleCount": slow_count,
            "dataQuality": "estimated" if occupancy_gap else "exact",
        }

        alert_result = self._build_alert_result(
            traffic_window=traffic_window,
            dashboard_result=dashboard_result,
        )
        notification_result = self._build_notification_result(dashboard_result=dashboard_result)
        history_result = {
            "analysisType": "traffic",
            "zoneId": traffic_window.zone_id,
            "sensorId": traffic_window.sensor_id,
            "windowStart": traffic_window.window_start.isoformat(),
            "windowEnd": traffic_window.window_end.isoformat(),
            "payload": dashboard_result,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        log_result = {
            "service": "ms-analyse",
            "eventType": "traffic_analysis_completed",
            "zoneId": traffic_window.zone_id,
            "sensorId": traffic_window.sensor_id,
            "severity": "warning" if alert_result["shouldCreateAlert"] else "info",
            "message": f"Traffic analysis completed for zone {traffic_window.zone_id}",
        }
        kpi_result = {
            "zoneId": traffic_window.zone_id,
            "windowStart": traffic_window.window_start.isoformat(),
            "windowEnd": traffic_window.window_end.isoformat(),
            "vehicleCount": traffic_window.vehicle_count,
            "averageSpeedKmh": average_speed,
            "flowRatePerMinute": flow_rate_per_minute,
            "congestionLevel": congestion_level,
            "heavyVehicleRatio": round(heavy_count / observed_count, 2) if observed_count else 0.0,
        }

        return {
            "input": {
                "sensorId": traffic_window.sensor_id,
                "zoneId": traffic_window.zone_id,
                "windowStart": traffic_window.window_start.isoformat(),
                "windowEnd": traffic_window.window_end.isoformat(),
                "vehicleCount": traffic_window.vehicle_count,
            },
            "outputs": [
                {
                    "destination": "dashboard",
                    "channel": "analysis.traffic.result",
                    "contentType": "detailed_result",
                    "payload": dashboard_result,
                },
                {
                    "destination": "ms-alerte",
                    "channel": "alert_queue",
                    "contentType": "simplified_alert",
                    "payload": alert_result,
                },
                {
                    "destination": "historisation",
                    "channel": "postgresql.analysis_results",
                    "contentType": "calculated_analysis",
                    "payload": history_result,
                },
                {
                    "destination": "conducteur",
                    "channel": "analysis.user.notification",
                    "contentType": "readable_message",
                    "payload": notification_result,
                },
                {
                    "destination": "ms-log",
                    "channel": "log.events",
                    "contentType": "technical_trace",
                    "payload": log_result,
                },
                {
                    "destination": "kpi-metier",
                    "channel": "analysis.traffic.kpi",
                    "contentType": "aggregated_kpi",
                    "payload": kpi_result,
                },
            ],
        }

    def _compute_congestion_level(
        self,
        average_speed: float,
        vehicle_count: int,
        slow_count: int,
    ) -> str:
        if average_speed < 25 or vehicle_count >= 12 or slow_count >= 5:
            return "high"
        if average_speed < 40 or vehicle_count >= 6 or slow_count >= 2:
            return "medium"
        return "low"

    def _build_alert_result(self, traffic_window: TrafficWindow, dashboard_result: dict) -> dict:
        should_create_alert = (
            dashboard_result["trafficState"] == "high"
            or dashboard_result["maxSpeedKmh"] >= 80
        )
        alert_type = "traffic_congestion" if dashboard_result["trafficState"] == "high" else "overspeed"
        return {
            "shouldCreateAlert": should_create_alert,
            "alertType": alert_type if should_create_alert else None,
            "zoneId": traffic_window.zone_id,
            "sensorId": traffic_window.sensor_id,
            "severity": "critical" if dashboard_result["trafficState"] == "high" else "medium",
            "summary": (
                f"Congestion detected in zone {traffic_window.zone_id}"
                if dashboard_result["trafficState"] == "high"
                else f"Traffic remains stable in zone {traffic_window.zone_id}"
            ),
        }

    def _build_notification_result(self, dashboard_result: dict) -> dict:
        if dashboard_result["trafficState"] == "high":
            message = (
                f"Circulation dense dans la zone {dashboard_result['zoneId']}: "
                f"vitesse moyenne {dashboard_result['averageSpeedKmh']} km/h."
            )
        elif dashboard_result["trafficState"] == "medium":
            message = (
                f"Trafic ralenti dans la zone {dashboard_result['zoneId']}: "
                f"prudence recommandee."
            )
        else:
            message = (
                f"Trafic fluide dans la zone {dashboard_result['zoneId']} avec "
                f"{dashboard_result['vehicleCount']} vehicules observes."
            )

        return {
            "zoneId": dashboard_result["zoneId"],
            "message": message,
            "priority": dashboard_result["trafficState"],
        }
