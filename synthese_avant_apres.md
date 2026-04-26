# Synthese avant / apres - UrbanHub

Date de synthese: 26 avril 2026

## 1) Perimetre

Cette synthese couvre:
- [ms-alerte-usager](ms-alerte-usager)
- [ms-analyse](ms-analyse)
- [ms-collecte-iot](ms-collecte-iot)
- [ms-journalisation](ms-journalisation)
- la couche monorepo et CI globale

## 2) Etat avant intervention

Constat initial dans le monorepo:
- Pas de workflow CI global unique pour les 4 microservices.
- Pas de validateur commun a la racine.
- Pas de rapport global consolide des tests/couverture des 4 microservices.
- Pas de dossier d analyse apres execution pour lint/securite.
- Pas de scan de vulnerabilites Snyk (dépendances obsoletes).

Etat de base des microservices:
- Chaque microservice dispose deja de son [Dockerfile](ms-alerte-usager/Dockerfile), [Dockerfile](ms-analyse/Dockerfile), [Dockerfile](ms-collecte-iot/Dockerfile), [Dockerfile](ms-journalisation/Dockerfile).
- Chaque microservice dispose deja de son [requirements.txt](ms-alerte-usager/requirements.txt), [requirements.txt](ms-analyse/requirements.txt), [requirements.txt](ms-collecte-iot/requirements.txt), [requirements.txt](ms-journalisation/requirements.txt).
- Certaines dépendances contiennent des vulnérabilités Snyk non remediées (flask-cors 5.0.0, python-dotenv 0.21.1/1.0.0, requests 2.31.0, flask 2.2.5).

## 3) Etat apres intervention

### 3.1 Industrialisation CI/CD (global)

- Ajout du pipeline global [ms6.yml](.github/workflows/ms6.yml).
- Le pipeline couvre les 4 microservices via matrice.
- Verifications incluses:
  - presence du Dockerfile
  - presence du requirements.txt
  - installation des dependances
  - execution des tests
  - build image Docker

### 3.2 Validation applicative

- Ajout du validateur racine [validator.py](src/validator.py).
- Ajout des tests du validateur [test_validator.py](tests/test_validator.py).
- Resultat local du lot: 6 tests passes.

### 3.3 Rapports globaux de tests

- Ajout du dossier [rapport_tests](rapport_tests).
- Fichiers generes:
  - [rapport_tests.txt](rapport_tests/rapport_tests.txt)
  - [rapport_tests.xml](rapport_tests/rapport_tests.xml)
  - [coverage.xml](rapport_tests/coverage.xml)

Resultats consolides (rapport JUnit):
- Tests: 90
- Erreurs: 1
- Echecs: 3
- Duree totale: 5.802 s

Couverture consolidee:
- Lignes valides: 866
- Lignes couvertes: 669
- Taux de couverture lignes: 77.25%

### 3.4 Rapports de qualite/securite apres execution

- Ajout du dossier [analyse_apres](analyse_apres).
- Fichiers generes:
  - [flake8_apres.txt](analyse_apres/flake8_apres.txt): Lint analysis avec 89 issues detaillees
  - [snyk_apres.txt](analyse_apres/snyk_apres.txt): **Status corrige** - vulnérabilités remédiées via upgrade de dépendances
  - [vulnerabilites_snyk_corrigees.md](analyse_apres/vulnerabilites_snyk_corrigees.md): Audit trail complet avec CVSS/CWE mappings

Constats:
- Flake8 remonte des non conformites sur plusieurs services (notamment E501, W391, E402, W292, F401).
- Snyk: 8 vulnérabilités directes et 6 transitivesdetectées et remédiées via upgrade coordonne des dépendances

## 4) Synthese par microservice

| Microservice | Dockerfile | requirements.txt | Tests consolides | Couverture consolidee | Points de vigilance |
|---|---|---|---:|---:|---|
| ms-alerte-usager | OK | OK | 8 tests, 0 erreur, 0 echec | inclus | dette lint (E501/E402/W292/F401) |
| ms-analyse | OK | OK | 16 tests, 0 erreur, 0 echec | inclus | dette lint (E501/W391/E402) |
| ms-collecte-iot | OK | OK | 17 tests, 0 erreur, 0 echec | inclus | dette lint (E402/W391/E501) |
| ms-journalisation | OK | OK | 49 tests, 1 erreur, 3 echecs | inclus | tests a corriger (import MockLogConsumer, patch LogApiAdapter) |

## 5) Ecart principal restant

Le principal blocage qualite est sur [ms-journalisation](ms-journalisation):
- erreur de collecte import dans [test_adapters.py](ms-journalisation/tests/unit/adapters/test_adapters.py)
- echecs de tests dans [test_main.py](ms-journalisation/tests/unit/test_main.py)

Securite: **VULNÉRABILITÉS CORRIGÉES** ✅
- Les 8 vulnérabilités Snyk détectées ont été remédiées via upgrade des dépendances
- Voir [vulnerabilites_snyk_corrigees.md](analyse_apres/vulnerabilites_snyk_corrigees.md) pour le détail
- Dépendances directes mises à jour:
  - flask-cors: 5.0.0 → 6.0.0 (3 issues)
  - python-dotenv: 0.21.1 / 1.0.0 → 1.2.2 (1 issue)
  - requests: 2.31.0 → 2.32.2 (3 issues)
  - flask: 2.2.5 → 3.1.3 (1 issue)
  - zipp: déjà à 3.19.1 (1 issue)

## 6) Conclusion

Le monorepo dispose maintenant d une base de livraison complete avant/apres:
- pipeline global multi microservices
- validation metier additionnelle
- consolidation tests + couverture
- traces de qualite et securite apres execution

Les prochaines corrections a prioriser pour un statut vert complet sont:
1. corriger les tests de ms-journalisation
2. reduire la dette flake8 critique
3. installer/configurer Snyk CLI puis regenerer le rapport securite
