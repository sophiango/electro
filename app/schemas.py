from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeederResponse(BaseModel):
    id: int
    substation_name: Optional[str]
    substation_id: Optional[str]
    voltage_kv: Optional[float]
    existing_dg: Optional[float]
    queued_dg: Optional[float]
    redacted: Optional[str]
    ungrounded_banks: Optional[str]
    division: Optional[str]
    last_update_on_map: Optional[datetime]
    geometry_x: Optional[float]
    geometry_y: Optional[float]
    embedding: Optional[str]

    class Config:
        from_attributes = True  # <-- SQLAlchemy 2.x compatible

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query_text: str
    feeder_id: int
    rating: Optional[int] = None