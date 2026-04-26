from typing import Protocol


class PublisherPort(Protocol):
    def publish(self, analysis_result: dict) -> None:
        """Publish analysis outputs to messaging channels."""
