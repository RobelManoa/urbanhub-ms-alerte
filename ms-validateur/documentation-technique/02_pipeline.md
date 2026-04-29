# 02 - Pipeline CI/CD du microservice

Le pipeline du microservice est defini dans :

```text
.github/workflows/ms-validateur.yml
```

Il se lance sur les modifications du dossier `ms-validateur/**`, du chemin `ms-validateur-capteur/**` et du fichier workflow lui-meme.

## Vue d'ensemble

Le pipeline contient cinq jobs dans le fichier actuel :

1. `test`
2. `quality`
3. `build`
4. `verify-image`
5. `deploy-staging`

Pour la lecture demandee en quatre grandes etapes, `build` et `verify-image` peuvent etre lus ensemble comme l'etape de construction et verification de l'image Docker.

## Job 1 - test

Ce job installe Python, les dependances du service, puis lance les tests avec couverture.

Commande principale :

```bash
pytest tests \
  --tb=short \
  --junitxml=03_rapport_tests/rapport_tests.xml \
  --cov=src \
  --cov-report=term \
  --cov-report=xml:03_rapport_tests/coverage.xml \
  --cov-fail-under=80 \
  2>&1 | tee 03_rapport_tests/rapport_tests.txt
```

Livrables produits :

- `03_rapport_tests/rapport_tests.txt`
- `03_rapport_tests/rapport_tests.xml`
- `03_rapport_tests/rapport_test.xml`
- `03_rapport_tests/coverage.xml`

Resultat verifie localement :

- 19 tests passes ;
- couverture globale : 92.41% ;
- seuil minimum de 80% atteint.

## Job 2 - quality

Ce job regroupe les controles qualite et securite.

Il execute :

- `flake8` pour la qualite Python ;
- SonarCloud pour la qualite globale, la couverture et la maintenabilite ;
- Snyk pour l'analyse des vulnerabilites.

Livrables attendus :

- `reports/quality/flake8_avant.txt`
- `reports/quality/flake8_apres.txt`
- `reports/quality/sonar_avant.png`
- `reports/quality/sonar_apres.png`
- `reports/security/snyk_avant.txt`
- `reports/security/snyk_apres.txt`

Les scans SonarCloud et Snyk dependent des secrets `SONAR_TOKEN` et `SNYK_TOKEN`.

## Job 3 - build et verify-image

La partie `build` construit l'image Docker du microservice, puis la pousse vers GHCR :

```text
ghcr.io/<org>/ms-validateur:<sha>
```

La partie `verify-image` recupere ensuite cette image, lance un conteneur et verifie que le service repond :

```bash
curl http://localhost:8000/health
```

Cette verification evite de publier une image qui se construit correctement mais qui ne demarre pas.

## Job 4 - deploy-staging

Le dernier job lance le service via le `docker-compose.yml` global :

```bash
docker compose up -d ms-validateur
```

Puis il verifie le port expose en staging :

```bash
curl http://localhost:8006/health
```

Dans le compose UrbanHub, le port interne `8000` est expose sur `8006`.
