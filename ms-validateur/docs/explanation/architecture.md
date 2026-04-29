# Architecture et integration UrbanHub

`ms-validateur` agit comme porte de qualite entre la collecte IoT et l'analyse.

Flux :

```text
ms-collecte-iot -> collecte_queue -> ms-validateur -> validated_queue -> ms-analyse
```

## Responsabilites

- Recevoir des mesures capteur via API.
- Valider et classifier les valeurs selon des seuils.
- Recevoir des fenetres de trafic via API ou RabbitMQ.
- Rejeter les donnees incoherentes.
- Publier les donnees acceptees vers `validated_queue`.

## Decoupage technique

- `src/config/` : configuration des seuils.
- `src/domain/` : logique metier.
- `src/application/` : orchestration des cas d'usage.
- `src/adapters/api/` : routes et schemas FastAPI.
- `src/adapters/rabbitmq/` : communication avec RabbitMQ.
- `src/ports/` : contrats techniques internes.

Ce decoupage limite le couplage entre FastAPI, RabbitMQ et les regles metier.
