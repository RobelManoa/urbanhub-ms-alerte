# INsertion d'une nouvelle fonctionne (microservices) dans le projet

Nom du microservices : Validateur de donnée de capteur

role : porte de qualité entre la collecte IoT et le traitement d'évenements. Avant qu'une donnée brute capteur soit propagée sur le bus d'évenement, elle doit être validér et classifier selon des seuils définis

# tache à faire : 

- Créer le Microservices
- ecrire le test
- le dockeriser
- configurer son pipeline GitHub action complet avec Sonarqube et snyk
- produire les rapport d'analyse qualité et sécurité (avant et apres correction)

# flux du traitement : 

Capteur IoT (simuler) -- ms-collecte-iot -- ms-validateur -- ms-analyse

# À mettre dans le pipeline CI/CD du nouveau microservices

- test : pip install des dépendances + exécution pytest avec couverture – minimum 80 % du coverage (livrable attendu : rapport_tests.txt, rapport_test.xml , coverage.xml)

- quality : sonarqube + snyk + flake8 (sonar_avant.png, sonar_apres.png, snyk_avant.txt, snyk_apres.txt, flake8_avant/apres.txt)

- build construction de l’image docker, push vers ghcr.io ,puis docker run de verification : le conteneur doit démarrer et répondre sur le port 8000 (livrable attendu : image sur ghcr.io/[org]/ms-validateur:sha)

- deploy-staging : ajout du service ms-validateur dans le docker-compose.yml du projet general et lancement via docker-compose up ms-validateur (livrable attendu : services accessible sur le port 8006)


# spécification du microservices validateur (ms-validateur)

# Fonctionnalité 

le microservices ms-validateur expose un endpoint POST/validate. Il reçoit une donnée capteur et retourne sa classification selon les seuls  définis

# seuil de références

Capteur : CO2
Seuil modéré : 800
Seuil critique : 1000
Unité : Ppm

Capteur : Températur
Seuil modéré : 35
Seuil critique : 40
Unité : °C

Capteur : Noise
Seuil modéré : 70
Seuil critique : 85
Unité : DB

On doit ajouter au moins un capteur supplémentaire de notre choix avec seuil

# contrat d’interface

POST/validate – exemple d’entrée / sortie

entrée : {"sensor" : "co2", "value" : 500}
sortie : {"valid" : true, "level" : "normal", "sensor" : "co2", "value" : 500, "threshold" : 800, "timestamp" : "2026-04-27T09:00Z"}

# Phase de teste

effectuer au minimum 4 teste dans tests/test_validator.py
- test_normal : valeur < seuil modéré → level= "normal", valid= True
- test_moderate : valeur entre seuil modéré et critique → level = "moderate", valid=True
- test_critical : valeur ≥ seuil critique  → level = "critical", valid= False
- test_unknow : capteur non répertorié → level = "unknow", valid=False 

# Commande pytest + coverage à intégrer dans le job run-tests

pip install pytest pytest-cov coverage

pytest tests\
	--tb=short
	-- junitxml=03_rapport_tests/rapport_tests.xml
	--cov=src \
	--cov-report= term \
	-- cov-report = xml:03_rapport_tests/coverage.xml
	-- cov-fail-under=80 \ 2>&1 | tee 03_rapport_tests/rapport_tests.txt

# optimisation des developpement et structuration du code sonarqube obligatoire

exigence de maintenabilité : 
    • structurer le code de façon modulaire : séparer la configuration des seuils, la logique de validation et les routes FastAPI en fonctions ou modules distincts
    • une fonction ne doit pas avoir qu’une seule responsabilité – éviter les fonctions monolithiques
    • les noms de variables et de fonctions doivent être explicites
    • la complexité cyclonique de chaque fonction doit rester faible – sonarqube la mésure