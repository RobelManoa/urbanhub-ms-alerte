# ms-collecte-iot

Microservice de collecte IoT base sur une architecture ports/adapters.

## Role du service

`ms-collecte-iot` est responsable de :

- consommer des donnees IoT brutes depuis RabbitMQ
- normaliser ces donnees dans un format exploitable par les autres services
- enregistrer les donnees normalisees dans MongoDB
- republier les donnees normalisees dans RabbitMQ

## Flux de donnees

1. Le service consomme un message JSON brut depuis la file `iot_raw_queue`
2. Le message est normalise
3. Le resultat est enregistre dans MongoDB dans la base `urbanhub` et la collection `iot_collecte`
4. Le message normalise est publie dans la file `collecte_queue`

## Donnees entrantes

Le service attend un message JSON brut provenant d'un capteur IoT.

Exemple de fichier JSON entrant :

```json
{
  "id": "sensor-1",
  "loc": "A",
  "ts-d": "11/04/26 10:00:00",
  "ts-e": "11/04/26 10:00:15",
  "data": [
    { "spd": "45km/h", "veh": "car" },
    { "spd": "40km/h", "veh": "truck" },
    { "spd": "20km/h", "veh": "car" },
    { "spd": "38km/h", "veh": "bike" }
  ]
}
```

### Signification des champs entrants

- `id` : identifiant du capteur
- `loc` : zone brute ou localisation courte du capteur
- `ts-d` : date de debut de la fenetre de collecte au format `dd/mm/yy HH:MM:SS`
- `ts-e` : date de fin de la fenetre de collecte au format `dd/mm/yy HH:MM:SS`
- `data` : liste des vehicules detectes
- `spd` : vitesse brute sous forme de chaine
- `veh` : type de vehicule brut

## Donnees produites

Le service produit un message JSON normalise publie vers RabbitMQ sur `collecte_queue`.

Exemple de fichier JSON sortant :

```json
{
  "sensorId": "sensor-1",
  "zoneId": "zone-A",
  "windowStart": "2026-04-11T10:00:00Z",
  "windowEnd": "2026-04-11T10:00:15Z",
  "vehicles": [
    { "speedKmh": 45, "vehicleType": "car" },
    { "speedKmh": 40, "vehicleType": "truck" },
    { "speedKmh": 20, "vehicleType": "car" }
  ],
  "vehicleCount": 3
}
```

### Signification des champs sortants

- `sensorId` : identifiant du capteur
- `zoneId` : zone normalisee a partir de `loc`
- `windowStart` : date de debut convertie en ISO 8601 UTC
- `windowEnd` : date de fin convertie en ISO 8601 UTC
- `vehicles` : liste des vehicules retenus apres normalisation
- `speedKmh` : vitesse convertie en entier
- `vehicleType` : type de vehicule normalise
- `vehicleCount` : nombre de vehicules conserves

## Regles de normalisation

- les dates sont converties du format `dd/mm/yy HH:MM:SS` vers le format ISO UTC
- `zoneId` est construit sous la forme `zone-{loc}`
- la vitesse est extraite depuis la chaine brute pour obtenir un entier en km/h
- seuls les types de vehicules supportes sont conserves
- les entrees non reconnues ou invalides sont ignorees

## Variables d'environnement utiles

- `RABBITMQ_HOST` : hote RabbitMQ
- `RABBITMQ_INPUT_QUEUE` : file de consommation, par defaut `iot_raw_queue`
- `RABBITMQ_OUTPUT_QUEUE` : file de publication, par defaut `collecte_queue`
- `MONGODB_URI` : URL de connexion MongoDB
- `MONGODB_DATABASE` : base MongoDB cible, par defaut `urbanhub`
- `MONGODB_COLLECTION` : collection MongoDB cible, par defaut `iot_collecte`

## Test manuel via RabbitMQ Management UI

Pour tester rapidement `ms-collecte-iot`, il est possible de publier un message brut directement depuis RabbitMQ Management.

Interface RabbitMQ Management :

- URL : `http://localhost:15672` (Port à verifier dans le docker compose)
- utilisateur par defaut : `guest`
- mot de passe par defaut : `guest`

### 1. Verifier ou creer la file d'entree

Dans RabbitMQ Management :

1. Aller dans l'onglet `Queues`
2. Verifier si la file `iot_raw_queue` existe
3. Si besoin, la creer avec les parametres suivants :

- Name : `iot_raw_queue`
- Durable : activé si tu veux conserver la queue apres redemarrage

### 2. Publier un message dans RabbitMQ

Dans RabbitMQ Management :

1. Aller dans l'onglet `Exchanges`
2. Ouvrir l'exchange `amq.default`

Pourquoi utiliser `amq.default` :

- c'est le moyen le plus simple pour publier directement dans une queue
- la `routing key` doit etre egale au nom de la queue cible

### 3. Remplir la section `Publish message`

Utiliser les valeurs suivantes :

- Routing key : `iot_raw_queue`
- Payload :

```json
{
  "id": "sensor-1",
  "loc": "A",
  "ts-d": "11/04/26 10:00:00",
  "ts-e": "11/04/26 10:00:15",
  "data": [
    { "spd": "45km/h", "veh": "car" },
    { "spd": "40km/h", "veh": "truck" },
    { "spd": "20km/h", "veh": "car" },
    { "spd": "38km/h", "veh": "bike" }
  ]
}
```

- Properties recommandees :
- `content_type: application/json`
- `delivery_mode: 2`

Puis cliquer sur `Publish message`.

### 4. Resultat attendu

Si `ms-collecte-iot` tourne correctement :

- le message est consommé depuis `iot_raw_queue`
- les donnees sont normalisées
- un document est enregistré dans MongoDB dans `urbanhub.iot_collecte`
- un message normalisé est publié dans la queue `collecte_queue`

### 5. Verifications apres publication

Tu peux verifier le resultat de plusieurs manieres :

- consulter les logs du service `ms-collecte-iot`
- verifier dans MongoDB Compass que la base `urbanhub` contient la collection `iot_collecte`
- verifier dans RabbitMQ Management que la queue `collecte_queue` recoit le message normalisé
