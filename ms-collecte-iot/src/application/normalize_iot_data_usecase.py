from datetime import UTC, datetime
import re

from src.domain.entities import (
    NormalizedIoTWindow,
    NormalizedVehicle,
    RawIoTWindow,
)
from src.ports.publisher_port import PublisherPort
from src.ports.repository_port import IoTRepositoryPort


class NormalizeIoTDataUseCase:
    """Orchestre la normalisation, la persistence et la republication."""

    SUPPORTED_VEHICLE_TYPES = {"car", "truck", "bus"}

    def __init__(
        self,
        repository: IoTRepositoryPort,
        publisher: PublisherPort,
    ):
        """Initialise le cas d'usage avec le repository et le publisher.

        Args:
            repository (IoTRepositoryPort): Composant charge d'enregistrer les
                donnees normalisees.
            publisher (PublisherPort): Composant charge de republier les
                donnees normalisees vers RabbitMQ.

        Returns:
            None
        """
        self.repository = repository
        self.publisher = publisher

    def execute(self, payload: RawIoTWindow) -> NormalizedIoTWindow:
        """Normalise une fenetre IoT puis la sauvegarde et la republie.

        Args:
            payload (RawIoTWindow): Fenetre brute recue depuis RabbitMQ.

        Returns:
            NormalizedIoTWindow: Charge utile normalisee prete a etre stockee
                et republiee.

        Raises:
            ValueError: Si une date ne respecte pas le format
                ``%d/%m/%y %H:%M:%S``.
        """
        normalized_payload = self._normalize(payload)
        self.repository.save(normalized_payload)
        self.publisher.publish(normalized_payload)
        return normalized_payload

    def _normalize(self, payload: RawIoTWindow) -> NormalizedIoTWindow:
        """Transforme un message brut en document conforme au format cible.

        Args:
            payload (RawIoTWindow): Message brut provenant d'un capteur IoT.

        Returns:
            NormalizedIoTWindow: Document nettoye avec zone, dates ISO et
                vehicules filtres.

        Raises:
            ValueError: Si ``started_at`` ou ``ended_at`` ne peuvent pas etre
                convertis en date ISO UTC.
        """
        vehicles = []

        for record in payload.data:
            normalized_vehicle_type = record.vehicle_type.strip().lower()
            if normalized_vehicle_type not in self.SUPPORTED_VEHICLE_TYPES:
                continue

            speed_kmh = self._parse_speed(record.speed)
            if speed_kmh is None:
                continue

            vehicles.append(
                NormalizedVehicle(
                    speed_kmh=speed_kmh,
                    vehicle_type=normalized_vehicle_type,
                )
            )

        return NormalizedIoTWindow(
            sensor_id=payload.sensor_id,
            zone_id=f"zone-{payload.location.strip()}",
            window_start=self._format_timestamp(payload.started_at),
            window_end=self._format_timestamp(payload.ended_at),
            vehicles=vehicles,
            vehicle_count=len(vehicles),
        )

    @staticmethod
    def _parse_speed(raw_speed: str) -> int | None:
        """Extrait la vitesse numerique en km/h depuis une chaine brute.

        Args:
            raw_speed (str): Valeur brute comme ``"45km/h"``.

        Returns:
            int | None: Vitesse convertie en entier, ou ``None`` si aucune
                valeur numerique n'est detectee.
        """
        match = re.search(r"\d+", raw_speed or "")
        if match is None:
            return None
        return int(match.group())

    @staticmethod
    def _format_timestamp(raw_timestamp: str) -> str:
        """Convertit une date courte capteur vers une date ISO UTC.

        Args:
            raw_timestamp (str): Date brute au format ``dd/mm/yy HH:MM:SS``.

        Returns:
            str: Date convertie au format ISO 8601 en UTC.

        Raises:
            ValueError: Si la date fournie ne respecte pas le format attendu.
        """
        parsed = datetime.strptime(raw_timestamp, "%d/%m/%y %H:%M:%S")
        return parsed.replace(tzinfo=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
