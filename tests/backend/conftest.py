"""
Shared Pytest Fixtures
======================
Day 26: Central conftest.py for the backend test suite.

Provides:
  - client     — FastAPI TestClient with temp SQLite DB
  - valid_pdf_bytes — minimal syntactically valid PDF
  - sample_contract_id — pre-seeded contract UUID in the DB
"""

import os
import uuid
import tempfile
import pytest

from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Minimal PDF that passes the %PDF- magic-byte check
# ---------------------------------------------------------------------------
MINIMAL_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    b"xref\n0 2\n0000000000 65535 f \n0000000009 00000 n \n"
    b"trailer\n<< /Size 2 /Root 1 0 R >>\nstartxref\n9\n%%EOF\n"
)


@pytest.fixture(scope="session")
def valid_pdf_bytes() -> bytes:
    """Return a minimal syntactically valid PDF byte string."""
    return MINIMAL_PDF


@pytest.fixture(scope="session")
def temp_dirs(tmp_path_factory):
    """Create isolated temp directories for uploads, DB, and logs."""
    base = tmp_path_factory.mktemp("contract_ai_test")
    uploads = base / "uploads"
    data = base / "data"
    logs = base / "logs"
    for d in (uploads, data, logs):
        d.mkdir(parents=True, exist_ok=True)
    return {
        "base": str(base),
        "uploads": str(uploads),
        "data": str(data),
        "logs": str(logs),
    }


@pytest.fixture(scope="session")
def client(temp_dirs):
    """
    Provide a FastAPI TestClient backed by an isolated SQLite database.

    Environment variables are patched before importing the app so that
    the Settings singleton picks up the temp paths.
    """
    os.environ["UPLOAD_DIR"] = temp_dirs["uploads"]
    os.environ["DATABASE_DIR"] = temp_dirs["data"]
    os.environ["LOG_DIR"] = temp_dirs["logs"]
    os.environ["APP_ENV"] = "test"
    os.environ["DEBUG"] = "false"
    # Disable CORS credentials restriction for testing
    os.environ["CORS_ALLOW_CREDENTIALS"] = "false"
    os.environ["CORS_ORIGINS"] = "*"

    # Import app AFTER setting env vars so Settings picks them up
    from main import app
    from backend.services.tracking import init_db

    init_db()

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture
def sample_contract_id(temp_dirs) -> str:
    """
    Insert a contract record into the DB and return its UUID.

    Uses scope='function' so each test that needs a contract gets a fresh one.
    """
    from backend.services.tracking import create_contract

    contract_id = str(uuid.uuid4())
    create_contract(
        contract_id=contract_id,
        filename="sample_contract.pdf",
        file_size_bytes=1024,
    )
    # Also write a placeholder file so file-path lookups work
    upload_dir = temp_dirs["uploads"]
    with open(os.path.join(upload_dir, f"{contract_id}.pdf"), "wb") as fh:
        fh.write(MINIMAL_PDF)

    return contract_id
