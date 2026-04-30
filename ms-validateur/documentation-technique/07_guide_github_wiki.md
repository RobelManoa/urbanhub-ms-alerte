# 07 - Guide pour creer le GitHub Wiki

Ce guide explique comment publier la documentation technique de `ms-validateur` dans le GitHub Wiki du projet.

Lien public attendu du Wiki :

```text
https://github.com/RobelManoa/urbanhub-ms-alerte/wiki
```

Ce lien est aussi stocke dans le fichier `lien_wiki.txt` a la racine du projet.

## 1. Activer le Wiki GitHub

Sur GitHub :

1. Ouvrir le repository.
2. Aller dans `Settings`.
3. Descendre jusqu'a la section `Features`.
4. Cocher `Wikis`.
5. Revenir sur l'onglet `Wiki`.

Si l'onglet `Wiki` n'apparait pas, verifier que le repository est bien accessible avec les droits d'administration.

## 2. Creer la page d'accueil

Dans l'onglet `Wiki`, cliquer sur `Create the first page`.

Nom de la page :

```text
Home
```

Contenu conseille :

```markdown
# Wiki UrbanHub - ms-validateur

Ce Wiki documente le microservice `ms-validateur`, charge de valider les donnees capteurs et les fenetres de trafic avant leur passage vers `ms-analyse`.

## Pages principales

- 01 - Presentation du microservice
- 02 - Pipeline CI/CD
- 03 - SonarCloud High/Critical
- 04 - Snyk
- 05 - Guide de prise en main
- 06 - Evolutivite et integration UrbanHub

## Documentation source

La documentation source se trouve dans le repository :

- `ms-validateur/documentation-technique/`
- `ms-validateur/docs/`
```

Enregistrer avec `Save Page`.

## 3. Ajouter les six pages demandees

Creer ensuite les pages suivantes dans le Wiki.

| Page Wiki | Fichier source a copier |
|---|---|
| `01 - Presentation du microservice` | `ms-validateur/documentation-technique/01_presentation.md` |
| `02 - Pipeline CI CD` | `ms-validateur/documentation-technique/02_pipeline.md` |
| `03 - SonarCloud High Critical` | `ms-validateur/documentation-technique/03_sonarcloud.md` |
| `04 - Snyk` | `ms-validateur/documentation-technique/04_snyk.md` |
| `05 - Guide de prise en main` | `ms-validateur/documentation-technique/05_guide_prise_en_main.md` |
| `06 - Evolutivite et integration UrbanHub` | `ms-validateur/documentation-technique/06_evolutivite.md` |

Pour chaque page :

1. Cliquer sur `New Page`.
2. Mettre le nom de la page.
3. Copier le contenu du fichier `.md` correspondant.
4. Cliquer sur `Save Page`.

## 4. Ajouter une sidebar

Dans le Wiki, creer une page speciale nommee :

```text
_Sidebar
```

Contenu conseille :

```markdown
## ms-validateur

- [Accueil](Home)
- [01 - Presentation](01---Presentation-du-microservice)
- [02 - Pipeline CI/CD](02---Pipeline-CI-CD)
- [03 - SonarCloud](03---SonarCloud-High-Critical)
- [04 - Snyk](04---Snyk)
- [05 - Guide de prise en main](05---Guide-de-prise-en-main)
- [06 - Evolutivite](06---Evolutivite-et-integration-UrbanHub)
```

GitHub transforme automatiquement les titres de pages en liens. Si un lien ne fonctionne pas, ouvrir la page dans le Wiki et copier son URL exacte.

## 5. Verifier le rendu

Verifier les points suivants :

- la page `Home` existe ;
- les six pages demandees sont visibles ;
- les tableaux Markdown s'affichent correctement ;
- les blocs de code sont lisibles ;
- la sidebar permet de naviguer entre les pages ;
- le lien public du Wiki fonctionne sans authentification si le repository est public.

## 6. Mettre a jour le livrable `lien_wiki.txt`

Le fichier `lien_wiki.txt` doit contenir uniquement le lien public du Wiki :

```text
https://github.com/RobelManoa/urbanhub-ms-alerte/wiki
```

Ne pas ajouter de commentaire dans ce fichier si l'evaluation attend seulement une URL.

## 7. Variante avec clone du Wiki

GitHub Wiki est aussi un repository Git separe. Il peut etre clone comme ceci :

```bash
git clone git@github.com:RobelManoa/urbanhub-ms-alerte.wiki.git
```

Ensuite, copier les fichiers Markdown dedans, puis faire :

```bash
git add .
git commit -m "docs: add ms-validateur wiki"
git push
```

Cette variante est pratique si on veut garder un historique propre, mais la creation depuis l'interface GitHub suffit pour le rendu final.
