# Documentation technique ms-validateur

Cette documentation applique la methode Diataxis au systeme d'information du microservice `ms-validateur`.

Diataxis separe la documentation selon le besoin du lecteur :

| Type | Question principale | Dossier |
|---|---|---|
| Tutoriels | Comment apprendre par une premiere realisation guidee ? | `tutorials/` |
| Guides pratiques | Comment accomplir une tache precise ? | `how-to-guides/` |
| Reference | Quels sont les contrats, commandes et configurations exactes ? | `reference/` |
| Explications | Pourquoi le systeme est structure ainsi ? | `explanation/` |
| ADR | Quelles decisions d'architecture ont ete prises ? | `adr/` |

## Application au SI UrbanHub

Dans le systeme d'information UrbanHub, `ms-validateur` joue le role de controle qualite entre la collecte IoT et l'analyse. La documentation est donc organisee pour couvrir :

- l'onboarding d'un nouveau developpeur ;
- l'exploitation locale et CI/CD ;
- les contrats d'API, seuils et rapports qualite/securite ;
- les choix d'architecture et d'evolutivite ;
- la conservation des decisions via des ADR.

## Regles d'arborescence

- Les dossiers sont en minuscules avec des tirets, au format kebab-case.
- Chaque sous-dossier contient un `index.md`.
- L'arborescence est limitee a 3 niveaux : `docs/<section>/<page>.md`.
- Le dossier `adr/` existe des le debut pour eviter de perdre les decisions d'architecture.

## Parcours recommande

1. Commencer par `tutorials/first-run.md`.
2. Utiliser `how-to-guides/` pour les actions courantes.
3. Consulter `reference/` pour les contrats exacts.
4. Lire `explanation/` pour comprendre l'integration UrbanHub.
5. Verifier `adr/` pour connaitre les decisions structurantes.
