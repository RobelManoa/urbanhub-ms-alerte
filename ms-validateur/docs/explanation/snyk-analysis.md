# Analyse Snyk

Snyk controle les vulnerabilites connues des dependances Python du microservice.

## Etat local

Les fichiers suivants existent :

- `reports/security/snyk_avant.txt`
- `reports/security/snyk_apres.txt`

Le contenu local indique que le CLI Snyk n'etait pas installe au moment de la generation. Le workflow CI installe Snyk avec `npm install -g snyk` et produit un rapport complet si `SNYK_TOKEN` est configure.

## Attendus d'analyse

Un rapport Snyk exploitable doit contenir :

- CVE ;
- gravite ;
- package ;
- version vulnerable ;
- version corrigee ;
- action appliquee.

## Mesures deja appliquees

- Dependances runtime versionnees.
- Image Docker minimale `python:3.11-slim`.
- Utilisateur non-root dans le conteneur.
- Verification automatique avant build et staging.
