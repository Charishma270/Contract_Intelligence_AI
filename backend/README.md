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

## Progress

- [x] `/api/upload` — PDF upload with validation
- [x] `/api/contracts` — contract listing & status
- [x] `/api/analyze` — full pipeline orchestration (Day 8)
- [x] `/api/chat` — RAG chatbot with FAISS retrieval (Day 9)
- [x] `/api/risk-score` — rule-based risk scoring endpoint (Day 10)
- [x] Comprehensive error handling & validation (Day 12)
- [x] Structured logging with JSON file output (Day 13)

## Next Steps

- [ ] Real OCR integration (Day 14)
- [ ] Celery async task processing
- [ ] Real NLP/RAG integration (replace mocks)
- [ ] Authentication & authorization
