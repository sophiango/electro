# electro/PG&E Grid Intelligence Backend

A production-style backend service that ingests public electric grid planning data from PG&E’s ArcGIS REST API, normalizes it into a relational database, and exposes a REST API for querying and future AI-powered recommendations.

This project demonstrates:

- External API integration
- Data normalization and validation
- SQL schema design
- FastAPI backend architecture
- Dependency injection
- Clean separation between ORM and API schemas
- Foundation for AI-powered recommendations


This structure separates:

- Database layer (SQLAlchemy models)
- API layer (Pydantic schemas)
- Business logic
- Ingestion logic

---

## 🚀 Features

### 📡 Data Ingestion
- Fetches data from PG&E ArcGIS FeatureServer REST endpoint
- Parses nested `features → attributes`
- Normalizes ArcGIS timestamps (milliseconds → Python datetime)
- Bulk inserts into SQLite
- Snapshot-ready schema

### 🌐 REST API
- `GET /feeders` — List stored feeder records
- `POST /ingest` — Trigger ingestion from ArcGIS API

### 🧠 Backend Design Practices
- SQLAlchemy 2.x ORM
- Pydantic response models
- Dependency-injected DB sessions
- Defensive type normalization
- Modular and extensible architecture

---

## 🛠 Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Requests
- Pydantic
- Uvicorn
- NumPy (future vector similarity)
- python-dateutil (timestamp parsing)

---

## ⚙️ Setup

### 1 Clone Repository

```bash
git clone <your-repo-url>
cd electro
```

### 2 Clone Repository
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
If requirements.txt exists:
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python -m uvicorn app.main:app --reload
```

Open in browser. FastAPI swagger will appear

```http://127.0.0.1:8000/docs```

---

## License
MIT
