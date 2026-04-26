from src.domain.entities import TrafficWindow
from src.domain.services import TrafficAnalysisService
from src.ports.dashboard_repository_port import DashboardRepositoryPort
from src.ports.publisher_port import PublisherPort


class AnalyzeTrafficUseCase:
    def __init__(
        self,
        analysis_service: TrafficAnalysisService,
        publisher: PublisherPort,
        dashboard_repository: DashboardRepositoryPort,
    ) -> None:
        self.analysis_service = analysis_service
        self.publisher = publisher
        self.dashboard_repository = dashboard_repository

    def execute(self, traffic_window: TrafficWindow) -> dict:
        analysis_result = self.analysis_service.analyze(traffic_window)
        self.publisher.publish(analysis_result)
        self.dashboard_repository.save(analysis_result)
        return analysis_result
