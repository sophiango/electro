from app.ingestion import fetch_layer, parse_feeders
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository import bulk_insert_feeders, get_all_feeders
from app.database import engine
from app.base import Base
from typing import List
from app.schemas import FeederResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/feeders", response_model=List[FeederResponse])
def list_feeders(db: Session = Depends(get_db)):
    feeders = get_all_feeders(db)
    return feeders

@app.post("/ingest")
def ingest_data(db: Session = Depends(get_db)):
    features = fetch_layer()
    feeders = parse_feeders(features)
    bulk_insert_feeders(db, feeders)
    return {"inserted": len(feeders)}