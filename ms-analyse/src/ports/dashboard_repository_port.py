from typing import Protocol


class DashboardRepositoryPort(Protocol):
    def save(self, analysis_result: dict) -> None:
        """Persist the dashboard-facing analysis result."""

    def list_recent(self) -> list[dict]:
        """Return recent dashboard-facing analysis results."""
