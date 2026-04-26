from abc import ABC, abstractmethod

from src.domain.entities import NormalizedIoTWindow


class PublisherPort(ABC):
    """Contrat de publication d'un message normalise."""

    @abstractmethod
    def publish(self, payload: NormalizedIoTWindow):
        """Publie la charge utile normalisee vers un systeme externe.

        Args:
            payload (NormalizedIoTWindow): Charge utile normalisee a publier.

        Returns:
            None
        """
        pass
