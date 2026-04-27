from typing import Protocol

from src.domain.entities import ValidationResult


class PublisherPort(Protocol):
    def publish(self, validation_result: ValidationResult) -> None:
        raise NotImplementedError