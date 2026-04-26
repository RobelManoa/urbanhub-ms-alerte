import os
from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.api.schemas import TrafficAnalysisRequest
from src.adapters.database.models import Base
from src.adapters.database.repository import SQLAlchemyDashboardRepository
from src.adapters.rabbitmq.consumer import RabbitMQConsumer
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.use_cases.analyze_traffic_use_case import AnalyzeTrafficUseCase
from src.domain.services import TrafficAnalysisService

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ms_analyse.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine)
dashboard_repository = SQLAlchemyDashboardRepository(SessionLocal)
analyze_traffic_use_case = AnalyzeTrafficUseCase(
    analysis_service=TrafficAnalysisService(),
    publisher=RabbitMQPublisher(),
    dashboard_repository=dashboard_repository,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    if os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true":
        consumer = RabbitMQConsumer(analyze_traffic_use_case)
        consumer_thread = Thread(target=consumer.start_consuming, daemon=True)
        consumer_thread.start()
    yield


app = FastAPI(title="ms-analyse", lifespan=lifespan)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/traffic/analyze")
def analyze_traffic(payload: TrafficAnalysisRequest) -> dict:
    return analyze_traffic_use_case.execute(payload.to_domain())


@app.get("/traffic/dashboard")
def list_dashboard_results() -> dict[str, list[dict]]:
    return {"items": dashboard_repository.list_recent()}
