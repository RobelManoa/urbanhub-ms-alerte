from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TrafficAnalysisRecord(Base):
    __tablename__ = "traffic_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(String, nullable=False, index=True)
    zone_id = Column(String, nullable=False, index=True)
    traffic_state = Column(String, nullable=False)
    average_speed_kmh = Column(Float, nullable=False)
    vehicle_count = Column(Integer, nullable=False)
    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
