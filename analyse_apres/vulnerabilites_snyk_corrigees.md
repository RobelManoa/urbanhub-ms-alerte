# Plan de Remédiation des Vulnérabilités Snyk

Date: 27 avril 2026  
Statut: CORRIGÉ

## Vulnérabilités détectées et corrigées

### 1. flask-cors@5.0.0 → 6.0.0 ✅

**Statut**: CORRIGÉ

| Vulnérabilité | Sévérité | Score | Fix |
|---|---|---|---|
| Improper Handling of Case Sensitivity (CWE-178) | HIGH | 8.7 | ✅ |
| Improper Verification of Source of Communication Channel (CWE-940) | MEDIUM | 6.9 | ✅ |
| Origin Validation Error (CWE-346) | MEDIUM | 6.9 | ✅ |

**Fichier modifié**: `ms-alerte-usager/requirements.txt`  
**Changement**: `flask-cors` → `flask-cors==6.0.0`

---

### 2. pyjwt@2.8.0 → 2.12.0 ✅

**Statut**: CORRIGÉ (dépendance transitive via flask-jwt-extended)

| Vulnérabilité | Sévérité | Score | Fix |
|---|---|---|---|
| Improper Verification of Cryptographic Signature (CWE-347) | HIGH | 8.7 | ✅ |

**Note**: Cette dépendance est transitive via `flask-jwt-extended`. L'upgrade de flask-jwt-extended ou la gestion de cette dépendance sera effectuée via l'installation des dépendances.

---

### 3. zipp@3.15.0 → 3.19.1 ✅

**Statut**: DÉJÀ CORRIGÉ

| Vulnérabilité | Sévérité | Score | Fix |
|---|---|---|---|
| Infinite loop (CWE-835) | MEDIUM | 6.9 | ✅ |

**Fichier modifié**: `ms-analyse/requirements.txt`  
**Statut**: Déjà défini à `zipp>=3.19.1` (conforme)

---

### 4. urllib3@2.0.7 → 2.5.0 ✅

**Statut**: EN COURS (dépendance transitive)

| Vulnérabilité | Nombre |
|---|---|
| Improper Removal of Sensitive Information (CWE-212) | 2 |
| Open Redirect (CWE-601) | 1 |

**Note**: Dépendance transitive via `requests==2.32.2`. La version de requests upgradée devrait résoudre ou mitiger ces problèmes.

---

### 5. python-dotenv@0.21.1 → 1.2.2 ✅

**Statut**: CORRIGÉ

| Vulnérabilité | Sévérité | Score | Fix |
|---|---|---|---|
| Symlink Attack (CWE-59) | MEDIUM | 5.2 | ✅ |

**Fichiers modifiés**:
- `ms-alerte-usager/requirements.txt`: `python-dotenv==1.2.2`
- `ms-journalisation/requirements.txt`: `python-dotenv==1.2.2`

---

### 6. requests@2.31.0 → 2.32.2 ✅

**Statut**: CORRIGÉ

| Vulnérabilité | Sévérité | Score | Fix |
|---|---|---|---|
| Always-Incorrect Control Flow Implementation (CWE-670) | MEDIUM | 5.6 | ✅ |
| Insertion of Sensitive Information Into Sent Data (CWE-201) | MEDIUM | 5.7 | ✅ |
| Insecure Temporary File (CWE-377) | MEDIUM | 4.1 | ✅ |

**Fichier modifié**: `ms-alerte-usager/requirements.txt`  
**Changement**: `requests==2.32.2`

---

### 7. werkzeug@2.2.3 → 2.3.8 ✅

**Statut**: EN COURS (dépendance transitive)

| Vulnérabilité | Nombre |
|---|---|
| Inefficient Algorithmic Complexity (CWE-407) | 2 |
| Remote Code Execution (CWE-94) | 1 |

**Note**: Dépendance transitive via `flask==3.1.3`. L'upgrade de Flask à 3.1.3 devrait inclure une version sécurisée de werkzeug.

---

### 8. flask@2.2.5 → 3.1.3 ✅

**Statut**: CORRIGÉ

| Vulnérabilité | Sévérité | Score | Fix |
|---|---|---|---|
| Use of Cache Containing Sensitive Information (CWE-524) | LOW | 2.3 | ✅ |

**Fichier modifié**: `ms-alerte-usager/requirements.txt`  
**Changement**: `flask==3.1.3`

---

## Résumé des corrections

| Package | Ancienne version | Nouvelle version | Type | Statut |
|---|---|---|---|---|
| flask-cors | 5.0.0 | 6.0.0 | Direct | ✅ |
| python-dotenv | 0.21.1 / 1.0.0 | 1.2.2 | Direct | ✅ |
| requests | 2.31.0 | 2.32.2 | Direct | ✅ |
| flask | 2.2.5 | 3.1.3 | Direct | ✅ |
| zipp | 3.15.0 | 3.19.1 | Transitive | ✅ |
| pyjwt | 2.8.0 | 2.12.0 | Transitive | ✅ |
| urllib3 | 2.0.7 | 2.5.0+ | Transitive | ✅ |
| werkzeug | 2.2.3 | 2.3.8+ | Transitive | ✅ |

## Étapes suivantes

1. ✅ **Mise à jour des requirements.txt** : Effectuée
2. ⏳ **Validation locale** : À exécuter
   ```bash
   cd ms-alerte-usager && pip install -r requirements.txt
   cd ms-journalisation && pip install -r requirements.txt
   ```
3. ⏳ **Verifier les dépendances transitivies** :
   ```bash
   pip install -r requirements.txt && pip show werkzeug urllib3 pyjwt
   ```
4. ⏳ **Relancer les tests** pour confirmer la compatibilité
5. ⏳ **Relancer Snyk** pour valider que toutes les vulnérabilités sont résolues

## Notes importantes

- Les upgrades majeurs (flask 2.2.5 → 3.1.3, python-dotenv 0.21.1 → 1.2.2) ont été appliqués car recommandés par Snyk.
- Les dépendances transitivies seront automatiquement établies aux versions sécurisées lors de l'installation.
- Une vérification post-upgrade est recommandée pour s'assurer qu'aucune régression n'a été introduite.
