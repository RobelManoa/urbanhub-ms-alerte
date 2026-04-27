# ms-validateur

`ms-validateur` est le microservice de qualite qui s intercale entre `ms-collecte-iot` et `ms-analyse`.

## Role

- consommer les fenetres IoT normalisees depuis RabbitMQ
- verifier la coherence des donnees capteur
- classer chaque fenetre selon la charge de trafic
- republier uniquement les donnees valides vers `validated_queue`

## Flux

1. `ms-collecte-iot` publie une fenetre dans `collecte_queue`
2. `ms-validateur` consomme la fenetre
3. Le service valide les champs, les horodatages, les vehicules et les seuils metier
4. La fenetre enrichie est republiee dans `validated_queue`
5. `ms-analyse` consomme ensuite `validated_queue`

## Regles metier

- `trafficClass = high` si la vitesse moyenne est inferieure a 25 km/h, ou si la fenetre contient au moins 12 vehicules, ou si au moins 5 vehicules sont lents
- `trafficClass = medium` si la vitesse moyenne est inferieure a 40 km/h, ou si la fenetre contient au moins 6 vehicules, ou si au moins 2 vehicules sont lents
- `trafficClass = low` sinon
- une fenetre invalide n est pas republiee

## Variables d environnement

- `RABBITMQ_HOST` : hote RabbitMQ, par defaut `localhost`
- `RABBITMQ_INPUT_QUEUE` : file d entree, par defaut `collecte_queue`
- `RABBITMQ_OUTPUT_QUEUE` : file de sortie, par defaut `validated_queue`
- `ENABLE_RABBITMQ_CONSUMER` : active le consumer au demarrage, par defaut `false`

## Endpoints

- `GET /health`
- `POST /validate`
- `POST /traffic/validate`

### Contrat `POST /validate`

Entree:

```json
{"sensor": "co2", "value": 500}
```

Sortie:

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

Regles de validite:

- `normal` et `moderate` donnent `valid: true`
- `critical` donne `valid: false`
- capteur non repertorie donne `level: "unknow"` et `valid: false`

Seuils de reference:

- `co2` : modere `800`, critique `1000` (ppm)
- `temperature` : modere `35`, critique `40` (C)
- `noise` : modere `70`, critique `85` (dB)
- `humidity` : modere `60`, critique `75` (%)

Le conteneur expose le service sur le port `8000`.
Dans le `docker-compose` global, il est publie sur le port `8006`.

## Lancement local

```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Tests et couverture

Commande recommandee:

```bash
mkdir -p 03_rapport_tests
pytest tests \
	--tb=short \
	--junitxml=03_rapport_tests/rapport_tests.xml \
	--cov=src \
	--cov-report=term \
	--cov-report=xml:03_rapport_tests/coverage.xml \
	--cov-fail-under=80 \
	2>&1 | tee 03_rapport_tests/rapport_tests.txt
cp 03_rapport_tests/rapport_tests.xml 03_rapport_tests/rapport_test.xml
```