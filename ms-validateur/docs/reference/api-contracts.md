# Contrats d'API

## `GET /health`

Reponse :

```json
{"status":"ok"}
```

## `POST /validate`

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

Niveaux :

| Niveau | Condition | Validite |
|---|---|---|
| `normal` | valeur inferieure au seuil modere | `true` |
| `moderate` | valeur entre seuil modere et seuil critique | `true` |
| `critical` | valeur superieure ou egale au seuil critique | `false` |
| `unknow` | capteur inconnu ou valeur invalide | `false` |

## `POST /traffic/validate`

Ce contrat valide une fenetre de trafic issue de `ms-collecte-iot`.

Champs principaux :

- `sensorId`
- `zoneId`
- `windowStart`
- `windowEnd`
- `vehicles`
- `vehicleCount`

La sortie ajoute un bloc `validation` avec :

- `status`
- `trafficClass`
- `qualityScore`
- `issues`
