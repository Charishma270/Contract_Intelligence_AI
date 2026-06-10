# Load Testing — Contract Intelligence AI

## Overview

Load tests use [Locust](https://locust.io/) to simulate multiple concurrent users hitting the API.
Three user classes cover different usage patterns:

| User Class | Simulates | Weight |
|------------|-----------|--------|
| `HealthUser` | Monitoring agent pinging `/health` | ×2 |
| `ContractUser` | Legal analyst — upload → analyze → risk → chat | ×5 |
| `VectorDBUser` | Developer inspecting FAISS index health | ×3 |

---

## Prerequisites

```bash
# Install locust (inside your virtual environment)
pip install locust

# Verify the backend is running first
curl http://localhost:8000/health
```

---

## Running the Tests

### 1. Smoke Test (quick sanity — 30 seconds)
```bash
locust -f tests/load/locustfile.py \
    --headless -u 2 -r 1 -t 30s \
    --host=http://localhost:8000
```

### 2. Normal Load Test (2 minutes)
```bash
locust -f tests/load/locustfile.py \
    --headless -u 10 -r 2 -t 2m \
    --host=http://localhost:8000
```

### 3. Stress Test (50 users, 5 minutes)
```bash
locust -f tests/load/locustfile.py \
    --headless -u 50 -r 5 -t 5m \
    --host=http://localhost:8000
```

### 4. Interactive Web UI
```bash
locust -f tests/load/locustfile.py --host=http://localhost:8000
# Open http://localhost:8089 in your browser
```

### 5. Generate HTML Report
```bash
locust -f tests/load/locustfile.py \
    --headless -u 10 -r 2 -t 60s \
    --host=http://localhost:8000 \
    --html=tests/load/report.html
```

---

## Against EC2 (production)

```bash
BASE_URL=http://<YOUR_EC2_IP>:8000

locust -f tests/load/locustfile.py \
    --headless -u 10 -r 2 -t 2m \
    --host=$BASE_URL
```

---

## Performance Thresholds

Defined in [`load_test_config.py`](load_test_config.py):

| Endpoint | p50 target | p95 target |
|----------|-----------|-----------|
| `GET /health` | 50 ms | 200 ms |
| `GET /api/contracts` | 200 ms | 500 ms |
| `POST /api/upload` | 1 000 ms | 5 000 ms |
| `POST /api/analyze/{id}` | 5 000 ms | 15 000 ms |
| `GET /api/risk-score/{id}` | 500 ms | 2 000 ms |
| `POST /api/chat` | 2 000 ms | 8 000 ms |
| `GET /api/vectordb/status` | 100 ms | 500 ms |

> **Note:** The analyze endpoint runs a full OCR → NLP → RAG → risk pipeline,
> so higher latencies are expected.
> These thresholds are for a single-instance deployment on a `t3.medium` EC2.

---

## Sample PDF

`ContractUser` uploads a PDF on each test cycle.
- If `tests/load/sample_contract.pdf` exists on disk, it will use that file.
- Otherwise a minimal valid PDF is generated automatically so tests can run without real contract files.

To use a real contract for more realistic testing:
```bash
cp /path/to/your/sample.pdf tests/load/sample_contract.pdf
```

---

## Output Interpretation

Key metrics from the Locust report:

| Metric | What it means |
|--------|--------------|
| **RPS** | Requests per second — overall throughput |
| **Failures %** | Should be < 1% under normal load |
| **p50 (median)** | Half of requests faster than this |
| **p95** | 95% of requests faster than this — compare to thresholds above |
| **p99** | Tail latency — watch for spikes |

---

## Files

```
tests/load/
├── locustfile.py         ← Main test scenarios (HealthUser, ContractUser, VectorDBUser)
├── load_test_config.py   ← Thresholds, profiles, test data paths
├── README.md             ← This file
└── sample_contract.pdf   ← Optional real PDF for upload tests (gitignored)
```
