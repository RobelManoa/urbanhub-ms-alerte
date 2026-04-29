# Reference qualite et securite

## SonarCloud

Configuration : `sonar-project.properties`

Parametres :

- `sonar.sources=src`
- `sonar.tests=tests`
- `sonar.python.coverage.reportPaths=03_rapport_tests/coverage.xml`
- `sonar.python.xunit.reportPath=03_rapport_tests/rapport_tests.xml`
- `sonar.python.flake8.reportPaths=reports/quality/flake8_apres.txt`

## Flake8

Rapports :

- `reports/quality/flake8_avant.txt`
- `reports/quality/flake8_apres.txt`

## Snyk

Rapports :

- `reports/security/snyk_avant.txt`
- `reports/security/snyk_apres.txt`

Le scan complet est produit en CI lorsque `SNYK_TOKEN` est configure.

## Tests et couverture

Rapports :

- `03_rapport_tests/rapport_tests.txt`
- `03_rapport_tests/rapport_tests.xml`
- `03_rapport_tests/rapport_test.xml`
- `03_rapport_tests/coverage.xml`
