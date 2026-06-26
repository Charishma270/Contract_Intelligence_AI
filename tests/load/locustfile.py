"""
Contract Intelligence AI — Locust Load Test Suite
===================================================
Day 25: Performance and scalability testing for all major API endpoints.

Scenarios:
  HealthUser      — Hammers /health and / (baseline throughput check)
  ContractUser    — Full upload → analyze → risk-score → chat flow
  VectorDBUser    — Polls vectordb status and chunk listing

Usage:
  # Smoke test (quick sanity check)
  locust -f tests/load/locustfile.py --headless -u 2 -r 1 -t 30s --host=http://localhost:8000

  # Normal load test
  locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 2m --host=http://localhost:8000

  # Web UI (interactive)
  locust -f tests/load/locustfile.py --host=http://localhost:8000
  # Then open http://localhost:8089

  # Generate HTML report
  locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 60s \\
      --host=http://localhost:8000 --html=tests/load/report.html

Requirements:
  pip install locust
"""

import os
import json
import random
import logging

from locust import (
    HttpUser,
    TaskSet,
    task,
    between,
    events,
)

from tests.load.load_test_config import (
    CHAT_QUERIES,
    SAMPLE_PDF_PATH,
    THRESHOLDS,
)

logger = logging.getLogger("locust.contract_ai")


# ===========================================================================
# Helpers
# ===========================================================================

def _make_minimal_pdf() -> bytes:
    """
    Return the bytes of a minimal valid PDF.
    Used when no sample PDF is found on disk, so tests can still run
    without a real contract file.
    """
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
        b"xref\n0 4\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer\n<< /Root 1 0 R /Size 4 >>\nstartxref\n190\n%%EOF\n"
    )


def _load_sample_pdf() -> bytes:
    """Load sample PDF from disk, or generate a minimal one as fallback."""
    if os.path.isfile(SAMPLE_PDF_PATH):
        with open(SAMPLE_PDF_PATH, "rb") as f:
            return f.read()
    return _make_minimal_pdf()


# ===========================================================================
# Task Sets
# ===========================================================================

