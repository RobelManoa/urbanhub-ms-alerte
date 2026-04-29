# Analyse SonarCloud High/Critical

Les captures locales `sonar_avant.png` et `sonar_apres.png` sont presentes dans `reports/quality/`. Dans l'environnement local, elles servent de traces, car le scan reel est execute cote SonarCloud avec `SONAR_TOKEN`.

## Zones a surveiller

| Zone | Risque | Traitement |
|---|---|---|
| `src/domain/services.py` | Accumulation de regles metier. | Extraction de fonctions de classification et de score. |
| `src/domain/sensor_validation.py` | Branches de seuils. | Seuils externalises et tests dedies. |
| `src/adapters/rabbitmq/*` | Erreurs reseau ou broker indisponible. | Tests avec mocks et gestion d'exception. |
| `src/adapters/api/routes.py` | Routes trop riches. | Routes minces, logique deleguee au domaine. |

## Lecture attendue

Les alertes High/Critical doivent etre traitees en priorite si elles touchent :

- la validite des donnees ;
- la publication RabbitMQ ;
- les contrats d'API ;
- la couverture des branches d'erreur.
