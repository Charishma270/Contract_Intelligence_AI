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
│   ├── rag.py             # FAISS RAG retrieval service
│   ├── mock_ocr.py
│   ├── mock_nlp.py
│   └── mock_rag.py
├── utils/
│   ├── __init__.py
│   ├── exceptions.py      # Centralized exception hierarchy  [NEW Day 12]
│   ├── validators.py      # Reusable request validators       [NEW Day 12]
│   └── logging_config.py  # Structured logging setup          [NEW Day 13]
└── README.md              # ← you are here
```

---

## Database

- **Engine:** SQLite via SQLAlchemy
- **Location:** `data/contracts.db`
- **Tables:** `contracts` (contract_id PK, filename, upload_time, status, error_message, file_size_bytes)

---

## Error Handling

### HTTP Status Codes

| Status | Meaning                     |
|--------|-----------------------------| 
| 400    | Bad request / invalid input |
| 404    | Contract not found          |
| 413    | File too large (>20 MB)     |
| 415    | Unsupported file type       |
| 500    | Internal server error       |

### Error Response Format (Day 12)

All errors return a consistent JSON structure:

```json
{
  "detail": "Human-readable error message",
  "error_type": "ContractNotFoundError",
  "path": "/api/contracts/invalid-id"
}
```

### Custom Exception Types

| Exception | Status | When |
|-----------|--------|------|
| `InvalidContractIdError` | 400 | contract_id is not a valid UUID |
| `ContractNotFoundError` | 404 | contract_id doesn't exist in DB |
| `ContractAlreadyFailedError` | 400 | Contract previously failed processing |
| `ContractNotAnalyzedError` | 400 | Contract hasn't been analyzed yet |
| `EmptyQueryError` | 400 | Chat query is empty/whitespace |
| `EmptyFileError` | 400 | Uploaded file is 0 bytes |
| `FileTooLargeError` | 413 | File exceeds 20 MB limit |
| `UnsupportedFileTypeError` | 415 | Non-PDF file uploaded |
| `PipelineError` | 500 | Pipeline stage failure |

### Validation Features (Day 12)

- **UUID format validation** on all contract_id path parameters
- **PDF magic byte check** on upload (validates `%PDF-` header)
- **Empty file rejection** on upload
- **Query sanitization** on chat endpoint
- **Contract status checks** before analysis and risk scoring
- **X-Request-ID** header on all responses for traceability

---

## Logging (Day 13)

### Architecture

- **Module:** `backend/utils/logging_config.py`
- **Logger hierarchy:** All modules use `contract_ai.*` (e.g., `contract_ai.upload`, `contract_ai.pipeline`)
- **One-call setup:** `setup_logging()` called during app startup in `main.py`

### Output Destinations

| Destination | Format | Handler |
|-------------|--------|---------|
| Console (stdout) | Colored, human-readable | `StreamHandler` |
| File (`logs/contract_ai.log`) | JSON Lines | `TimedRotatingFileHandler` |

### JSON Log Fields

```json
{
  "timestamp": "2026-05-20T09:00:00+00:00",
  "level": "INFO",
  "logger": "contract_ai.upload",
  "message": "Uploaded contract abc-123",
  "request_id": "a1b2c3d4",
  "module": "upload",
  "funcName": "upload_contract",
  "lineno": 95
}
```

### Configuration

| Setting | Default | Override |
|---------|---------|----------|
| Log level | `INFO` | `LOG_LEVEL` env var or `setup_logging(log_level=...)` |
| Log directory | `logs/` | `setup_logging(log_dir=...)` |
| Rotation | Daily at midnight | Built-in |
| Retention | 30 days | Built-in |

### Request Context

- Every HTTP request gets a unique `request_id` (8-char UUID prefix)
- The `request_id` is injected into all log lines via `contextvars.ContextVar` (async-safe)
- Also returned as `X-Request-ID` response header
- Request/response pairs are logged: `→ GET /api/contracts` / `← GET /api/contracts status=200`

---

## Configuration (Day 20)

All backend settings are centralized in `backend/config.py` and read from environment variables at startup. Each setting has a sensible default for local development.

### Quick Setup

```bash
# 1. Copy the template
cp .env.example .env

# 2. Edit for your environment
# (defaults work for local development)

# 3. Start the backend
uvicorn main:app --reload
```

### Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | Environment: development, staging, production |
| `DEBUG` | `false` | Enable debug mode (true/false) |
| `PORT` | `8000` | Server port |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins |
| `MAX_FILE_SIZE_MB` | `20` | Maximum upload file size in MB |
| `DATABASE_DIR` | `data` | SQLite database directory |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `LOG_DIR` | `logs` | Log file directory |
| `OCR_POPPLER_PATH` | (Windows default) | Path to Poppler bin directory |
| `OCR_TESSERACT_CMD` | (Windows default) | Path to Tesseract executable |
| `OCR_DPI` | `300` | DPI for PDF-to-image conversion |
| `NLP_CONFIDENCE_THRESHOLD` | `0.30` | Clause detection confidence threshold |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery broker URL |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/1` | Celery result backend URL |

See `.env.example` for the complete list.

### Usage in Code

```python
from backend.config import settings

# Access any setting
print(settings.APP_VERSION)      # "0.6.0"
print(settings.MAX_FILE_SIZE_MB) # 20
print(settings.DATABASE_URL)     # "sqlite:///data/contracts.db"
```

---

## Progress

- [x] `/api/upload` — PDF upload with validation
- [x] `/api/contracts` — contract listing & status
- [x] `/api/analyze` — full pipeline orchestration (Day 8)
- [x] `/api/chat` — RAG chatbot with FAISS retrieval (Day 9)
- [x] `/api/risk-score` — rule-based risk scoring endpoint (Day 10)
- [x] Comprehensive error handling & validation (Day 12)
- [x] Structured logging with JSON file output (Day 13)
- [x] Real OCR integration — pdfplumber + Tesseract (Day 14)
- [x] Real NLP integration — Legal-BERT + spaCy NER (Day 15)
- [x] E2E pipeline validation (Day 16)
- [x] Celery async task processing (Day 17)
- [x] Vector DB inspection endpoints (Day 18)
- [x] Frontend API contract finalization (Day 19)
- [x] Centralized config & environment variables (Day 20)
- [x] Week 3 integration demo tests (Day 21)

## Next Steps (Week 4)

- [ ] Backend Dockerfile (Day 22)
- [ ] Docker Compose integration (Day 23)
- [ ] AWS EC2 deployment prep (Day 24)
- [ ] Load testing with Locust (Day 25)
- [ ] Comprehensive test suite (Day 26)
- [ ] Final docs & architecture diagram (Day 27)
- [ ] Demo day & handover (Day 28)

