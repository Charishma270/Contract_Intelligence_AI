# ==============================================================================
# Contract Intelligence AI — Locust Load Test Configuration
# ==============================================================================
# Day 25: Shared configuration constants for all load test scenarios.
# ==============================================================================

# ---------------------------------------------------------------------------
# Target
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:8000"

# ---------------------------------------------------------------------------
# Performance Thresholds
# ---------------------------------------------------------------------------
# Response time thresholds (milliseconds) — used in assertions
THRESHOLDS = {
    "health":        {"p50": 50,    "p95": 200},
    "contracts":     {"p50": 200,   "p95": 500},
    "analyze":       {"p50": 5_000, "p95": 15_000},  # Heavy ML pipeline
    "risk_score":    {"p50": 500,   "p95": 2_000},
    "chat":          {"p50": 2_000, "p95": 8_000},   # RAG retrieval
    "vectordb":      {"p50": 100,   "p95": 500},
    "upload":        {"p50": 1_000, "p95": 5_000},   # File I/O + OCR
}

# ---------------------------------------------------------------------------
# Test Data
# ---------------------------------------------------------------------------
# Path to a small sample PDF for upload tests.
# Generate a minimal valid PDF or use an existing test contract.
SAMPLE_PDF_PATH = "tests/load/sample_contract.pdf"

# Chat queries to rotate through (simulates real user behaviour)
CHAT_QUERIES = [
    "What are the termination conditions in this contract?",
    "Is there a liability cap mentioned?",
    "What is the notice period for termination?",
    "Are there any indemnification clauses?",
    "What are the payment terms?",
    "Describe the intellectual property rights.",
    "What warranties are provided?",
    "Are there any non-compete clauses?",
]

# ---------------------------------------------------------------------------
# Load Profiles
# ---------------------------------------------------------------------------
# Default Locust run parameters (used in README examples).
PROFILES = {
    "smoke": {
        "users": 2,
        "spawn_rate": 1,
        "run_time": "30s",
        "description": "Quick sanity check — 2 concurrent users, 30 seconds",
    },
    "load": {
        "users": 10,
        "spawn_rate": 2,
        "run_time": "2m",
        "description": "Normal load — 10 concurrent users, 2 minutes",
    },
    "stress": {
        "users": 50,
        "spawn_rate": 5,
        "run_time": "5m",
        "description": "Stress test — 50 concurrent users, 5 minutes",
    },
    "spike": {
        "users": 100,
        "spawn_rate": 20,
        "run_time": "1m",
        "description": "Spike test — ramp to 100 users in 5s, hold 1 minute",
    },
}
