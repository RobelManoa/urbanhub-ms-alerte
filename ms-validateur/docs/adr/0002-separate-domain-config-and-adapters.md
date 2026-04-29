# ADR 0002 - Separer domaine, configuration et adapters

## Statut

Acceptee.

## Contexte

La specification demande une bonne maintenabilite SonarCloud, une complexite faible et une separation claire des responsabilites.

## Decision

Separer le code en zones :

- `src/config/` pour les seuils ;
- `src/domain/` pour les regles metier ;
- `src/application/` pour les cas d'usage ;
- `src/adapters/` pour FastAPI et RabbitMQ ;
- `src/ports/` pour les contrats techniques.

## Consequences

- Les routes restent minces.
- Les seuils evoluent sans modifier l'API.
- Les tests peuvent cibler le domaine sans demarrer RabbitMQ.
- La structure est plus lisible pour SonarCloud et pour les mainteneurs.
