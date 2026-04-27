import os
from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI

from src.adapters.api.routes import router, traffic_validation_use_case
from src.adapters.rabbitmq.consumer import RabbitMQConsumer


@asynccontextmanager
async def lifespan(_: FastAPI):
    if os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true":
        consumer = RabbitMQConsumer(traffic_validation_use_case)
        consumer_thread = Thread(target=consumer.start_consuming, daemon=True)
        consumer_thread.start()
    yield


app = FastAPI(title="ms-validateur", lifespan=lifespan)
app.include_router(router)