from __future__ import annotations

from datetime import datetime
from typing import Iterable

ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
REQUIRED_LOG_FIELDS = ("service", "event_type", "message")


def validate_required_fields(payload: dict, required_fields: Iterable[str]) -> list[str]:
    missing = []
    for field in required_fields:
        value = payload.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing


def validate_log_level(level: str | None) -> bool:
    if level is None:
        return True
    return level in ALLOWED_LOG_LEVELS


def validate_iso_timestamp(timestamp: str | None) -> bool:
    if timestamp is None:
        return True
    if not isinstance(timestamp, str) or not timestamp.strip():
        return False

    normalized = timestamp.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return True


def validate_log_payload(payload: dict) -> tuple[bool, list[str]]:
    if not isinstance(payload, dict):
        return False, ["payload doit etre un dictionnaire"]

    errors: list[str] = []

    missing = validate_required_fields(payload, REQUIRED_LOG_FIELDS)
    if missing:
        errors.append(f"champs obligatoires manquants: {', '.join(missing)}")

    if not validate_log_level(payload.get("level")):
        errors.append("level invalide")

    if not validate_iso_timestamp(payload.get("timestamp")):
        errors.append("timestamp invalide")

    return len(errors) == 0, errors
