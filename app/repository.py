from sqlalchemy.orm import Session
from app.models import Feeder
from typing import List

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