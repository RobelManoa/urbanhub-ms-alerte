from pymongo.collection import Collection

from src.domain.entities import NormalizedIoTWindow
from src.ports.repository_port import IoTRepositoryPort


class MongoIoTRepository(IoTRepositoryPort):
    """Persiste les donnees normalisees dans une collection MongoDB."""

    def __init__(self, collection: Collection):
        """Recoit la collection MongoDB cible pour les insertions.

        Args:
            collection (Collection): Collection MongoDB dans laquelle inserer
                les documents normalises.

        Returns:
            None
        """
        self.collection = collection

    def save(self, payload: NormalizedIoTWindow):
        """Enregistre le document normalise dans MongoDB.

        Args:
            payload (NormalizedIoTWindow): Donnees normalisees a enregistrer.

        Returns:
            None

        Raises:
            pymongo.errors.PyMongoError: Si l'insertion MongoDB echoue.
        """
        self.collection.insert_one(payload.to_dict())
