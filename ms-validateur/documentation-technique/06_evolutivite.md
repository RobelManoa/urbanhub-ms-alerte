# 06 - Evolutivite et integration UrbanHub

## Integration actuelle

`ms-validateur` est integre au systeme UrbanHub comme service de controle entre la collecte IoT et l'analyse.

Flux actuel :

```text
ms-collecte-iot -> collecte_queue -> ms-validateur -> validated_queue -> ms-analyse
```

Dans `docker-compose.yml`, le service depend de RabbitMQ et expose :

```text
8006:8000
```

Le port interne reste `8000`, tandis que le port accessible depuis l'exterieur du compose est `8006`.

## Integration dans docker-compose.yml

Le service `ms-validateur` a ete ajoute dans le `docker-compose.yml` general du projet UrbanHub.

Configuration principale :

```yaml
ms-validateur:
  build:
    context: ./ms-validateur
  container_name: ms-validateur
  depends_on:
    rabbitmq:
      condition: service_healthy
  ports:
    - "8006:8000"
  environment:
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_INPUT_QUEUE: collecte_queue
    RABBITMQ_OUTPUT_QUEUE: validated_queue
    ENABLE_RABBITMQ_CONSUMER: "true"
  command: ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
  restart: unless-stopped
```

Le service utilise le reseau Docker Compose par defaut du projet. Il n'y a donc pas besoin de declarer un reseau specifique pour que `ms-validateur` parle avec RabbitMQ : le nom DNS interne `rabbitmq` suffit.

Dans ce reseau interne :

- `ms-collecte-iot` publie vers `collecte_queue` ;
- `ms-validateur` consomme `collecte_queue` ;
- `ms-validateur` republie vers `validated_queue` ;
- `ms-analyse` consomme `validated_queue`.

Le port `8006` sert surtout aux tests locaux et a la verification staging. Les autres microservices communiquent principalement par RabbitMQ.

## Ajout de nouveaux capteurs

L'ajout d'un capteur est ne sera pas compliquer. Il faut modifier :

```text
src/config/sensor_thresholds.py
```

Exemple :

```python
"air_quality": SensorThreshold(moderate=50, critical=80, unit="aqi")
```

Puis ajouter un test dans `tests/` pour verifier le comportement attendu.

Cette approche evite de toucher aux routes API pour chaque nouveau capteur.

## Evolution des seuils

Dans cette version, les seuils sont dans le code. C'est simple, versionne et suffisant pour un premier microservice.

Pour une version plus avancee, les seuils pourraient venir :

- d'un fichier de configuration par environnement ;
- d'une base de donnees ;
- d'un service de configuration central ;
- d'une configuration par zone urbaine.

## Scalabilite

Le service peut etre replique tant que le traitement reste stateless.

Avec RabbitMQ, plusieurs instances peuvent consommer la file `collecte_queue`. Il faudra simplement surveiller :

- l'idempotence du traitement ;
- la gestion des erreurs de publication ;
- les logs des messages rejetes ;
- la consommation concurrente.

## Deploiement cloud avec Kubernetes

Dans une infrastructure Kubernetes, `ms-validateur` peut etre deploye comme un microservice stateless.

L'image construite par le pipeline serait publiee dans GHCR :

```text
ghcr.io/<org>/ms-validateur:<sha>
```

Puis Kubernetes utiliserait cette image dans un `Deployment`. Le conteneur exposerait toujours le port interne `8000`.

Exemple de principe :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ms-validateur
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ms-validateur
  template:
    metadata:
      labels:
        app: ms-validateur
    spec:
      containers:
        - name: ms-validateur
          image: ghcr.io/<org>/ms-validateur:<sha>
          ports:
            - containerPort: 8000
          env:
            - name: RABBITMQ_HOST
              value: rabbitmq
            - name: RABBITMQ_INPUT_QUEUE
              value: collecte_queue
            - name: RABBITMQ_OUTPUT_QUEUE
              value: validated_queue
            - name: ENABLE_RABBITMQ_CONSUMER
              value: "true"
```

Un `Service` Kubernetes exposerait ensuite `ms-validateur` a l'interieur du cluster :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ms-validateur
spec:
  selector:
    app: ms-validateur
  ports:
    - port: 8000
      targetPort: 8000
```

Pour l'acces externe, deux options sont possibles :

- utiliser un `Ingress` si l'API doit etre exposee publiquement ;
- garder le service en `ClusterIP` si `ms-validateur` reste uniquement consomme par les autres services UrbanHub.

RabbitMQ serait aussi deploye dans Kubernetes, ou fourni par un service manage. Dans les deux cas, `RABBITMQ_HOST` doit pointer vers le nom DNS interne du broker, par exemple `rabbitmq` ou `rabbitmq.default.svc.cluster.local`.

Les secrets techniques, comme les tokens de scan ou les identifiants d'un registre prive, ne doivent pas etre ecrits dans les manifests. Ils doivent etre fournis via `Secret` Kubernetes ou via le gestionnaire de secrets de la plateforme cloud.

## Observabilite

Les ameliorations utiles pour la production seraient :

- logs structures en JSON ;
- metriques Prometheus ;
- compteur de validations par niveau ;
- compteur de messages rejetes ;
- traces des publications vers `validated_queue`.

Ces elements aideraient a suivre la qualite des donnees dans le SI (System d'Information) UrbanHub.

## Integration future avec UrbanHub

Le microservice peut evoluer vers un role plus central de validation des donnees urbaines :

- validation de nouveaux types de capteurs ;
- regles differentes selon les zones ;
- enrichissement avec l'unite et la source du seuil ;
- stockage des validations critiques ;
- notification vers un service d'alerte.

La structure actuelle facilite ces evolutions, car les responsabilites sont deja separees entre configuration, domaine, API et RabbitMQ.

## Lien avec les decisions d'architecture

Les decisions importantes sont documentees dans :

```text
ms-validateur/docs/adr/
```
