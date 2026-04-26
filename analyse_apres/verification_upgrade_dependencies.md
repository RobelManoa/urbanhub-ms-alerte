# Vérification des upgrads de dépendances (Snyk remediation)

**Date de verification**: 26 avril 2026  
**Objectif**: Confirmer que tous les packages vulnerables ont been upgraded aux versions recommandées par Snyk

## 1) Dépendances corrigées dans ms-alerte-usager/requirements.txt

| Package | Version avant | Version après | Vulnerabilites remédiées | CVSS Score |
|---------|---------------|---------------|--------------------------|------------|
| flask-cors | 5.0.0 | 6.0.0 | CWE-178, CWE-940, CWE-346 | 7.5 |
| python-dotenv | unpinned (0.21.1) | 1.2.2 | CWE-59 | 7.5 |
| requests | 2.31.0 | 2.32.2 | CWE-670, CWE-201, CWE-377 | 6.5 |
| flask | 2.2.5 | 3.1.3 | CWE-524 | 5.3 |

## 2) Dépendances corrigées dans ms-journalisation/requirements.txt

| Package | Version avant | Version après | Vulnerabilites remédiées | CVSS Score |
|---------|---------------|---------------|--------------------------|------------|
| python-dotenv | 1.0.0 | 1.2.2 | CWE-59 | 7.5 |

## 3) Dépendances transitivesresolues automatiquement

Les packages suivants seront mis à jour automatiquement via `pip install`:

| Package | Motif de l'update | Minimum version recommandée |
|---------|-------------------|---------------------------|
| pyjwt | Dépendance transitive de flask-jwt-extended | 2.12.0 |
| urllib3 | Dépendance transitive de requests | 2.5.0 |
| werkzeug | Dépendance transitive de flask | 2.3.8 |
| zipp | Déjà conforme dans ms-analyse | 3.19.1 |

## 4) Services non affectés par les vulnerabilites

- **ms-analyse**: Pas de dépendances vulnerables directes. zipp déjà à version 3.19.1 (conforme)
- **ms-collecte-iot**: Pas de dépendances vulnérables directes

## 5) Prochaines etapes recommandees

### Validation immediatelocale (recommandé)
```bash
# Dans ms-alerte-usager
pip install -r requirements.txt
pytest

# Dans ms-journalisation
pip install -r requirements.txt
pytest
```

### Execution de la suite de tests globale
```bash
# À la racine du monorepo
python -m pytest ms-*/tests --cov=ms-* --cov-report=xml --cov-append
```

### Verificationdes versions transitivesaprès installation
```bash
pip list | grep -E "pyjwt|urllib3|werkzeug|zipp"
```

## 6) Traceabilite

- Audit trail complet: [vulnerabilites_snyk_corrigees.md](vulnerabilites_snyk_corrigees.md)
- Rapport Snyk apres remediation: [snyk_apres.txt](snyk_apres.txt)
- Fichiers modifies: 
  - [ms-alerte-usager/requirements.txt](../ms-alerte-usager/requirements.txt)
  - [ms-journalisation/requirements.txt](../ms-journalisation/requirements.txt)
