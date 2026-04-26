from src.validator import (
    validate_iso_timestamp,
    validate_log_level,
    validate_log_payload,
    validate_required_fields,
)


def test_validate_required_fields_ok() -> None:
    payload = {"service": "ms-alerte", "event_type": "alert", "message": "ok"}
    missing = validate_required_fields(payload, ["service", "event_type", "message"])
    assert missing == []


def test_validate_required_fields_missing_or_empty() -> None:
    payload = {"service": "", "event_type": "alert"}
    missing = validate_required_fields(payload, ["service", "event_type", "message"])
    assert missing == ["service", "message"]


def test_validate_log_level() -> None:
    assert validate_log_level("INFO") is True
    assert validate_log_level("BAD_LEVEL") is False
    assert validate_log_level(None) is True


def test_validate_iso_timestamp() -> None:
    assert validate_iso_timestamp("2026-04-26T10:30:00Z") is True
    assert validate_iso_timestamp("2026-04-26T10:30:00+00:00") is True
    assert validate_iso_timestamp("26/04/2026 10:30:00") is False


def test_validate_log_payload_ok() -> None:
    ok, errors = validate_log_payload(
        {
            "service": "ms-journalisation",
            "event_type": "notification_sent",
            "message": "email envoye",
            "level": "INFO",
            "timestamp": "2026-04-26T10:30:00Z",
        }
    )
    assert ok is True
    assert errors == []


def test_validate_log_payload_errors() -> None:
    ok, errors = validate_log_payload(
        {
            "service": "",
            "event_type": "notification_sent",
            "level": "NOPE",
            "timestamp": "not-a-date",
        }
    )
    assert ok is False
    assert any("champs obligatoires" in message for message in errors)
    assert "level invalide" in errors
    assert "timestamp invalide" in errors
