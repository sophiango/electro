import json
from fastapi import FastAPI, Depends, BackgroundTasks
from typing import List
from sqlalchemy.orm import Session

from app.ai import generate_embedding, cosine_similarity, hybrid_score, summarize_results
from app.ingestion import fetch_layer, parse_feeders
from app.database import get_db
from app.repository import bulk_insert_feeders, get_all_feeders, generate_and_store_embeddings, insert_feedback
from app.database import engine
from app.base import Base
from app.schemas import FeedbackRequest, FeederResponse, QueryRequest

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/feeders", response_model=List[FeederResponse])
def list_feeders(db: Session = Depends(get_db)):
    feeders = get_all_feeders(db)
    return feeders

@app.post("/ingest")
def ingest_data(bg_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    features = fetch_layer()
    feeders = parse_feeders(features)
    bulk_insert_feeders(db, feeders)
    bg_tasks.add_task(generate_and_store_embeddings, db)
    return {"inserted": len(feeders)}

@app.post("/recommend")
def recommend(request: QueryRequest, db: Session = Depends(get_db)):
    generate_and_store_embeddings(db)
    query_embedding = generate_embedding(request.query)
    feeders = get_all_feeders(db)
    scores = []
    for feeder in feeders:
        if not feeder.embedding:
            continue
        embedding = json.loads(feeder.embedding)
        score = hybrid_score(cosine_similarity(embedding, query_embedding), feeder)
        scores.append([score, feeder])
    scores.sort(key=lambda x: x[0], reverse=True)
    top = [f for _,f in scores[:5]]
    analysis = summarize_results(request.query, top)
    return analysis

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    insert_feedback(
        db,
        request.query_text,
        request.feeder_id,
        request.rating
    )
    return {"status": "feedback recorded"}