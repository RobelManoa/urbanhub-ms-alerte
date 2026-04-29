# Utiliser le pipeline CI/CD

Le workflow est defini dans `.github/workflows/ms-validateur.yml`.

## Declencheurs

- `push` vers `main` ou `develop`.
- `pull_request` vers `main`.
- Changements dans `ms-validateur/**`, `ms-validateur-capteur/**` ou le workflow.

## Jobs

| Job | Role |
|---|---|
| `test` | Installe les dependances, execute pytest et publie les rapports. |
| `quality` | Execute flake8, SonarCloud et Snyk. |
| `build` | Construit l'image Docker et pousse vers GHCR. |
| `verify-image` | Lance l'image publiee et verifie `/health` sur `8000`. |
| `deploy-staging` | Lance `ms-validateur` via Docker Compose et verifie `8006`. |

## Secrets requis

- `SONAR_TOKEN` pour SonarCloud.
- `SNYK_TOKEN` pour Snyk.
- `GITHUB_TOKEN` pour GHCR, fourni automatiquement par GitHub Actions.
