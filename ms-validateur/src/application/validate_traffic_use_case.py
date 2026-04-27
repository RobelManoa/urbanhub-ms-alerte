from src.domain.entities import TrafficWindow, ValidationResult
from src.domain.services import TrafficValidationService
from src.ports.publisher_port import PublisherPort


class ValidateTrafficUseCase:
    def __init__(self, validation_service: TrafficValidationService, publisher: PublisherPort) -> None:
        self.validation_service = validation_service
        self.publisher = publisher

    def execute(self, traffic_window: TrafficWindow) -> ValidationResult:
        validation_result = self.validation_service.validate(traffic_window)
        if validation_result.accepted:
            self.publisher.publish(validation_result)
        return validation_result