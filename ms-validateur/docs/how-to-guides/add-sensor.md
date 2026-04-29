# Ajouter un capteur

## Modifier les seuils

Ajouter le capteur dans `src/config/sensor_thresholds.py` :

```python
"air_quality": SensorThreshold(moderate=50, critical=80, unit="aqi")
```

## Ajouter un test

Ajouter un cas dans `tests/test_validation.py` ou `tests/test_validator.py` :

```python
def test_sensor_validation_service_supports_air_quality() -> None:
    service = SensorValidationService()
    result = service.validate(sensor="air_quality", value=55)

    assert result["valid"] is True
    assert result["level"] == "moderate"
    assert result["threshold"] == 80
```

## Verifier

```bash
pytest tests --cov=src --cov-fail-under=80
```

Le nouveau capteur doit aussi etre ajoute dans la reference des seuils.
