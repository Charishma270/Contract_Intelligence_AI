# API Reference — Contract Intelligence AI

> **Version:** 0.6.0 · **Base URL:** `http://localhost:8000`

All endpoints return JSON. Errors follow a consistent envelope:
```json
{ "detail": "Human-readable message", "error_type": "ExceptionClass", "path": "/api/..." }
```

Every response includes headers:
- `X-Request-ID` — 8-character UUID prefix for tracing
- `X-Process-Time` — seconds elapsed on the server

---

## Table of Contents

1. [System](#system)
2. [Upload](#upload)
3. [Contracts](#contracts)
4. [Analysis — Sync](#analysis--sync)
5. [Risk Score](#risk-score)
6. [Chat (RAG)](#chat-rag)
7. [Async Analysis](#async-analysis)
8. [Task Management](#task-management)
9. [Vector DB Inspection](#vector-db-inspection)
10. [Error Reference](#error-reference)

---

## System

### `GET /`

Root info — returns links and endpoint map.

**Response 200:**
```json
{
  "message": "Contract Intelligence AI API",
  "docs": "/docs",
  "health": "/health",
  "endpoints": { "upload": "POST /api/upload", "..." : "..." }
}
```

---

### `GET /health`

Liveness probe used by Docker healthchecks and load balancers.

**Response 200:**
```json
{
  "status": "ok",
  "service": "Contract Intelligence AI",
  "version": "0.6.0",
  "environment": "production"
}
```

---

## Upload

### `POST /api/upload`

Upload a PDF contract. On success the file is saved, an OCR + FAISS ingestion
pipeline runs, and a contract tracking record is created.

**Request:** `multipart/form-data`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `file` | File | ✅ | PDF only, max 20 MB |

**Validation rules:**
- File extension must be `.pdf`
- MIME type must be `application/pdf`
- File must not be empty (0 bytes)
- File must begin with `%PDF-` magic bytes
- File size must not exceed `MAX_FILE_SIZE_MB` (default 20 MB)

**Response 201:**
```json
{
  "contract_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "service_agreement.pdf",
  "status": "uploaded",
  "message": "File uploaded and 14 chunks indexed successfully",
  "timestamp": "2026-06-12T10:00:00Z",
  "file_size_bytes": 1048576
}
```

**Errors:**

| Status | Error Type | Reason |
|--------|-----------|--------|
| 400 | `EmptyFileError` | Zero-byte file |
| 413 | `FileTooLargeError` | File exceeds size limit |
| 415 | `UnsupportedFileTypeError` | Non-PDF extension, MIME, or magic bytes |
| 422 | Validation Error | Missing `file` field |

---

## Contracts

### `GET /api/contracts`

List all uploaded contracts, newest first, with pagination.

**Query Parameters:**

| Param | Type | Default | Constraints |
|-------|------|---------|------------|
| `skip` | int | `0` | `>= 0` |
| `limit` | int | `20` | `1–100` |

**Response 200:** Array of `ContractMetadata` objects.
```json
[
  {
    "contract_id": "a1b2c3d4-...",
    "filename": "service_agreement.pdf",
    "upload_time": "2026-06-12T10:00:00",
    "status": "completed",
    "error_message": null,
    "file_size_bytes": 1048576
  }
]
```

**Contract Status Values:**

| Value | Meaning |
|-------|---------|
| `uploaded` | File saved, not yet analyzed |
| `processing` | Async pipeline in progress |
| `ocr_done` | Text extraction complete |
| `nlp_done` | Clause classification complete |
| `rag_indexed` | FAISS indexing complete |
| `completed` | Full pipeline done |
| `failed` | Pipeline error — see `error_message` |

---

### `GET /api/contracts/{contract_id}`

Get status and metadata for a specific contract.

**Path Parameters:**

| Param | Type | Notes |
|-------|------|-------|
| `contract_id` | UUID string | Must be valid UUID v4 |

**Response 200:** `ContractMetadata` object (same shape as list item above).

**Errors:**

| Status | Error Type | Reason |
|--------|-----------|--------|
| 400 | `InvalidContractIdError` | Not a valid UUID format |
| 404 | `ContractNotFoundError` | No contract with that ID |

---

## Analysis — Sync

### `POST /api/analyze/{contract_id}`

Run the full synchronous 4-stage analysis pipeline:
1. **OCR** — pdfplumber + Tesseract text extraction
2. **NLP** — Legal-BERT clause classification + spaCy NER
3. **RAG Indexing** — FAISS embedding storage
4. **Risk Scoring** — Rule-based risk computation

**Path Parameters:**

| Param | Type | Notes |
|-------|------|-------|
| `contract_id` | UUID string | Must be valid UUID v4 |

**Response 200:**
```json
{
  "contract_id": "a1b2c3d4-...",
  "filename": "service_agreement.pdf",
  "status": "completed",
  "risk_score": 65,
  "risk_severity": "high",
  "clauses": [
    {
      "clause_type": "Termination For Convenience",
      "answer_text": "Either party may terminate with 30 days notice.",
      "confidence": 0.94,
      "is_present": true,
      "page": 3,
      "page_label": null
    }
  ],
  "entities": [
    {
      "text": "Acme Corp",
      "label": "ORG",
      "start": 42,
      "end": 51,
      "confidence": 0.99
    }
  ],
  "risk_breakdown": [
    {
      "factor": "Base Contract Risk",
      "score": 30,
      "severity": "low",
      "description": "Baseline risk inherent in any legal contract."
    }
  ]
}
```

**Errors:**

| Status | Error Type | Reason |
|--------|-----------|--------|
| 400 | `InvalidContractIdError` | Not a valid UUID |
| 400 | `ContractAlreadyFailedError` | Contract previously failed |
| 404 | `ContractNotFoundError` | No contract with that ID |
| 500 | `PipelineError` | Stage failure (OCR/NLP/RAG/Risk) |

---

## Risk Score

### `GET /api/risk/risk-score/{contract_id}`

Compute and return the risk score for a contract using the NLP clause output.

**Path Parameters:**

| Param | Type | Notes |
|-------|------|-------|
| `contract_id` | UUID string | Must exist in the database |

**Risk Rules:**

| Clause Detected | Score Change | Severity |
|----------------|-------------|---------|
| Base contract risk | +30 | low |
| Auto-renewal clause | +20 | medium |
| Uncapped liability | +30 | high |
| Termination for convenience | -5 | low |
| Liability cap present | -10 | low |

**Severity Thresholds:**

| Score | Severity |
|-------|---------|
| 0–24 | `low` |
| 25–49 | `medium` |
| 50–74 | `high` |
| 75–100 | `critical` |

**Response 200:**
```json
{
  "contract_id": "a1b2c3d4-...",
  "overall_risk": 65,
  "severity": "high",
  "breakdown": [
    { "factor": "Base Contract Risk", "score": 30, "severity": "low", "description": "..." },
    { "factor": "Auto-Renewal Clause", "score": 20, "severity": "medium", "description": "..." }
  ]
}
```

**Errors:**

| Status | Error Type | Reason |
|--------|-----------|--------|
| 400 | `InvalidContractIdError` | Not a valid UUID |
| 404 | `ContractNotFoundError` | No contract with that ID |

---

## Chat (RAG)

### `POST /api/chat/chat`

Ask a natural language question about a contract. Uses hybrid FAISS + BM25
retrieval augmented generation.

**Request Body:**
```json
{
  "contract_id": "a1b2c3d4-...",
  "query": "What are the termination notice requirements?"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `contract_id` | UUID string | ✅ | Must exist |
| `query` | string | ✅ | Non-empty |

**Response 200:**
```json
{
  "answer": "The contract requires 30 days written notice for termination...",
  "retrieved_chunks": [
    {
      "text": "Either party may terminate this agreement...",
      "score": 0.87,
      "page": 3,
      "contract_id": "a1b2c3d4-..."
    }
  ],
  "citations": ["Page 3", "Section 12.1"]
}
```

**Errors:**

| Status | Error Type | Reason |
|--------|-----------|--------|
| 400 | `InvalidContractIdError` | Not a valid UUID |
| 400 | `EmptyQueryError` | Query is empty or whitespace |
| 404 | `ContractNotFoundError` | No contract with that ID |
| 500 | Internal | RAG pipeline error |

---

## Async Analysis

### `POST /api/analyze/{contract_id}/async`

Submit a contract for async analysis via Celery. Returns immediately with a
`task_id` for polling — use this for large documents that would time out a
synchronous request.

**Path Parameters:**

| Param | Type | Notes |
|-------|------|-------|
| `contract_id` | UUID string | Must not be in FAILED status |

**Response 202:**
```json
{
  "task_id": "celery-abc123-def456",
  "contract_id": "a1b2c3d4-...",
  "status": "processing",
  "message": "Analysis task submitted for contract 'agreement.pdf'. Poll GET /api/tasks/celery-abc123-def456 for progress."
}
```

**Errors:**

| Status | Error Type | Reason |
|--------|-----------|--------|
| 400 | `InvalidContractIdError` | Not a valid UUID |
| 400 | `ContractAlreadyFailedError` | Contract previously failed |
| 404 | `ContractNotFoundError` | No contract with that ID |

---

## Task Management

### `GET /api/tasks/{task_id}`

Poll the status of an async analysis task.

**Path Parameters:**

| Param | Type |
|-------|------|
| `task_id` | string (Celery task ID) |

**Task States:**

| State | Meaning |
|-------|---------|
| `PENDING` | Queued, not yet started |
| `STARTED` | Worker received the task |
| `PROGRESS` | Running — includes `progress.stage` and `progress.percent` |
| `SUCCESS` | Complete — `result` contains `AnalysisResponse` |
| `FAILURE` | Failed — `error` contains detail string |
| `REVOKED` | Cancelled |

**Response 200:**
```json
{
  "task_id": "celery-abc123-def456",
  "state": "PROGRESS",
  "progress": { "stage": "nlp", "percent": 50 },
  "result": null,
  "error": null
}
```

---

### `POST /api/tasks/{task_id}/revoke`

Cancel a pending or running async analysis task.

**Response 200:**
```json
{
  "task_id": "celery-abc123-def456",
  "status": "revoked",
  "message": "Task celery-abc123-def456 has been revoked. If the task was running, it will be terminated."
}
```

---

## Vector DB Inspection

### `GET /api/vectordb/status`

Return FAISS index health and statistics.

**Response 200:**
```json
{
  "total_vectors": 142,
  "dimension": 384,
  "index_type": "FlatL2",
  "metadata_count": 142,
  "bm25_ready": true
}
```

**Errors:**

| Status | Reason |
|--------|--------|
| 503 | FAISS index not loaded or empty |

---

### `GET /api/vectordb/chunks`

Paginated listing of stored chunks (text metadata).

**Query Parameters:**

| Param | Default | Range |
|-------|---------|-------|
| `skip` | `0` | `>= 0` |
| `limit` | `20` | `1–100` |

**Response 200:**
```json
{
  "total": 142,
  "skip": 0,
  "limit": 20,
  "chunks": [
    { "index": 0, "text": "[Contract: abc, Page: 1] This agreement...", "label": null }
  ]
}
```

---

### `GET /api/vectordb/chunks/{index}`

Get a single chunk by its FAISS index position.

**Errors:**

| Status | Reason |
|--------|--------|
| 404 | Index out of range |
| 503 | FAISS index not loaded |

---

### `POST /api/vectordb/chunks/search`

Search stored chunks by label and/or keyword (AND logic when both provided).

**Request Body:**
```json
{
  "label": "Termination",
  "keyword": "notice",
  "limit": 20
}
```

All fields are optional, but at least one of `label` or `keyword` must be provided.

**Response 200:**
```json
{
  "total_matches": 3,
  "chunks": [...]
}
```

**Errors:**

| Status | Reason |
|--------|--------|
| 400 | No search criteria provided |
| 503 | FAISS index not loaded |

---

## Error Reference

### Standard Error Envelope

```json
{
  "detail": "Contract 'abc-123' not found.",
  "error_type": "ContractNotFoundError",
  "path": "http://localhost:8000/api/contracts/abc-123"
}
```

### All Custom Exception Types

| Exception | HTTP Status | When Raised |
|-----------|-------------|-------------|
| `InvalidContractIdError` | 400 | `contract_id` is not a valid UUID |
| `EmptyQueryError` | 400 | Chat query is empty or whitespace |
| `EmptyFileError` | 400 | Uploaded file is 0 bytes |
| `ContractAlreadyFailedError` | 400 | Contract previously failed processing |
| `ContractNotAnalyzedError` | 400 | Contract hasn't been analyzed yet |
| `FileTooLargeError` | 413 | File exceeds `MAX_FILE_SIZE_MB` |
| `UnsupportedFileTypeError` | 415 | Non-PDF extension, MIME, or magic bytes |
| `ContractNotFoundError` | 404 | No contract with that ID in the database |
| `PipelineError` | 500 | Any stage of the analysis pipeline failed |
| `OCRProcessingError` | 500 | Specifically the OCR stage failed |
| `NLPProcessingError` | 500 | Specifically the NLP stage failed |
