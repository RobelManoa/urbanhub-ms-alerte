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

## Rappel synthetique des vulnerabilites identifiees

Pour `ms-validateur`, les fichiers locaux `snyk_avant.txt` et `snyk_apres.txt` ne listent pas de CVE exploitable, car le CLI Snyk n'etait pas disponible pendant la generation locale. Le scan complet doit donc etre relance dans GitHub Actions avec `SNYK_TOKEN`.

Au niveau du projet UrbanHub, les rapports de correction deja presents indiquent les vulnerabilites suivantes. Les identifiants exacts de CVE ne sont pas toujours fournis dans les rapports locaux ; quand le rapport donne uniquement un nom de faiblesse CWE, il est conserve tel quel.

| CVE / Nom de vulnerabilite | Gravite | Dependance concernee | Statut |
|---|---|---|---|
| Improper Handling of Case Sensitivity, CWE-178 | High, CVSS 8.7 | `flask-cors@5.0.0` | Corrige par passage a `flask-cors==6.0.0`. |
| Improper Verification of Source of Communication Channel, CWE-940 | Medium, CVSS 6.9 | `flask-cors@5.0.0` | Corrige par passage a `flask-cors==6.0.0`. |
| Origin Validation Error, CWE-346 | Medium, CVSS 6.9 | `flask-cors@5.0.0` | Corrige par passage a `flask-cors==6.0.0`. |
| Improper Verification of Cryptographic Signature, CWE-347 | High, CVSS 8.7 | `pyjwt@2.8.0`, transitif via `flask-jwt-extended` | Corrige via mise a jour de la chaine de dependances. |
| Infinite loop, CWE-835 | Medium, CVSS 6.9 | `zipp@3.15.0` | Corrige par version `zipp>=3.19.1`. |
| Symlink Attack, CWE-59 | Medium, CVSS 5.2 | `python-dotenv@0.21.1` / `1.0.0` | Corrige par passage a `python-dotenv==1.2.2`. |
| Always-Incorrect Control Flow Implementation, CWE-670 | Medium, CVSS 5.6 | `requests@2.31.0` | Corrige par passage a `requests==2.32.2`. |
| Insertion of Sensitive Information Into Sent Data, CWE-201 | Medium, CVSS 5.7 | `requests@2.31.0` | Corrige par passage a `requests==2.32.2`. |
| Insecure Temporary File, CWE-377 | Medium, CVSS 4.1 | `requests@2.31.0` | Corrige par passage a `requests==2.32.2`. |
| Inefficient Algorithmic Complexity, CWE-407 | Medium | `werkzeug@2.2.3`, transitif via Flask | Corrige via upgrade de Flask et de ses dependances. |
| Remote Code Execution, CWE-94 | High | `werkzeug@2.2.3`, transitif via Flask | Corrige via upgrade de Flask et de ses dependances. |
| Use of Cache Containing Sensitive Information, CWE-524 | Low, CVSS 2.3 | `flask@2.2.5` | Corrige par passage a `flask==3.1.3`. |

Pour `ms-validateur` lui-meme, les dependances actuelles sont differentes : FastAPI, Uvicorn, Pydantic, Pika et HTTPX. Elles sont versionnees dans `requirements.txt` afin que Snyk analyse toujours le meme graphe de dependances.

## Justification des corrections appliquees

Les corrections appliquees au niveau UrbanHub suivent une logique simple : mettre a jour la dependance directe quand elle est controlee par le projet, et laisser le gestionnaire de dependances resoudre les transitives quand elles dependent d'un package parent.

