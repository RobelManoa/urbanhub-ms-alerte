# 06 - Evolutivite et integration UrbanHub

## Integration actuelle

`ms-validateur` est integre au systeme UrbanHub comme service de controle entre la collecte IoT et l'analyse.

Flux actuel :

```text
ms-collecte-iot -> collecte_queue -> ms-validateur -> validated_queue -> ms-analyse
```

Dans `docker-compose.yml`, le service depend de RabbitMQ et expose :

```text
8006:8000
```

Le port interne reste `8000`, tandis que le port accessible depuis l'exterieur du compose est `8006`.

## Ajout de nouveaux capteurs

L'ajout d'un capteur est volontairement simple. Il faut modifier :

```text
src/config/sensor_thresholds.py
```

Exemple :

```python
"air_quality": SensorThreshold(moderate=50, critical=80, unit="aqi")
```

Puis ajouter un test dans `tests/` pour verifier le comportement attendu.

Cette approche evite de toucher aux routes API pour chaque nouveau capteur.

## Evolution des seuils

Dans cette version, les seuils sont dans le code. C'est simple, versionne et suffisant pour un premier microservice.

Pour une version plus avancee, les seuils pourraient venir :

- d'un fichier de configuration par environnement ;
- d'une base de donnees ;
- d'un service de configuration central ;
- d'une configuration par zone urbaine.

## Scalabilite

Le service peut etre replique tant que le traitement reste stateless.

Avec RabbitMQ, plusieurs instances peuvent consommer la file `collecte_queue`. Il faudra simplement surveiller :

- l'idempotence du traitement ;
- la gestion des erreurs de publication ;
- les logs des messages rejetes ;
- la consommation concurrente.

## Observabilite

Les ameliorations utiles pour la production seraient :

- logs structures en JSON ;
- metriques Prometheus ;
- compteur de validations par niveau ;
- compteur de messages rejetes ;
- traces des publications vers `validated_queue`.

Ces elements aideraient a suivre la qualite des donnees dans le SI UrbanHub.

## Integration future avec UrbanHub

Le microservice peut evoluer vers un role plus central de validation des donnees urbaines :

- validation de nouveaux types de capteurs ;
- regles differentes selon les zones ;
- enrichissement avec l'unite et la source du seuil ;
- stockage des validations critiques ;
- notification vers un service d'alerte.

La structure actuelle facilite ces evolutions, car les responsabilites sont deja separees entre configuration, domaine, API et RabbitMQ.

## Lien avec les decisions d'architecture

Les decisions importantes sont documentees dans :

```text
ms-validateur/docs/adr/
```

Ce dossier doit continuer a etre alimente a chaque choix structurant : changement de broker, externalisation des seuils, ajout d'une base de donnees ou modification du contrat API.
