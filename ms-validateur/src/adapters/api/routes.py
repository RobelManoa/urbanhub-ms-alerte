from fastapi import APIRouter

from src.adapters.api.schemas import TrafficValidationRequest
from src.adapters.rabbitmq.publisher import RabbitMQPublisher
from src.application.validate_traffic_use_case import ValidateTrafficUseCase
from src.domain.sensor_validation import SensorValidationService
from src.domain.services import TrafficValidationService
from src.validator import Sensordata


router = APIRouter()

traffic_validation_use_case = ValidateTrafficUseCase(
    validation_service=TrafficValidationService(),
    publisher=RabbitMQPublisher(),
)
sensor_validation_service = SensorValidationService()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/traffic/validate")
def validate_traffic(payload: TrafficValidationRequest) -> dict:
    return traffic_validation_use_case.execute(payload.to_domain()).to_dict()


@router.post("/validate")
def validate_sensor(payload: Sensordata) -> dict:
    return sensor_validation_service.validate(sensor=payload.sensor, value=payload.value)