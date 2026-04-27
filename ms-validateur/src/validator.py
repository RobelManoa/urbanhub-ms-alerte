import os
from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.adapters.rabbitmq.consumer import RabbitMQConsumer
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.validate_traffic_use_case import ValidateTrafficUseCase
from src.config.sensor_thresholds import SENSOR_THRESHOLDS as THRESHOLDS
from src.domain.services import TrafficValidationService


class Sensordata(BaseModel):
    sensor: str = Field(min_length=1)
    value: float = Field(ge=0)


traffic_validation_use_case = ValidateTrafficUseCase(
    validation_service=TrafficValidationService(),
    publisher=RabbitMQPublisher(),
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true":
        consumer = RabbitMQConsumer(traffic_validation_use_case)
        consumer_thread = Thread(target=consumer.start_consuming, daemon=True)
        consumer_thread.start()
    yield


def create_app() -> FastAPI:
    from src.adapters.api.routes import router

    app = FastAPI(title="ms-validateur", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()