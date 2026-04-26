from typing import Protocol

from src.domain.entities import TrafficWindow


class AnalysisPort(Protocol):
    def execute(self, traffic_window: TrafficWindow) -> dict:
        """Run a traffic analysis and return routed business outputs."""

