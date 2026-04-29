# Application de Diataxis au SI du validateur

`ms-validateur` appartient au systeme d'information UrbanHub. Sa documentation doit servir plusieurs profils :

- nouveau developpeur qui decouvre le service ;
- mainteneur qui doit lancer les tests ou ajouter un capteur ;
- evaluateur qui verifie les livrables CI/CD, qualite et securite ;
- architecte qui veut comprendre les decisions structurantes.

## Separation Diataxis

| Besoin SI | Type Diataxis | Exemple dans cette documentation |
|---|---|---|
| Decouvrir le service par la pratique | Tutoriel | `tutorials/first-run.md` |
| Realiser une operation | Guide pratique | `how-to-guides/run-tests.md` |
| Verifier un contrat exact | Reference | `reference/api-contracts.md` |
| Comprendre les choix et compromis | Explication | `explanation/architecture.md` |
| Tracer une decision structurante | ADR | `adr/0001-use-fastapi-and-rabbitmq.md` |

## Effet sur la gouvernance documentaire

Cette organisation evite de melanger :

- une procedure reproductible ;
- une specification d'interface ;
- une justification d'architecture ;
- une decision historisee.

Le resultat est plus maintenable pour le SI : chaque changement a une place claire.

## Limites imposees

- Dossiers en kebab-case pour eviter les problemes cross-platform.
- `index.md` dans chaque sous-dossier pour decrire le contenu.
- Trois niveaux maximum pour limiter la desorientation.
- `adr/` cree des le depart pour capturer les decisions avant qu'elles soient oubliees.