class HealthTasks(TaskSet):
    """
    Lightweight tasks that verify system liveness.
    Weight: high — these run frequently to establish baseline throughput.
    """

    @task(3)
    def get_health(self):
        """GET /health — primary liveness probe."""
        with self.client.get(
            "/health",
            name="GET /health",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                body = resp.json()
                if body.get("status") != "ok":
                    resp.failure(
                        f"Unexpected status field: {body.get('status')}"
                    )
                else:
                    resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")

    @task(1)
    def get_root(self):
        """GET / — root info endpoint."""
        with self.client.get(
            "/",
            name="GET /",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")

    @task(1)
    def get_docs(self):
        """GET /docs — Swagger UI available."""
        with self.client.get(
            "/docs",
            name="GET /docs",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")


class ContractFlowTasks(TaskSet):
    """
    Simulates the full user journey:
      1. Upload a PDF contract
      2. Trigger analysis pipeline
      3. Fetch risk score
      4. Ask a chat question about the contract
    """

    def on_start(self):
        """Cache sample PDF bytes once per simulated user."""
        self._pdf_bytes = _load_sample_pdf()
        self._contract_id = None

    # ------------------------------------------------------------------
    # Step 1 — Upload
    # ------------------------------------------------------------------
    @task(4)
    def upload_contract(self):
        """POST /api/upload — uploads a PDF and caches the contract_id."""
        with self.client.post(
            "/api/upload",
            name="POST /api/upload",
            files={
                "file": (
                    "load_test_contract.pdf",
                    self._pdf_bytes,
                    "application/pdf",
                )
            },
            catch_response=True,
        ) as resp:
            if resp.status_code in (200, 201):
                try:
                    body = resp.json()
                    self._contract_id = body.get("contract_id")
                    resp.success()
                except Exception as exc:
                    resp.failure(f"JSON parse error: {exc}")
            elif resp.status_code == 413:
                resp.failure("File too large (413)")
            elif resp.status_code == 422:
                resp.failure(f"Validation error (422): {resp.text[:200]}")
            else:
                resp.failure(f"HTTP {resp.status_code}")

    # ------------------------------------------------------------------
    # Step 2 — Analyze
    # ------------------------------------------------------------------
    @task(2)
    def analyze_contract(self):
        """POST /api/analyze/{id} — runs the ML pipeline."""
        if not self._contract_id:
            return  # Skip if no upload happened yet

        with self.client.post(
            f"/api/analyze/{self._contract_id}",
            name="POST /api/analyze/{id}",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            elif resp.status_code == 404:
                # Contract may have been cleaned up — reset and continue
                self._contract_id = None
                resp.failure("Contract not found (404) — resetting")
            else:
                resp.failure(f"HTTP {resp.status_code}")

    # ------------------------------------------------------------------
    # Step 3 — Risk Score
    # ------------------------------------------------------------------
    @task(2)
    def get_risk_score(self):
        """GET /api/risk-score/{id} — fetch risk breakdown."""
        if not self._contract_id:
            return

        with self.client.get(
            f"/api/risk-score/{self._contract_id}",
            name="GET /api/risk-score/{id}",
            catch_response=True,
        ) as resp:
            if resp.status_code in (200, 404):
                # 404 is acceptable (contract not yet analyzed)
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")

    # ------------------------------------------------------------------
    # Step 4 — Chat
    # ------------------------------------------------------------------
    @task(1)
    def chat_query(self):
        """POST /api/chat — RAG-powered question answering."""
        query = random.choice(CHAT_QUERIES)
        payload = {
            "query": query,
            "contract_id": self._contract_id,
        }

        with self.client.post(
            "/api/chat",
            name="POST /api/chat",
            json=payload,
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                body = resp.json()
                if "answer" not in body:
                    resp.failure("Response missing 'answer' field")
                else:
                    resp.success()
            elif resp.status_code == 422:
                resp.failure(f"Validation error (422): {resp.text[:200]}")
            else:
                resp.failure(f"HTTP {resp.status_code}")

    # ------------------------------------------------------------------
    # Contract listing
    # ------------------------------------------------------------------
    @task(3)
    def list_contracts(self):
        """GET /api/contracts — paginated contract listing."""
        page = random.randint(1, 3)
        with self.client.get(
            f"/api/contracts?page={page}&page_size=10",
            name="GET /api/contracts",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")


class VectorDBTasks(TaskSet):
    """
    Simulates the frontend developer / QA engineer
    inspecting the FAISS index health and chunk contents.
    """

    @task(3)
    def vectordb_status(self):
        """GET /api/vectordb/status — FAISS index health."""
        with self.client.get(
            "/api/vectordb/status",
            name="GET /api/vectordb/status",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")

    @task(2)
    def vectordb_chunks(self):
        """GET /api/vectordb/chunks — paginated chunk list."""
        page = random.randint(0, 5)
        with self.client.get(
            f"/api/vectordb/chunks?offset={page * 20}&limit=20",
            name="GET /api/vectordb/chunks",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")

    @task(1)
    def vectordb_search(self):
        """POST /api/vectordb/chunks/search — keyword search."""
        keywords = [
            "termination", "liability", "payment",
            "warranty", "indemnification", "notice",
        ]
        with self.client.post(
            "/api/vectordb/chunks/search",
            name="POST /api/vectordb/chunks/search",
            json={"keyword": random.choice(keywords)},
            catch_response=True,
        ) as resp:
            if resp.status_code in (200, 404):
                resp.success()
            else:
                resp.failure(f"HTTP {resp.status_code}")


# ===========================================================================
# User Classes
# ===========================================================================

class HealthUser(HttpUser):
    """
    Simulates a monitoring agent pinging the health endpoint.
    Fast wait time — high frequency.
    """
    tasks = [HealthTasks]
    wait_time = between(0.5, 2)
    weight = 2  # Spawn 2x more HealthUsers than others


class ContractUser(HttpUser):
    """
    Simulates a legal analyst uploading and analyzing contracts.
    Slower wait time — reflects real human interaction pace.
    """
    tasks = [ContractFlowTasks]
    wait_time = between(3, 8)
    weight = 5  # Primary load driver


class VectorDBUser(HttpUser):
    """
    Simulates a developer / QA engineer inspecting the vector DB.
    """
    tasks = [VectorDBTasks]
    wait_time = between(1, 4)
    weight = 3


# ===========================================================================
# Event Hooks
# ===========================================================================

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Log test start with configuration summary."""
    logger.info(
        "Load test starting | "
        f"host={environment.host} | "
        f"users={environment.runner.target_user_count if environment.runner else 'N/A'}"
    )


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Log final stats and check thresholds."""
    stats = environment.runner.stats if environment.runner else None
    if not stats:
        return

    logger.info("Load test complete — checking thresholds...")

    failures = []
    threshold_map = {
        "GET /health":           THRESHOLDS["health"],
        "GET /api/contracts":    THRESHOLDS["contracts"],
        "POST /api/upload":      THRESHOLDS["upload"],
        "POST /api/chat":        THRESHOLDS["chat"],
        "GET /api/vectordb/status": THRESHOLDS["vectordb"],
    }

    for name, limits in threshold_map.items():
        entry = stats.entries.get((name, "GET"), None) \
            or stats.entries.get((name, "POST"), None)
        if not entry or entry.num_requests == 0:
            continue
        p95 = entry.get_response_time_percentile(0.95)
        if p95 > limits["p95"]:
            failures.append(
                f"  {name}: p95={p95:.0f}ms > threshold={limits['p95']}ms"
            )

    if failures:
        logger.warning("THRESHOLD VIOLATIONS:\n" + "\n".join(failures))
    else:
        logger.info("All response time thresholds passed!")
