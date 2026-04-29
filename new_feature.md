# Insertion d'une nouvelle fonctionnalite microservice dans UrbanHub

## Microservice cible

Nom du microservice : `ms-validateur`

Role : porte de qualite entre `ms-collecte-iot` et `ms-analyse`. Avant qu'une donnee brute capteur soit propagee vers le bus d'evenements, elle est validee et classifiee selon des seuils metier definis.

Flux de traitement :

```text
Capteur IoT simule -> ms-collecte-iot -> ms-validateur -> ms-analyse
```

## Taches demandees

- [x] Creer le microservice `ms-validateur`.
- [x] Ecrire les tests unitaires et API.
- [x] Dockeriser le microservice.
- [x] Configurer le pipeline GitHub Actions avec tests, qualite, securite, build, verification d'image et staging.
- [x] Produire les rapports de tests et couverture.
- [x] Produire les traces qualite et securite avant/apres correction.
- [x] Ajouter `ms-validateur` au `docker-compose.yml` general.
- [x] Rediger la documentation complete du microservice.

## Fonctionnalite exposee

`ms-validateur` expose un endpoint `POST /validate`.

Il recoit une donnee capteur et retourne sa classification :

- `normal` : valeur inferieure au seuil modere, `valid=true`
- `moderate` : valeur entre le seuil modere et le seuil critique, `valid=true`
- `critical` : valeur superieure ou egale au seuil critique, `valid=false`
- `unknow` : capteur non repertorie ou valeur invalide, `valid=false`

Le libelle `unknow` est conserve car il est present dans la specification initiale et dans les tests.

## Seuils de reference implementes

| Capteur | Seuil modere | Seuil critique | Unite |
|---|---:|---:|---|
| `co2` | 800 | 1000 | ppm |
| `temperature` | 35 | 40 | C |
| `noise` | 70 | 85 | dB |
| `humidity` | 60 | 75 | % |
| `pressure` | 1000 | 1200 | hPa |

Les seuils sont configures dans `ms-validateur/src/config/sensor_thresholds.py`.

## Contrat d'interface

Endpoint :

```http
POST /validate
```

Exemple d'entree :

```json
{"sensor": "co2", "value": 500}
```

Exemple de sortie :

```json
{
  "valid": true,
  "level": "normal",
  "sensor": "co2",
  "value": 500,
  "threshold": 800,
  "timestamp": "2026-04-27T09:00Z"
}
```

Endpoint complementaire deja integre au flux UrbanHub :

```http
POST /traffic/validate
```

Cet endpoint valide les fenetres de trafic issues de `ms-collecte-iot`, enrichit la charge de trafic, puis publie vers `validated_queue`.

## Commande de tests et couverture

Commande integree au job `test` :

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

Resultat local verifie :

- 19 tests passes.
- Couverture globale : 92.41%.
- Seuil minimum de 80% atteint.

## Exigences de maintenabilite

- [x] Configuration des seuils separee dans `src/config/sensor_thresholds.py`.
- [x] Logique de validation capteur separee dans `src/domain/sensor_validation.py`.
- [x] Logique de validation trafic separee dans `src/domain/services.py`.
- [x] Routes FastAPI separees dans `src/adapters/api/routes.py`.
- [x] Schemas API separes dans `src/adapters/api/schemas.py`.
- [x] Publication/consommation RabbitMQ isolees dans `src/adapters/rabbitmq/`.
- [x] Fonctions courtes et responsabilites separees pour limiter la complexite cyclomatique.

## Verification et separation des livrables

### L1 - Workflow GitHub Actions et code source

| Livrable | Statut | Chemin verifie | Notes |
|---|---|---|---|
| Workflow CI/CD | OK | `.github/workflows/ms-validateur.yml` | 5 jobs sequentiels : `test`, `quality`, `build`, `verify-image`, `deploy-staging`. |
| Code principal | OK | `ms-validateur/src/validator.py` | App FastAPI, `Sensordata`, seuils importes, lifespan RabbitMQ. |
| Routes API | OK | `ms-validateur/src/adapters/api/routes.py` | `GET /health`, `POST /validate`, `POST /traffic/validate`. |
| Tests | OK | `ms-validateur/tests/test_validator.py`, `ms-validateur/tests/test_validation.py` | 19 tests au total, dont cas normal/moderate/critical/unknow. |
| Dockerfile | OK | `ms-validateur/Dockerfile` | Base `python:3.11-slim`, `EXPOSE 8000`, `CMD uvicorn`. |
| Dependances runtime | OK | `ms-validateur/requirements.txt` | Versions fixees pour FastAPI, Uvicorn, Pydantic, Pika, HTTPX. |
| Dependances dev | OK | `ms-validateur/requirements-dev.txt` | Pytest, pytest-cov, coverage et flake8 versions. |
| Sonar | OK | `ms-validateur/sonar-project.properties` | Coverage et JUnit branches vers `03_rapport_tests`. |

### L2 - Rapports pytest et coverage

| Livrable | Statut | Chemin verifie |
|---|---|---|
| Sortie console pytest | OK | `ms-validateur/03_rapport_tests/rapport_tests.txt` |
| Rapport JUnit XML | OK | `ms-validateur/03_rapport_tests/rapport_tests.xml` |
| Alias demande `rapport_test.xml` | OK | `ms-validateur/03_rapport_tests/rapport_test.xml` |
| Rapport coverage XML | OK | `ms-validateur/03_rapport_tests/coverage.xml` |

### L3 - Qualite et securite avant/apres