| Correction | Pourquoi cette version ? | Pourquoi ce remplacement ? |
|---|---|---|
| `flask-cors@5.0.0` vers `flask-cors==6.0.0` | Version plus recente corrigeant les problemes de verification d'origine et de gestion CORS. | `flask-cors` est une dependance directe, donc la correction la plus claire est de fixer une version corrigee. |
| `python-dotenv@0.21.1` / `1.0.0` vers `python-dotenv==1.2.2` | Version plus recente, compatible avec les usages existants et corrigeant le risque de symlink attack. | Le package sert au chargement de variables d'environnement ; le remplacement limite le risque sans changer l'architecture. |
| `requests@2.31.0` vers `requests==2.32.2` | Version corrigee recommandee dans le rapport de remediation. | `requests` est largement utilise et stable ; l'upgrade reduit les risques sans imposer de refonte. |
| `flask@2.2.5` vers `flask==3.1.3` | Version majeure plus recente, incluant des correctifs de securite et une chaine transitive plus saine. | Le remplacement permet aussi de corriger des dependances transitives comme `werkzeug`. |
| `zipp@3.15.0` vers `zipp>=3.19.1` | Version minimale corrigee deja definie dans `ms-analyse`. | `zipp` est une dependance technique ; fixer une version minimale evite de bloquer les patchs futurs. |
| `pyjwt`, `urllib3`, `werkzeug` | Versions corrigees obtenues via mise a jour des dependances directes. | Ces dependances sont transitives ; les forcer directement peut creer des conflits inutiles. Le choix retenu est de corriger le parent qui les amene. |

Pour `ms-validateur`, la mesure appliquee est le versionnement strict des dependances runtime et dev. C'est important, car un microservice expose au reseau doit eviter les installations variables d'un environnement a l'autre.

## Justification des vulnerabilites non corrigees

Dans l'etat actuel, aucune vulnerabilite non corrigee n'est confirmee directement dans `ms-validateur`, car le rapport local ne contient pas de scan Snyk complet.

Les cas restants sont donc classes comme suit :

| Cas | Justification | Decision |
|---|---|---|
| Absence de CVE detaillee dans `ms-validateur/reports/security/snyk_apres.txt` | Le CLI Snyk n'etait pas installe localement. Le fichier ne peut pas etre utilise comme preuve d'absence de vulnerabilite. | Risque accepte temporairement, avec obligation de relancer le scan en CI avec `SNYK_TOKEN`. |
| Dependances transitives non forcees manuellement | Les transitives dependent du graphe resolu par les packages directs. Les forcer sans besoin peut casser la compatibilite. | Maintien justifie tant que Snyk ne remonte pas d'alerte High/Critical apres installation complete. |
| `pika`, `uvicorn`, `httpx`, `fastapi`, `pydantic` | Aucune alerte locale exploitable n'est presente dans les rapports fournis. | Maintien des versions fixees et surveillance par Snyk a chaque execution CI. |
| Rapport Snyk avec `|| true` dans le pipeline | Le pipeline conserve le rapport meme si des failles sont detectees. | Acceptable pour produire les livrables, mais une vraie livraison production devrait bloquer sur High/Critical. |

Si une vulnerabilite High ou Critical apparait apres le scan CI, elle ne doit pas etre acceptee par defaut. Elle doit etre documentee avec la contrainte exacte : incompatibilite technique, dependance transitive non controlable, absence de correctif disponible ou risque juge faible dans le contexte UrbanHub.

## Impact sur la securite globale du projet UrbanHub

L'analyse Snyk renforce la securite globale du projet UrbanHub sur quatre points.

Premier point : elle reduit le risque lie aux dependances exposees au reseau. Les microservices UrbanHub utilisent des API HTTP, RabbitMQ et parfois des bases de donnees. Une dependance vulnerable peut donc avoir un impact direct sur l'entree ou la circulation des donnees.

Deuxieme point : elle evite que les failles d'un microservice contaminent le reste du SI. `ms-validateur` est place entre la collecte IoT et l'analyse ; s'il laisse passer des donnees invalides ou s'il embarque une dependance vulnerable, le risque peut se propager vers `ms-analyse` et les services aval.

Troisieme point : elle rend les corrections tracables. Les fichiers `snyk_avant.txt`, `snyk_apres.txt` et la synthese de remediation permettent de montrer ce qui etait vulnerable, ce qui a ete corrige et ce qui reste accepte temporairement.

Quatrieme point : elle ameliore la discipline CI/CD. Le scan Snyk dans le job `quality`, combine a SonarCloud, flake8 et aux tests, donne une verification plus complete avant la construction de l'image Docker et le deploiement staging.

Pour une mise en production, la recommandation est de faire echouer le pipeline si Snyk detecte une vulnerabilite High ou Critical non justifiee.

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
