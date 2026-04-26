from abc import ABC, abstractmethod


class EventConsumerPort(ABC):
    """Contrat minimal pour un composant consommant des evenements."""

    @abstractmethod
    def start_consuming(self):
        """Demarre l'ecoute et le traitement des messages entrants.

        Returns:
            None
        """
        pass
