# 04 - Analyse cybersecurite Snyk

## Objectif

Snyk est utilise pour analyser les vulnerabilites connues dans les dependances du microservice `ms-validateur`.

Le service etant en Python, l'analyse porte principalement sur :

```text
requirements.txt
requirements-dev.txt
```

## Dependances runtime

| Package | Version |
|---|---|
| `fastapi` | `0.136.1` |
| `uvicorn[standard]` | `0.46.0` |
| `pydantic` | `2.13.3` |
| `pika` | `1.3.2` |
| `httpx` | `0.28.1` |

## Dependances de developpement

| Package | Version |
|---|---|
| `pytest` | `9.0.3` |
| `pytest-cov` | `7.1.0` |
| `coverage` | `7.13.5` |
| `flake8` | `7.3.0` |

Le versionnement fixe limite les differences entre les executions locales et CI.

## Execution dans le pipeline

Le job `quality` installe Snyk puis lance :

```bash
snyk auth "$SNYK_TOKEN"
snyk test --file=requirements.txt > reports/security/snyk_avant.txt || true
snyk test --file=requirements.txt > reports/security/snyk_apres.txt || true
```

Le `|| true` permet de conserver le rapport meme si Snyk detecte des vulnerabilites.

## Rapports attendus

Les rapports sont stockes ici :

- `reports/security/snyk_avant.txt`
- `reports/security/snyk_apres.txt`

Un rapport complet doit permettre d'identifier :

- la CVE ;
- la gravite ;
- le package touche ;
- la version vulnerable ;
- la version corrigee ;
- l'action appliquee.

## Etat local

Dans l'environnement local, les rapports indiquent que le CLI Snyk n'etait pas installe au moment de la generation.

Ce n'est pas un blocage pour la structure du projet, car le pipeline CI installe Snyk automatiquement. Pour obtenir les resultats complets, il faut configurer `SNYK_TOKEN` dans les secrets GitHub.

## Mesures de securite deja appliquees

- Image Docker basee sur `python:3.11-slim`.
- Dependances runtime versionnees.
- Dependances de developpement separees.
- Utilisateur non-root dans le Dockerfile.
- Verification de l'image avant deploiement staging.
- Surface d'API limitee et controlee.

## Points a surveiller

Les dependances les plus sensibles sont celles exposees au reseau :

- FastAPI ;
- Uvicorn ;
- HTTPX ;
- Pika pour RabbitMQ.

En cas d'alerte Snyk High ou Critical, la priorite est de mettre a jour le package, relancer les tests, puis regenerer le rapport `snyk_apres.txt`.
