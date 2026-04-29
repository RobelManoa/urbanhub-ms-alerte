# 01 - Presentation du microservice ms-validateur

## Role dans UrbanHub

`ms-validateur` est le microservice qui sert de controle qualite entre la collecte IoT et l'analyse.

Dans le flux UrbanHub, il se place entre `ms-collecte-iot` et `ms-analyse` :

```text
Capteur IoT simule -> ms-collecte-iot -> ms-validateur -> ms-analyse
```

Son objectif est simple : eviter qu'une donnee incoherente ou critique parte directement vers le traitement d'analyse.

## Responsabilites principales

Le microservice assure deux types de validation.

La premiere validation concerne les mesures capteurs simples via `POST /validate`. Le service recoit un capteur et une valeur, puis retourne un niveau :

- `normal` ;
- `moderate` ;
- `critical` ;
- `unknow` pour un capteur non reconnu.

La deuxieme validation concerne les fenetres de trafic UrbanHub via `POST /traffic/validate`. Cette partie permet d'enrichir les donnees avant publication vers la file RabbitMQ `validated_queue`.

## Endpoints disponibles

| Endpoint | Description |
|---|---|
| `GET /health` | Verifie que le service est disponible. |
| `POST /validate` | Valide une mesure capteur simple. |
| `POST /traffic/validate` | Valide une fenetre de trafic venant du SI UrbanHub. |

## Exemple du contrat `POST /validate`

Entree :

```json
{"sensor": "co2", "value": 500}
```

Sortie :

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

Le timestamp est genere en UTC au moment de la validation.

## Seuils capteurs

| Capteur | Seuil modere | Seuil critique | Unite |
|---|---:|---:|---|
| `co2` | 800 | 1000 | ppm |
| `temperature` | 35 | 40 | C |
| `noise` | 70 | 85 | dB |
| `humidity` | 60 | 75 | % |
| `pressure` | 1000 | 1200 | hPa |

Ces seuils sont definis dans `src/config/sensor_thresholds.py`.

## Organisation du code

Le service a ete structure pour rester lisible et maintenable :

- `src/config/` contient les seuils ;
- `src/domain/` contient les regles metier ;
- `src/application/` orchestre les cas d'utilisation ;
- `src/adapters/api/` contient les routes FastAPI ;
- `src/adapters/rabbitmq/` gere l'integration RabbitMQ.

Cette separation evite de mettre toute la logique dans une seule route FastAPI.
