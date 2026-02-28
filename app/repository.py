from openai.types import Embedding

from app.ai import generate_embedding
from app.helper import feeder_to_text
from sqlalchemy.orm import Session
from app.models import Feeder, Feedback
from typing import List
import json

def bulk_insert_feeders(db: Session, feeders: List):
    for feeder_data in feeders:
        feeder = Feeder(**feeder_data)
        db.add(feeder)
    db.commit()

def insert_data(db: Session, feeder_data):
    feeder = Feeder(**feeder_data)
    db.add(feeder)
    db.commit()

def get_all_feeders(db: Session):
    return db.query(Feeder).all()

def generate_and_store_embeddings(db: Session):
    feeders = db.query(Feeder).limit(5).all()
    for feeder in feeders:
        if feeder.embedding:
            continue
        text = feeder_to_text(feeder)
        em_feeder = generate_embedding(text)
        feeder.embedding = json.dumps(em_feeder)
    db.commit()

def insert_feedback(db: Session, input: dict):
    if "query_text" not in input or "feeder_id" not in input or "rating" not in input:
        return
    feedback = Feedback(
        query_text=input.get("query_text"),
        feeder_id=input.get("feeder_id"),
        rating=input.get("rating")
    )
    db.add(feedback)
    db.commit()