# 03 - Analyse SonarCloud High/Critical

## Objectif

SonarCloud est utilise pour suivre la maintenabilite du code, la couverture, les code smells, les bugs potentiels et la complexite.

La configuration du microservice est dans :

```text
ms-validateur/sonar-project.properties
```

## Configuration principale

```properties
sonar.sources=src
sonar.tests=tests
sonar.python.coverage.reportPaths=03_rapport_tests/coverage.xml
sonar.python.xunit.reportPath=03_rapport_tests/rapport_tests.xml
sonar.python.flake8.reportPaths=reports/quality/flake8_apres.txt
```

Cette configuration permet a SonarCloud de lire :

- le code source ;
- les tests ;
- le rapport de couverture ;
- le rapport JUnit ;
- le rapport flake8.

## Points High/Critical surveilles

Les alertes High ou Critical sont les plus importantes, car elles peuvent indiquer un vrai risque de maintenance ou de comportement.

| Zone | Risque possible | Reponse appliquee |
|---|---|---|
| `src/domain/services.py` | Trop de regles dans une seule fonction. | Classification et score isoles dans des methodes dediees. |
| `src/domain/sensor_validation.py` | Conditions de seuils difficiles a maintenir. | Seuils externalises dans `src/config/sensor_thresholds.py`. |
| `src/adapters/api/routes.py` | Routes FastAPI trop chargees. | Les routes deleguent au domaine et aux cas d'utilisation. |
| `src/adapters/rabbitmq/` | Erreurs de connexion au broker. | Gestion des exceptions et tests avec mocks. |

## Analyse des balises High/Critical apres correction

Le rapport local apres correction contient les traces `sonar_apres.png` et `sonar_apres.txt`, mais le scan complet SonarCloud depend de `SONAR_TOKEN` et du tableau de bord distant. Les points ci-dessous documentent donc les balises High/Critical a verifier dans le rapport apres correction, avec la correction ou la justification retenue dans le code.

### 1. Cognitive Complexity

| Champ | Analyse |
|---|---|
| Nom de la balise | `Cognitive Complexity` |
| Signification | Mesure la difficulte a comprendre une fonction. Plus il y a de conditions imbriquees, de boucles ou de branches, plus la complexite augmente. |
| Localisation | Principalement `src/domain/services.py`, fonction `TrafficValidationService.validate`, et `src/domain/sensor_validation.py`, fonction `SensorValidationService.validate`. |
| Cause | La validation metier peut vite accumuler plusieurs controles : capteur, fenetre temporelle, nombre de vehicules, seuils, classification et score qualite. |
| Action | La logique a ete separee : les seuils sont dans `src/config/sensor_thresholds.py`, la validation capteur dans `src/domain/sensor_validation.py`, la classification trafic dans `_classify` et le score dans `_compute_quality_score`. |
| Impact | Le code est plus simple a lire, plus facile a tester et moins risque lors de l'ajout de nouvelles regles. |

### 2. Maintainability / Code Smells

| Champ | Analyse |
|---|---|
| Nom de la balise | `Code Smells` / `Maintainability` |
| Signification | Indique les problemes qui ne cassent pas forcement l'execution, mais qui rendent le code plus difficile a maintenir. |
| Localisation | `src/validator.py`, `src/adapters/api/routes.py`, `src/domain/`, `src/adapters/rabbitmq/`. |
| Cause | Une premiere version pouvait melanger creation FastAPI, routes, configuration des seuils et logique de validation dans les memes fichiers. |
| Action | Le code est organise par responsabilite : `config`, `domain`, `application`, `adapters`, `ports`. Les routes FastAPI restent courtes et deleguent le traitement au domaine. |
| Impact | La dette technique diminue et les futures modifications sont mieux localisees. Un nouveau developpeur peut comprendre le role de chaque dossier plus rapidement. |

### 3. Reliability / Bugs