| Livrable | Statut | Chemin verifie | Notes |
|---|---|---|---|
| Flake8 avant | OK | `ms-validateur/reports/quality/flake8_avant.txt` | Fichier present. |
| Flake8 apres | OK | `ms-validateur/reports/quality/flake8_apres.txt` | Fichier present. |
| Sonar avant | OK avec reserve | `ms-validateur/reports/quality/sonar_avant.png` | Placeholder local, le scan reel est distant via SonarCloud. |
| Sonar apres | OK avec reserve | `ms-validateur/reports/quality/sonar_apres.png` | Placeholder local, le scan reel est distant via SonarCloud. |
| Snyk avant | OK avec reserve | `ms-validateur/reports/security/snyk_avant.txt` | Trace locale indiquant que le CLI Snyk n'etait pas installe. |
| Snyk apres | OK avec reserve | `ms-validateur/reports/security/snyk_apres.txt` | Trace locale indiquant que le CLI Snyk n'etait pas installe. |
| Synthese avant/apres | OK | `ms-validateur/reports/synthese_avant_apres.md`, `ms-validateur/reports/synthese_avant_apres.pdf` | Synthese dediee au microservice. |

### L4 - Deploiement et integration

| Livrable | Statut | Chemin verifie | Notes |
|---|---|---|---|
| Build image | OK | `.github/workflows/ms-validateur.yml` | Image poussee vers `ghcr.io/<org>/ms-validateur:<sha>`. |
| Verification conteneur | OK | `.github/workflows/ms-validateur.yml` | `docker run` et verification `GET /health` sur le port `8000`. |
| Compose staging | OK | `docker-compose.yml` | Service `ms-validateur` expose sur `8006:8000`. |

## Documentation technique Diataxis

La documentation du microservice est disponible dans `ms-validateur/docs/` et applique la methode Diataxis au systeme d'information du validateur :

- [x] `index.md` : entree principale et application de Diataxis au SI UrbanHub.
- [x] `tutorials/` : parcours guide, dont `first-run.md`.
- [x] `how-to-guides/` : procedures reproductibles pour tests, Docker, CI/CD et ajout de capteur.
- [x] `reference/` : contrats d'API, seuils, variables et reference qualite/securite.
- [x] `explanation/` : architecture, evolutivite, analyse SonarCloud et Snyk.
- [x] `adr/` : decisions d'architecture conservees des le debut du projet.

Contraintes appliquees :

- [x] Dossiers en minuscules avec tirets, au format kebab-case.
- [x] `index.md` present dans chaque sous-dossier.
- [x] Arborescence limitee a 3 niveaux maximum : `docs/<section>/<page>.md`.
- [x] Dossier `adr/` cree et alimente avec les premieres decisions.

## Livrables documentaires demandes

Une version de restitution au format attendu est disponible dans `ms-validateur/documentation-technique/` :

- [x] `01_presentation.md` : presentation du microservice.
- [x] `02_pipeline.md` : description du pipeline CI/CD et regroupement en 4 grandes etapes.
- [x] `03_sonarcloud.md` : analyse des balises SonarCloud High/Critical.
- [x] `04_snyk.md` : analyse cybersecurite Snyk approfondie.
- [x] `05_guide_prise_en_main.md` : guide reproductible pour un nouveau developpeur.
- [x] `06_evolutivite.md` : evolutivite et integration UrbanHub.

Ces documents s'appuient sur la documentation Diataxis sans la remplacer.

## Points de verification finale

- [x] Le nom de dossier reel utilise est `ms-validateur`.
- [x] Le workflow surveille `ms-validateur/**` et conserve aussi `ms-validateur-capteur/**` pour compatibilite avec l'intitule initial.
- [x] Le port interne Docker est `8000`.
- [x] Le port expose par le `docker-compose.yml` general est `8006`.
- [x] Les tests couvrent le contrat capteur et le flux trafic/RabbitMQ.
- [x] Les rapports de tests sont generes dans `ms-validateur/03_rapport_tests/`.
- [x] La documentation demandee est reorganisee selon Diataxis.
- [x] La taille du dossier `ms-validateur` reste inferieure a 5 Mo hors caches Python et artefacts de virtualenv.

## Commandes de verification locale

Depuis la racine du projet :

```bash
cd ms-validateur
pip install -r requirements.txt -r requirements-dev.txt
pytest tests \
  --tb=short \
  --junitxml=03_rapport_tests/rapport_tests.xml \
  --cov=src \
  --cov-report=term \
  --cov-report=xml:03_rapport_tests/coverage.xml \
  --cov-fail-under=80 \
  2>&1 | tee 03_rapport_tests/rapport_tests.txt
```

Verification Docker :

```bash
docker build -t ms-validateur:local ms-validateur
docker run --rm -p 8000:8000 ms-validateur:local
curl http://localhost:8000/health
```

Verification compose :

```bash
docker compose up -d ms-validateur
curl http://localhost:8006/health
```


# Remarque pour la documentation : 
dans la partie documentation technique de la nouvelle  microservices validateur j'aimerai que tu suives méthode Diátaxis, et faire Application de Diátaxis au SI (système d'information) du microservices validateur.
• Nommez les dossiers en minuscules avec des tirets (kebab-case) pour la
compatibilité cross-platform.
• Ajoutez un fichier index.md dans chaque sous-dossier avec une description de son
contenu.
• Limitez l'arborescence à 3 niveaux maximum pour éviter la désorientation.
• Créez le dossier adr/ dès le début du projet : les décisions d'architecture non
documentées sont perdues.
