# Executer les tests et generer les rapports

Depuis `ms-validateur/` :

```bash
mkdir -p 03_rapport_tests
pytest tests \
  --tb=short \
  --junitxml=03_rapport_tests/rapport_tests.xml \
  --cov=src \
  --cov-report=term \
  --cov-report=xml:03_rapport_tests/coverage.xml \
  --cov-fail-under=80 \
  2>&1 | tee 03_rapport_tests/rapport_tests.txt
cp 03_rapport_tests/rapport_tests.xml 03_rapport_tests/rapport_test.xml
```

## Livrables produits

- `03_rapport_tests/rapport_tests.txt`
- `03_rapport_tests/rapport_tests.xml`
- `03_rapport_tests/rapport_test.xml`
- `03_rapport_tests/coverage.xml`

## Qualite locale

```bash
flake8 src tests --config=.flake8
```

Le rapport apres correction est stocke dans `reports/quality/flake8_apres.txt`.
