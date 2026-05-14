# Backend — Contract Intelligence AI

## Overview

FastAPI-based REST API backend for the Contract Intelligence AI platform. This service handles:

- **PDF Upload** — Receive and validate legal contract PDFs
- **Contract Tracking** — SQLite-based status tracking through the processing pipeline
- **Mock Services** — Simulated OCR, NLP, and RAG outputs for development & integration testing

---

## Quick Start

```bash
# 1. Activate virtual environment
contract_ai_env\Scripts\activate        # Windows
source contract_ai_env/bin/activate     # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the backend
uvicorn main:app --reload

# 4. Open API docs
# http://localhost:8000/docs
```

---

## API Endpoints

### System

| Method | Path      | Description           |
|--------|-----------|-----------------------|
| GET    | `/`       | API info & doc links  |
| GET    | `/health` | Liveness health check |

### Upload

| Method | Path          | Description                              |
|--------|---------------|------------------------------------------|
| POST   | `/api/upload` | Upload a PDF contract (max 20 MB)        |

**Request:** `multipart/form-data` with field `file` (PDF)

**Response (201):**
```json
{
  "contract_id": "a1b2c3d4-...",
  "filename": "contract.pdf",
  "status": "uploaded",
  "message": "File uploaded successfully"
}
```

### Contracts

| Method | Path                            | Description                       |
|--------|---------------------------------|-----------------------------------|
| GET    | `/api/contracts`                | List all contracts (paginated)    |
| GET    | `/api/contracts/{contract_id}`  | Get status of a specific contract |

**Query params for list:** `skip` (default 0), `limit` (default 20, max 100)

---

## Pydantic Schemas

All schemas live in `backend/schemas/`:

| File                 | Models                                                  |
|----------------------|---------------------------------------------------------|
| `ocr_schema.py`      | `OCRChunk`, `OCROutput`                                |
| `nlp_schema.py`      | `ClausePrediction`, `EntityPrediction`, `NLPOutput`    |
| `rag_schema.py`      | `RetrievedChunk`, `ChatRequest`, `ChatResponse`        |
| `contract_schema.py` | `ContractStatus`, `ContractMetadata`, `AnalysisResponse`, `UploadResponse` |

### Contract Status Workflow

```
uploaded → ocr_done → nlp_done → rag_indexed → completed
                                                    ↓
                                                  failed
```

---

## Mock Services

Located in `backend/services/`:

| File            | Function          | Purpose                                     |
|-----------------|-------------------|---------------------------------------------|
| `mock_ocr.py`   | `run_mock_ocr()`  | Simulates OCR text extraction (4 pages)     |
| `mock_nlp.py`   | `run_mock_nlp()`  | Returns 4 CUAD clauses + 11 NER entities   |
| `mock_rag.py`   | `run_mock_rag()`  | FAISS-like retrieval + LLM answer           |

**Targeted CUAD clauses:** Termination For Convenience, Renewal Term, Cap On Liability, Uncapped Liability

---

## Project Structure

```
backend/
├── __init__.py
├── api/
│   └── __init__.py
├── routes/
│   ├── __init__.py
│   ├── upload.py          # POST /api/upload
│   ├── contracts.py       # GET /api/contracts
│   ├── analyze.py         # POST /api/analyze
│   ├── risk.py            # GET /api/risk-score/{id}
│   └── chat.py            # POST /api/chat
├── schemas/
│   ├── __init__.py
│   ├── ocr_schema.py
│   ├── nlp_schema.py
│   ├── rag_schema.py
│   └── contract_schema.py
├── services/
│   ├── __init__.py
│   ├── tracking.py        # SQLite + SQLAlchemy
│   ├── pipeline.py        # Sequential pipeline orchestrator
│   ├── mock_ocr.py
│   ├── mock_nlp.py
│   └── mock_rag.py
├── utils/
│   └── __init__.py
└── README.md              # ← you are here
```

---

## Database

- **Engine:** SQLite via SQLAlchemy
- **Location:** `data/contracts.db`
- **Tables:** `contracts` (contract_id PK, filename, upload_time, status, error_message, file_size_bytes)

---

## Error Handling

| Status | Meaning                     |
|--------|-----------------------------| 
| 400    | Bad request / invalid input |
| 404    | Contract not found          |
| 413    | File too large (>20 MB)     |
| 415    | Unsupported file type       |
| 500    | Internal server error       |

---

## Progress

- [x] `/api/upload` — PDF upload with validation
- [x] `/api/contracts` — contract listing & status
- [x] `/api/analyze` — full pipeline orchestration (Day 8)
- [x] `/api/risk-score` — rule-based risk scoring endpoint (Day 10)
- [x] `/api/chat` — RAG chatbot with FAISS retrieval (Day 9)

## Next Steps

- [ ] Celery async task processing
- [ ] Real OCR/NLP/RAG integration (replace mocks)
- [ ] WebSocket support for live processing updates
- [ ] Authentication & authorization
