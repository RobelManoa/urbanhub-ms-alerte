# ADR 0001 - Utiliser FastAPI et RabbitMQ

## Statut

Acceptee.

## Contexte

`ms-validateur` doit exposer des endpoints HTTP pour les validations directes et s'integrer au flux evenementiel UrbanHub entre `ms-collecte-iot` et `ms-analyse`.

## Decision

Utiliser :

- FastAPI pour l'API HTTP ;
- RabbitMQ pour consommer `collecte_queue` et publier vers `validated_queue`.

## Consequences

- Les contrats HTTP sont simples a tester avec `TestClient`.
- Le service reste compatible avec le bus d'evenements UrbanHub.
- Les erreurs RabbitMQ doivent etre couvertes par tests et logs.
