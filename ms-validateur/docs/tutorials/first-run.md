# Premier lancement de ms-validateur

Ce tutoriel guide un nouveau developpeur jusqu'a une premiere validation capteur reussie.

## Prerequis

- Python 3.11 ou 3.12.
- Docker si vous souhaitez tester l'image.
- Acces au repository UrbanHub.

## Installer les dependances

Depuis la racine du projet :

```bash
cd ms-validateur
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

## Lancer l'API

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Dans un autre terminal :

```bash
curl http://localhost:8000/health
```

Reponse attendue :

```json
{"status":"ok"}
```

## Valider une mesure capteur

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{"sensor":"co2","value":500}'
```

Reponse attendue :

```json
{
  "valid": true,
  "level": "normal",
  "sensor": "co2",
  "value": 500,
  "threshold": 800,
  "timestamp": "2026-04-27T09:00Z"
}
```

Le champ `timestamp` varie a chaque execution.

## Verifier les tests

```bash
pytest tests \
  --tb=short \
  --junitxml=03_rapport_tests/rapport_tests.xml \
  --cov=src \
  --cov-report=term \
  --cov-report=xml:03_rapport_tests/coverage.xml \
  --cov-fail-under=80
```

Resultat attendu : tests passes et couverture superieure a 80%.
