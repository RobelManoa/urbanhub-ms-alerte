# Architecture Decision Records

Ce dossier contient les decisions d'architecture du microservice `ms-validateur`.

Chaque ADR explique le contexte, la decision, le statut et les consequences. Le dossier existe des le debut du projet pour eviter que les choix structurants restent implicites.

## Contenu

- `0001-use-fastapi-and-rabbitmq.md` : choix de FastAPI pour l'API et RabbitMQ pour l'integration evenementielle.
- `0002-separate-domain-config-and-adapters.md` : separation entre configuration, domaine, application et adapters.
