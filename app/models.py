from typing import Text
from app.base import Base
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, Text
import datetime

class Feeder(Base):
    __tablename__ = "feeders"

    id = Column(Integer, primary_key=True, index=True)

    redacted = Column(Boolean)
    ungrounded_banks = Column(String, nullable=True)
    existing_dg = Column(Integer)
    queued_dg = Column(Integer)
    voltage_kv = Column(Integer)
    substation_name = Column(String)
    substation_id = Column(String)
    division = Column(String)
    last_update_on_map = Column(DateTime)
    geometry_x = Column(Float)
    geometry_y = Column(Float)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    embedding = Column(Text, nullable=True)