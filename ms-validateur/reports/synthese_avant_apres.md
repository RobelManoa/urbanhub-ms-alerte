# Synthese avant / apres - ms-validateur

## Page 1 - Comparatif qualite et securite

| Element | Avant | Apres |
|---|---|---|
| Tests automatises | A finaliser | 19 tests passes |
| Couverture | Non garantie | 92.41%, seuil 80% atteint |
| Architecture | Risque de logique monolithique | Configuration, domaine, routes et adapters separes |
| Flake8 | Rapport `flake8_avant.txt` present | Rapport `flake8_apres.txt` present |
| SonarCloud | Capture `sonar_avant.png` a remplacer par capture dashboard | Capture `sonar_apres.png` a remplacer par capture dashboard |
| Snyk | Trace `snyk_avant.txt` presente, CLI absent localement | Trace `snyk_apres.txt` presente, scan complet attendu en CI avec `SNYK_TOKEN` |

## Tableau Snyk CVE

| CVE | Gravite | Package | Version vulnerable | Version corrigee | Action appliquee |
|---|---|---|---|---|---|
| Aucune CVE locale exploitable | Non determinee | `requirements.txt` | Non determinee | Versions fixees | Executer Snyk en CI avec `SNYK_TOKEN` |

## Page 2 - Analyse SonarCloud High/Critical

Les captures locales Sonar sont des placeholders. Le workflow execute le scan SonarCloud si `SONAR_TOKEN` est configure.

Points de vigilance High/Critical a verifier dans SonarCloud :

- complexite excessive dans `TrafficValidationService.validate` ;
- duplication de regles entre validation capteur et validation trafic ;
- erreurs non gerees dans les adapters RabbitMQ ;
- couverture insuffisante sur les branches d'erreur ;
- dette de maintenabilite sur les routes FastAPI si elles grossissent.

Etat apres correction :

- seuils externalises ;
- logique capteur isolee ;
- logique trafic isolee ;
- routes FastAPI minces ;
- erreurs RabbitMQ couvertes par tests ;
- couverture globale de 92.41%, superieure a 80%.
