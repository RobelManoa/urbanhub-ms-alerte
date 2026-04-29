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
