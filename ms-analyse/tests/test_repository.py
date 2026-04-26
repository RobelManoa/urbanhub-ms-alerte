from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.database.models import Base
from src.adapters.database.repository import SQLAlchemyDashboardRepository


def build_analysis_result(zone_id: str) -> dict:
    return {
        "outputs": [
            {
                "destination": "dashboard",
                "payload": {
                    "sensorId": f"sensor-{zone_id}",
                    "zoneId": zone_id,
                    "trafficState": "medium",
                    "averageSpeedKmh": 35.0,
                    "vehicleCount": 3,
                    "windowStart": datetime(2026, 4, 11, 10, 0, tzinfo=timezone.utc).isoformat(),
                    "windowEnd": datetime(2026, 4, 11, 10, 0, 15, tzinfo=timezone.utc).isoformat(),
                },
            }
        ]
    }


def test_repository_saves_and_lists_recent_records() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    repository = SQLAlchemyDashboardRepository(sessionmaker(bind=engine))

    repository.save(build_analysis_result("zone-A"))
    repository.save(build_analysis_result("zone-B"))

    items = repository.list_recent()

    assert len(items) == 2
    assert items[0]["zoneId"] == "zone-B"
    assert items[1]["zoneId"] == "zone-A"


def test_repository_ignores_missing_dashboard_output() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    repository = SQLAlchemyDashboardRepository(sessionmaker(bind=engine))

    repository.save({"outputs": [{"destination": "ms-log", "payload": {"ok": True}}]})

    assert repository.list_recent() == []
