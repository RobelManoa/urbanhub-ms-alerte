# Evolutivite

## Ajouter des capteurs

Les seuils et la logique de validation sont separes. Un nouveau capteur peut etre ajoute dans `src/config/sensor_thresholds.py` sans modifier les routes FastAPI.

## Parametrer les seuils

Evolution possible :

- seuils par environnement ;
- seuils par zone urbaine ;
- configuration chargee depuis une base de donnees ;
- historique des changements de seuils.

## Ameliorer l'observabilite

Axes utiles :

- logs structures JSON ;
- metriques Prometheus ;
- compteur de messages rejetes ;
- suivi des classifications par capteur ;
- traces de publication RabbitMQ.

## Scalabilite

Le service peut etre replique derriere RabbitMQ. Les messages de `collecte_queue` peuvent etre consommes par plusieurs instances si le traitement reste idempotent.
