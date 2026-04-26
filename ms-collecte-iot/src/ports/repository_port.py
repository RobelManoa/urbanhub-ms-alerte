from abc import ABC, abstractmethod

from src.domain.entities import NormalizedIoTWindow


class IoTRepositoryPort(ABC):
    """Contrat de persistence des donnees IoT normalisees."""

    @abstractmethod
    def save(self, payload: NormalizedIoTWindow):
        """Enregistre une charge utile normalisee dans le stockage choisi.

        Args:
            payload (NormalizedIoTWindow): Donnees normalisees a persister.

        Returns:
            None
        """
        pass
