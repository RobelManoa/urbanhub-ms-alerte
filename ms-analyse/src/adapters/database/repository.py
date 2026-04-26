from datetime import datetime

from sqlalchemy.orm import Session, sessionmaker

from src.adapters.database.models import TrafficAnalysisRecord
from src.ports.dashboard_repository_port import DashboardRepositoryPort


class SQLAlchemyDashboardRepository(DashboardRepositoryPort):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def save(self, analysis_result: dict) -> None:
        dashboard_output = next(
            (
                output["payload"]
                for output in analysis_result["outputs"]
                if output["destination"] == "dashboard"
            ),
            None,
        )
        if dashboard_output is None:
            return

        with self.session_factory() as session:
            record = TrafficAnalysisRecord(
                sensor_id=dashboard_output["sensorId"],
                zone_id=dashboard_output["zoneId"],
                traffic_state=dashboard_output["trafficState"],
                average_speed_kmh=dashboard_output["averageSpeedKmh"],
                vehicle_count=dashboard_output["vehicleCount"],
                window_start=self._parse_datetime(dashboard_output["windowStart"]),
                window_end=self._parse_datetime(dashboard_output["windowEnd"]),
                payload=dashboard_output,
            )
            session.add(record)
            session.commit()

    def list_recent(self) -> list[dict]:
        with self.session_factory() as session:
            records = (
                session.query(TrafficAnalysisRecord)
                .order_by(TrafficAnalysisRecord.created_at.desc())
                .limit(50)
                .all()
            )
            return [record.payload for record in records]

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
