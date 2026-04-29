# Lancer avec Docker

## Construire l'image

Depuis la racine du projet :

```bash
docker build -t ms-validateur:local ms-validateur
```

## Lancer le conteneur seul

```bash
docker run --rm -p 8000:8000 ms-validateur:local
```

Verification :

```bash
curl http://localhost:8000/health
```

## Lancer avec Docker Compose

```bash
docker compose up -d ms-validateur
```

Verification :

```bash
curl http://localhost:8006/health
```

Dans le `docker-compose.yml` global, le service expose le port `8006` vers le port interne `8000`.
