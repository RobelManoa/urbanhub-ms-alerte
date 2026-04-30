# 05 - Guide de prise en main pour un nouveau developpeur

Ce guide permet a un nouveau developpeur de lancer `ms-validateur`, executer les tests et verifier le contrat principal.

## 1. Se placer dans le microservice

Depuis la racine du projet UrbanHub :

```bash
cd ms-validateur
```

## 2. Creer l'environnement Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

Installer les dependances :

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

## 3. Lancer l'API

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Verifier que le service repond :

```bash
curl http://localhost:8000/health
```

Reponse attendue :

```json
{"status":"ok"}
```

## 4. Tester la validation d'un capteur

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{"sensor":"co2","value":500}'
```

La reponse doit indiquer un niveau `normal` avec `valid=true`.

## 5. Lancer les tests

```bash
mkdir -p 03_rapport_tests
pytest tests \
  --tb=short \
  --junitxml=03_rapport_tests/rapport_tests.xml \
  --cov=src \
  --cov-report=term \
  --cov-report=xml:03_rapport_tests/coverage.xml \
  --cov-fail-under=80 \
  2>&1 | tee 03_rapport_tests/rapport_tests.txt
cp 03_rapport_tests/rapport_tests.xml 03_rapport_tests/rapport_test.xml
```

Resultat attendu :

- tests passes ;
- couverture superieure a 80% ;
- rapports generes dans `03_rapport_tests/`.

## 6. Lancer avec Docker

Depuis la racine du projet :

```bash
docker build -t ms-validateur:local ms-validateur
docker run --rm -p 8000:8000 ms-validateur:local
```

Verifier :

```bash
curl http://localhost:8000/health
```

## 7. Lancer avec Docker Compose

Depuis la racine du projet :

```bash
docker compose up -d ms-validateur
curl http://localhost:8006/health
```

## 8. Fichiers utiles

| Fichier | Utilite |
|---|---|
| `src/config/sensor_thresholds.py` | Modifier ou ajouter les seuils capteurs. |
| `src/domain/sensor_validation.py` | Comprendre la validation capteur. |
| `src/domain/services.py` | Comprendre la validation trafic. |
| `src/adapters/api/routes.py` | Voir les routes FastAPI. |
| `tests/` | Tests unitaires et API. |
| `Dockerfile` | Construction de l'image. |
| `sonar-project.properties` | Configuration SonarCloud. |

## 9. GitHub secrets

Pour que le pipeline CI/CD fonctionne completement sur GitHub Actions, certains secrets doivent etre configures dans le repository.

| Secret | Role | Ou le configurer |
|---|---|---|
| `SONAR_TOKEN` | Autorise le scan SonarCloud du microservice et l'envoi des resultats qualite. | GitHub repository -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`. |
| `SNYK_TOKEN` | Autorise l'analyse Snyk des dependances Python et la generation des rapports de securite. | GitHub repository -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`. |
| `GITHUB_TOKEN` | Permet au workflow de pousser l'image Docker vers GHCR. Ce secret est fourni automatiquement par GitHub Actions. | Aucune creation manuelle. Verifier seulement les permissions `packages: write` dans le workflow. |

Apres ajout ou modification d'un secret, relancer le workflow pour verifier que les jobs `quality`, `build` et `deploy-staging` s'executent correctement.