| Champ | Analyse |
|---|---|
| Nom de la balise | `Reliability` / `Bugs` |
| Signification | Signale les comportements qui peuvent produire un bug, une erreur runtime ou un resultat incorrect. |
| Localisation | `src/adapters/rabbitmq/consumer.py`, `src/adapters/rabbitmq/publisher.py`, `src/domain/services.py`. |
| Cause | Les connexions RabbitMQ peuvent echouer, un message peut etre invalide, ou une fenetre de trafic peut contenir des valeurs incoherentes. |
| Action | Les cas d'erreur RabbitMQ sont couverts par tests avec mocks. Les donnees invalides sont rejetees avec un statut de validation et une liste d'issues. |
| Impact | Le service evite de publier des donnees invalides vers `validated_queue` et reste plus robuste lorsque le broker n'est pas disponible. |

### 4. Security Hotspots

| Champ | Analyse |
|---|---|
| Nom de la balise | `Security Hotspots` |
| Signification | Repere les zones du code qui meritent une revue securite, meme si ce ne sont pas toujours des vulnerabilites confirmees. |
| Localisation | `src/adapters/api/routes.py`, `src/validator.py`, `Dockerfile`. |
| Cause | Le service expose une API HTTP et traite des donnees externes. Une mauvaise validation des entrees pourrait laisser passer des donnees incorrectes. |
| Action | Les schemas Pydantic imposent des contraintes simples : champs obligatoires, chaines non vides, valeurs numeriques positives. Le conteneur Docker utilise un utilisateur non-root. |
| Impact | La surface d'attaque reste limitee et les entrees sont filtrees avant d'atteindre la logique metier. |

### 5. Coverage on New Code

| Champ | Analyse |
|---|---|
| Nom de la balise | `Coverage` / `Coverage on New Code` |
| Signification | Mesure la proportion de code executee par les tests. Une couverture faible sur du nouveau code peut declencher une alerte qualite. |
| Localisation | Rapport `03_rapport_tests/coverage.xml`, lu par SonarCloud via `sonar.python.coverage.reportPaths`. |
| Cause | Les branches techniques comme les erreurs RabbitMQ ou les cas rejetes peuvent etre oubliees si seuls les cas nominaux sont testes. |
| Action | Les tests couvrent les cas `normal`, `moderate`, `critical`, `unknow`, les endpoints API, le use case et les erreurs RabbitMQ. |
| Impact | La couverture apres correction atteint 92.41%, au-dessus du seuil attendu de 80%. Le risque de regression est reduit. |

### 6. Duplicated Lines

| Champ | Analyse |
|---|---|
| Nom de la balise | `Duplicated Lines` |
| Signification | Mesure les blocs de code dupliques. Trop de duplication rend les corrections plus longues et augmente le risque d'incoherence. |
| Localisation | Principalement les tests et les validations de payload dans `tests/`, `src/adapters/api/schemas.py` et `src/domain/`. |
| Cause | Les tests peuvent repeter des payloads similaires pour verifier plusieurs niveaux de validation. |
| Action | Les tests de trafic utilisent une fonction d'aide `_build_window`. Les seuils capteurs sont centralises dans un dictionnaire unique. |
| Impact | Les changements de seuil ou de structure de payload sont plus faciles a propager et moins sujets aux oublis. |

## Couverture et maintenabilite

Les tests locaux donnent une couverture de 92.41%, au-dessus du seuil demande de 80%.

Les parties les moins couvertes restent les zones techniques liees aux erreurs RabbitMQ et aux branches de securite. C'est acceptable pour cette version, mais ce sont les premieres zones a renforcer si le service devient critique en production.

## Etat des captures SonarCloud

Les fichiers suivants existent :

- `reports/quality/sonar_avant.png`
- `reports/quality/sonar_apres.png`

Dans l'environnement local, ces fichiers servent de traces. Les captures reelles doivent etre recuperees depuis SonarCloud apres execution du pipeline avec `SONAR_TOKEN`.

## Lecture avant / apres

Avant correction, les risques principaux etaient :

- melanger configuration, validation et API ;
- laisser les routes FastAPI porter trop de logique ;
- ne pas avoir de couverture suffisante pour les branches importantes.

Apres correction, le code est separe en couches :

- configuration ;
- domaine ;
- application ;
- adapters API et RabbitMQ.

Cette structure rend les alertes SonarCloud plus faciles a comprendre et a corriger.
