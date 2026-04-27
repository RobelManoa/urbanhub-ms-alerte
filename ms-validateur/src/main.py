import os
from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI

from src.adapters.api.schemas import SensorValidationRequest, TrafficValidationRequest
from src.adapters.rabbitmq.consumer import RabbitMQConsumer
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.validate_traffic_use_case import ValidateTrafficUseCase
from src.domain.sensor_validation import SensorValidationService
from src.domain.services import TrafficValidationService


traffic_validation_use_case = ValidateTrafficUseCase(
    validation_service=TrafficValidationService(),
    publisher=RabbitMQPublisher(),
)
sensor_validation_service = SensorValidationService()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true":
        consumer = RabbitMQConsumer(traffic_validation_use_case)
        consumer_thread = Thread(target=consumer.start_consuming, daemon=True)
        consumer_thread.start()
    yield


app = FastAPI(title="ms-validateur", lifespan=lifespan)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/traffic/validate")
def validate_traffic(payload: TrafficValidationRequest) -> dict:
    return traffic_validation_use_case.execute(payload.to_domain()).to_dict()


@app.post("/validate")
def validate_sensor(payload: SensorValidationRequest) -> dict:
    return sensor_validation_service.validate(sensor=payload.sensor, value=payload.value)