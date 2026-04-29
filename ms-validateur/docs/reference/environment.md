# Variables d'environnement

| Variable | Valeur par defaut | Role |
|---|---|---|
| `RABBITMQ_HOST` | `localhost` | Hote RabbitMQ. |
| `RABBITMQ_INPUT_QUEUE` | `collecte_queue` | File consommee par le validateur. |
| `RABBITMQ_OUTPUT_QUEUE` | `validated_queue` | File publiee vers `ms-analyse`. |
| `ENABLE_RABBITMQ_CONSUMER` | `false` | Active le consumer RabbitMQ au demarrage. |

Dans `docker-compose.yml`, ces variables relient `ms-validateur` au broker RabbitMQ du SI UrbanHub.
