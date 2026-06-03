"""
Day 21 — Week 3 Integration Demo Test
=======================================
Complete integration test that validates the entire Week 3 feature set:

  Day 15: NLP integration (real_nlp service)
  Day 16: E2E pipeline (validated separately)
  Day 17: Celery async processing (schemas + task info)
  Day 18: Vector DB inspection endpoints
  Day 19: Frontend API contract finalization (schema exports)
  Day 20: Centralized configuration

This test suite is designed to run WITHOUT external services
(no Redis, no Celery worker, no FAISS index, no GPU).
It validates the integration surface via:
  - Schema instantiation and serialization
  - Config loading and delegation
  - Service function signatures and return types
  - Route registration on the FastAPI app (when deps available)
  - Mock pipeline execution
  - End-to-end HTTP contract (TestClient, when deps available)

Tests that require heavy dependencies (sqlalchemy, celery, etc.)
are skipped gracefully if those packages are not installed.
"""

import os
import json
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch


# ===================================================================
# Helper: check if heavy deps are available
# ===================================================================
def _has_module(name: str) -> bool:
    """Check if a module is fully importable without side effects."""
    try:
        mod = __import__(name)
        # For celery, the top-level import succeeds but submodules
        # fail if kombu is missing. Force a deeper import.
        if name == "celery":
            from celery import Celery  # noqa: F401
        return True
    except (ImportError, ModuleNotFoundError):
        return False


_HAS_SQLALCHEMY = _has_module("sqlalchemy")
_HAS_CELERY = _has_module("celery")
_HAS_HEAVY_DEPS = _HAS_SQLALCHEMY and _HAS_CELERY

_skip_no_sqlalchemy = pytest.mark.skipif(
    not _HAS_SQLALCHEMY,
    reason="sqlalchemy not installed",
)
_skip_no_celery = pytest.mark.skipif(
    not _HAS_CELERY,
    reason="celery not installed",
)
_skip_no_heavy = pytest.mark.skipif(
    not _HAS_HEAVY_DEPS,
    reason="sqlalchemy and/or celery not installed",
)


# ===================================================================
# SECTION 1: Configuration Integration (Day 20)
# ===================================================================

class TestConfigIntegration:
    """Verify the centralized config powers all subsystems."""

    def test_settings_loads(self):
        from backend.config import settings
        assert settings.APP_NAME is not None
        assert settings.APP_VERSION is not None

    def test_settings_summary_complete(self):
        from backend.config import settings
        s = settings.summary()
        assert "app_name" in s
        assert "celery_broker" in s
        assert "database_path" in s

    def test_ocr_config_delegates_to_settings(self):
        from backend.config import settings
        from backend.services.ocr_config import (
            POPPLER_PATH, TESSERACT_CMD, OCR_DPI,
        )
        assert POPPLER_PATH == settings.OCR_POPPLER_PATH
        assert TESSERACT_CMD == settings.OCR_TESSERACT_CMD
        assert OCR_DPI == settings.OCR_DPI

    def test_nlp_config_delegates_to_settings(self):
        from backend.config import settings
        from backend.services.nlp_config import (
            CONFIDENCE_THRESHOLD, MAX_SEQUENCE_LENGTH, SPACY_MODEL,
        )
        assert CONFIDENCE_THRESHOLD == settings.NLP_CONFIDENCE_THRESHOLD
        assert MAX_SEQUENCE_LENGTH == settings.NLP_MAX_SEQUENCE_LENGTH
        assert SPACY_MODEL == settings.NLP_SPACY_MODEL

    def test_env_override_creates_fresh_settings(self, monkeypatch):
        monkeypatch.setenv("APP_ENV", "testing")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.APP_ENV == "testing"


# ===================================================================
# SECTION 2: Schema Completeness (Day 19 finalization)
# ===================================================================

class TestSchemaCompleteness:
    """Verify every schema from all 4 schema modules is importable and usable."""

    def test_all_contract_schemas(self):
        from backend.schemas.contract_schema import (
            ContractStatus,
            ContractMetadata,
            RiskBreakdown,
            RiskScoreResponse,
            AnalysisResponse,
            UploadResponse,
            AsyncTaskResponse,
            TaskStatusResponse,
            TaskRevokeResponse,
        )
        # Verify enum values
        assert ContractStatus.UPLOADED.value == "uploaded"
        assert ContractStatus.COMPLETED.value == "completed"

        # Verify schema instantiation
        meta = ContractMetadata(contract_id="int-test", filename="demo.pdf")
        assert meta.status == ContractStatus.UPLOADED

    def test_all_nlp_schemas(self):
        from backend.schemas.nlp_schema import (
            ClausePrediction,
            EntityPrediction,
            NLPOutput,
        )
        clause = ClausePrediction(
            clause_type="Termination",
            answer_text="May be terminated",
            confidence=0.92,
        )
        assert clause.is_present is True
        assert clause.page == 1

    def test_all_rag_schemas(self):
        from backend.schemas.rag_schema import (
            RetrievedChunk,
            ChatRequest,
            ChatResponse,
            QueryRequest,
            QueryResponse,
            MultiLabelPrediction,
            ClauseResult,
            ContractSummary,
        )
        response = ChatResponse(answer="Test answer")
        assert response.retrieved_chunks == []
        assert response.citations == []

    def test_all_vectordb_schemas(self):
        from backend.schemas.vectordb_schema import (
            VectorDBStatusResponse,
            ChunkDetail,
            ChunkListResponse,
            ChunkSearchRequest,
            ChunkSearchResponse,
        )
        chunk = ChunkDetail(
            index=0,
            text="Test chunk",
            text_preview="Test",
            label_name="Termination",
            word_count=2,
        )
        assert chunk.index == 0

    def test_all_schemas_via_init(self):
        """Verify __init__.py re-exports are complete."""
        from backend.schemas import (
            # OCR
            OCRChunk, OCROutput,
            # NLP
            ClausePrediction, EntityPrediction, NLPOutput,
            # RAG
            RetrievedChunk, ChatRequest, ChatResponse,
            QueryRequest, QueryResponse,
            MultiLabelPrediction, ClauseResult, ContractSummary,
            # Contract
            ContractStatus, ContractMetadata,
            RiskBreakdown, RiskScoreResponse,
            AnalysisResponse, UploadResponse,
            AsyncTaskResponse, TaskStatusResponse, TaskRevokeResponse,
            # VectorDB
            VectorDBStatusResponse, ChunkDetail,
            ChunkListResponse, ChunkSearchRequest, ChunkSearchResponse,
        )
        # All should be non-None classes
        all_schemas = [
            OCRChunk, OCROutput,
            ClausePrediction, EntityPrediction, NLPOutput,
            RetrievedChunk, ChatRequest, ChatResponse,
            QueryRequest, QueryResponse,
            MultiLabelPrediction, ClauseResult, ContractSummary,
            ContractStatus, ContractMetadata,
            RiskBreakdown, RiskScoreResponse,
            AnalysisResponse, UploadResponse,
            AsyncTaskResponse, TaskStatusResponse, TaskRevokeResponse,
            VectorDBStatusResponse, ChunkDetail,
            ChunkListResponse, ChunkSearchRequest, ChunkSearchResponse,
        ]
        for schema in all_schemas:
            assert schema is not None


# ===================================================================
# SECTION 3: Async Task Schemas (Day 17)
# ===================================================================

class TestAsyncTaskSchemas:
    """Validate Celery async schemas work end-to-end."""

    def test_async_task_response_defaults(self):
        from backend.schemas.contract_schema import AsyncTaskResponse
        resp = AsyncTaskResponse(
            task_id="celery-task-001",
            contract_id="contract-001",
        )
        assert resp.status == "processing"
        assert resp.message == "Analysis task submitted successfully"

    def test_task_status_response_all_states(self):
        from backend.schemas.contract_schema import TaskStatusResponse

        # PENDING
        pending = TaskStatusResponse(task_id="t1", state="PENDING")
        assert pending.progress is None
        assert pending.result is None

        # SUCCESS
        success = TaskStatusResponse(
            task_id="t1",
            state="SUCCESS",
            result={"risk_score": 42},
        )
        assert success.result["risk_score"] == 42

        # FAILURE
        failure = TaskStatusResponse(
            task_id="t1",
            state="FAILURE",
            error="Model not loaded",
        )
        assert failure.error == "Model not loaded"

    def test_task_revoke_response(self):
        from backend.schemas.contract_schema import TaskRevokeResponse
        resp = TaskRevokeResponse(
            task_id="celery-task-001",
            message="Task revoked successfully",
        )
        assert resp.status == "revoked"

    @_skip_no_celery
    def test_celery_task_info_function_exists(self):
        """Verify the get_task_info helper is callable."""
        from backend.services.celery_tasks import get_task_info
        assert callable(get_task_info)


# ===================================================================
# SECTION 4: Vector DB Service (Day 18)
# ===================================================================

class TestVectorDBSchemas:
    """Validate Vector DB inspection schemas."""

    def test_status_response(self):
        from backend.schemas.vectordb_schema import VectorDBStatusResponse
        status = VectorDBStatusResponse(
            total_vectors=1000,
            dimension=384,
            is_trained=True,
            metadata_count=1000,
            index_type="IndexFlatL2",
            bm25_loaded=True,
        )
        assert status.total_vectors == 1000
        assert status.dimension == 384

    def test_chunk_list_response(self):
        from backend.schemas.vectordb_schema import (
            ChunkDetail,
            ChunkListResponse,
        )
        chunks = [
            ChunkDetail(
                index=i,
                text=f"Chunk {i} text",
                text_preview=f"Chunk {i}",
                label_name="Termination",
                word_count=3,
            )
            for i in range(5)
        ]
        resp = ChunkListResponse(
            total=100,
            skip=0,
            limit=5,
            chunks=chunks,
        )
        assert resp.total == 100
        assert len(resp.chunks) == 5

    def test_chunk_search_response(self):
        from backend.schemas.vectordb_schema import (
            ChunkDetail,
            ChunkSearchResponse,
        )
        resp = ChunkSearchResponse(
            match_count=0,
            chunks=[],
        )
        assert resp.match_count == 0

    def test_chunk_search_request(self):
        from backend.schemas.vectordb_schema import ChunkSearchRequest
        req = ChunkSearchRequest(
            label="termination",
            keyword="breach",
            limit=25,
        )
        assert req.label == "termination"
        assert req.keyword == "breach"


# ===================================================================
# SECTION 5: Pipeline Risk Scoring (Day 15 integration)
# ===================================================================

@_skip_no_sqlalchemy
class TestRiskScoringIntegration:
    """Validate the risk scoring logic with realistic NLP output."""

    def test_base_risk_only(self):
        """With no clause flags, risk should be base (30)."""
        from backend.schemas.nlp_schema import NLPOutput
        from backend.services.pipeline import _compute_risk_score

        nlp_output = NLPOutput(
            contract_id="test",
            clauses=[], entities=[],
            processing_time_seconds=0.5,
        )
        score, severity, breakdown = _compute_risk_score(nlp_output)
        assert score == 30
        assert severity == "medium"
        assert len(breakdown) == 1
        assert breakdown[0].factor == "Base Contract Risk"

    def test_high_risk_scenario(self):
        """Uncapped liability + auto-renewal should produce high risk."""
        from backend.schemas.nlp_schema import (
            ClausePrediction,
            NLPOutput,
        )
        from backend.services.pipeline import _compute_risk_score

        clauses = [
            ClausePrediction(
                clause_type="Uncapped Liability",
                answer_text="Unlimited liability for damages",
                confidence=0.95,
                is_present=True,
            ),
            ClausePrediction(
                clause_type="Renewal Term",
                answer_text="Auto-renews annually",
                confidence=0.88,
                is_present=True,
            ),
        ]
        nlp_output = NLPOutput(
            contract_id="test",
            clauses=clauses, entities=[],
            processing_time_seconds=1.0,
        )
        score, severity, breakdown = _compute_risk_score(nlp_output)
        # Base(30) + Uncapped(30) + Renewal(20) = 80
        assert score == 80
        assert severity == "critical"
        assert len(breakdown) == 3  # base + 2 factors

    def test_risk_clamped_to_100(self):
        """Score should never exceed 100."""
        from backend.schemas.nlp_schema import (
            ClausePrediction,
            NLPOutput,
        )
        from backend.services.pipeline import _compute_risk_score

        clauses = [
            ClausePrediction(
                clause_type="Uncapped Liability",
                answer_text="text",
                confidence=0.9,
                is_present=True,
            ),
            ClausePrediction(
                clause_type="Renewal Term",
                answer_text="text",
                confidence=0.9,
                is_present=True,
            ),
        ]
        nlp_output = NLPOutput(
            contract_id="test",
            clauses=clauses, entities=[],
            processing_time_seconds=0.5,
        )
        score, _, _ = _compute_risk_score(nlp_output)
        assert 0 <= score <= 100

    def test_risk_reduction_with_protective_clauses(self):
        """Termination for convenience and cap on liability reduce risk."""
        from backend.schemas.nlp_schema import (
            ClausePrediction,
            NLPOutput,
        )
        from backend.services.pipeline import _compute_risk_score

        clauses = [
            ClausePrediction(
                clause_type="Termination For Convenience",
                answer_text="Either party may terminate",
                confidence=0.85,
                is_present=True,
            ),
            ClausePrediction(
                clause_type="Cap on Liability",
                answer_text="Liability capped at $1M",
                confidence=0.90,
                is_present=True,
            ),
        ]
        nlp_output = NLPOutput(
            contract_id="test",
            clauses=clauses, entities=[],
            processing_time_seconds=0.5,
        )
        score, severity, breakdown = _compute_risk_score(nlp_output)
        # Base(30) - Termination(-5) - Cap(-10) = 15
        assert score == 15
        assert severity == "low"


# ===================================================================
# SECTION 6: FastAPI Route Registration
# ===================================================================

@_skip_no_heavy
class TestRouteRegistration:
    """Verify all expected routes are registered on the FastAPI app."""

    @pytest.fixture(scope="class")
    def app_routes(self):
        from main import app
        return [route.path for route in app.routes]

    def test_health_endpoint(self, app_routes):
        assert "/health" in app_routes

    def test_root_endpoint(self, app_routes):
        assert "/" in app_routes

    def test_upload_endpoint(self, app_routes):
        assert "/api/upload" in app_routes

    def test_contracts_endpoints(self, app_routes):
        assert "/api/contracts" in app_routes

    def test_analyze_endpoint(self, app_routes):
        assert "/api/analyze/{contract_id}" in app_routes

    def test_async_analyze_endpoint(self, app_routes):
        assert "/api/analyze/{contract_id}/async" in app_routes

    def test_task_status_endpoint(self, app_routes):
        assert "/api/tasks/{task_id}" in app_routes

    def test_task_revoke_endpoint(self, app_routes):
        assert "/api/tasks/{task_id}/revoke" in app_routes

    def test_vectordb_status_endpoint(self, app_routes):
        assert "/api/vectordb/status" in app_routes

    def test_vectordb_chunks_endpoint(self, app_routes):
        assert "/api/vectordb/chunks" in app_routes

    def test_chat_endpoint(self, app_routes):
        route_exists = any(
            "/api/chat" in r for r in app_routes
        )
        assert route_exists

    def test_risk_endpoint(self, app_routes):
        route_exists = any(
            "/api/risk" in r for r in app_routes
        )
        assert route_exists


# ===================================================================
# SECTION 7: Health & Root HTTP Tests (TestClient)
# ===================================================================

@_skip_no_heavy
class TestHTTPEndpoints:
    """End-to-end HTTP tests using FastAPI TestClient."""

    @pytest.fixture(scope="class")
    def client(self):
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "service" in data
        assert "environment" in data

    def test_health_version_matches_config(self, client):
        from backend.config import settings
        resp = client.get("/health")
        data = resp.json()
        assert data["version"] == settings.APP_VERSION
        assert data["service"] == settings.APP_NAME

    def test_root_returns_endpoints(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "endpoints" in data
        assert "upload" in data["endpoints"]
        assert "analyze" in data["endpoints"]
        assert "chat" in data["endpoints"]
        assert "risk" in data["endpoints"]
        assert "async_analyze" in data["endpoints"]
        assert "vectordb_status" in data["endpoints"]

    def test_request_id_header(self, client):
        resp = client.get("/health")
        assert "x-request-id" in resp.headers
        assert len(resp.headers["x-request-id"]) == 8

    def test_process_time_header(self, client):
        resp = client.get("/health")
        assert "x-process-time" in resp.headers
        process_time = float(resp.headers["x-process-time"])
        assert process_time >= 0

    def test_cors_headers(self, client):
        """Verify CORS middleware is active."""
        resp = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.status_code != 405

    def test_404_for_unknown_route(self, client):
        resp = client.get("/api/nonexistent")
        assert resp.status_code == 404


# ===================================================================
# SECTION 8: Upload Validation (without real file processing)
# ===================================================================

@_skip_no_heavy
class TestUploadValidation:
    """Test upload endpoint validation without real OCR processing."""

    @pytest.fixture(scope="class")
    def client(self):
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

    def test_reject_non_pdf(self, client):
        """Non-PDF files should be rejected."""
        resp = client.post(
            "/api/upload",
            files={"file": ("test.txt", b"hello world", "text/plain")},
        )
        assert resp.status_code in (400, 415, 422)


    def test_reject_empty_file(self, client):
        """Empty PDF files should be rejected."""
        resp = client.post(
            "/api/upload",
            files={"file": ("test.pdf", b"", "application/pdf")},
        )
        assert resp.status_code in (400, 415, 422)

    def test_reject_invalid_pdf_magic(self, client):
        """Files with PDF extension but wrong magic bytes should be rejected."""
        resp = client.post(
            "/api/upload",
            files={"file": ("test.pdf", b"not a pdf", "application/pdf")},
        )
        assert resp.status_code in (400, 415, 422)


# ===================================================================
# SECTION 9: Schema Serialization Round-Trip
# ===================================================================

class TestSchemaRoundTrip:
    """Verify schemas serialize/deserialize to JSON cleanly."""

    def test_analysis_response_json(self):
        from backend.schemas.contract_schema import (
            AnalysisResponse,
            ContractStatus,
            RiskBreakdown,
        )
        from backend.schemas.nlp_schema import (
            ClausePrediction,
            EntityPrediction,
        )

        resp = AnalysisResponse(
            contract_id="round-trip-test",
            filename="demo.pdf",
            status=ContractStatus.COMPLETED,
            risk_score=65,
            risk_severity="high",
            clauses=[
                ClausePrediction(
                    clause_type="Termination",
                    answer_text="May be terminated",
                    confidence=0.92,
                ),
            ],
            entities=[
                EntityPrediction(
                    entity_type="ORGANIZATION",
                    value="Acme Corp",
                ),
            ],
            risk_breakdown=[
                RiskBreakdown(
                    factor="Base Risk",
                    score=30,
                    severity="low",
                    description="Baseline risk",
                ),
            ],
        )

        # Serialize to JSON
        json_str = resp.model_dump_json()
        data = json.loads(json_str)

        # Verify key fields survived round-trip
        assert data["contract_id"] == "round-trip-test"
        assert data["risk_score"] == 65
        assert len(data["clauses"]) == 1
        assert len(data["entities"]) == 1
        assert len(data["risk_breakdown"]) == 1

    def test_upload_response_json(self):
        from backend.schemas.contract_schema import UploadResponse

        resp = UploadResponse(
            contract_id="upload-test",
            filename="contract.pdf",
            file_size_bytes=2048576,
            message="12 chunks indexed",
        )
        data = json.loads(resp.model_dump_json())
        assert data["contract_id"] == "upload-test"
        assert data["file_size_bytes"] == 2048576
        assert "timestamp" in data

    def test_vectordb_status_json(self):
        from backend.schemas.vectordb_schema import VectorDBStatusResponse
        status = VectorDBStatusResponse(
            total_vectors=500,
            dimension=384,
            is_trained=True,
            metadata_count=500,
            index_type="IndexFlatL2",
            bm25_loaded=False,
        )
        data = json.loads(status.model_dump_json())
        assert data["total_vectors"] == 500
        assert data["bm25_loaded"] is False


# ===================================================================
# SECTION 10: Integration Summary
# ===================================================================

class TestWeek3Summary:
    """
    Meta-test: verify that all Week 3 components are present
    and wired together correctly.
    """

    def test_week3_lightweight_modules_importable(self):
        """Week 3 modules that have no heavy deps should import without error."""
        import importlib
        lightweight_targets = [
            "backend.config",
            "backend.schemas.contract_schema",
            "backend.schemas.nlp_schema",
            "backend.schemas.rag_schema",
            "backend.schemas.vectordb_schema",
            "backend.services.ocr_config",
            "backend.services.nlp_config",
        ]
        for module_name in lightweight_targets:
            mod = importlib.import_module(module_name)
            assert mod is not None, f"Failed to import {module_name}"

    @_skip_no_sqlalchemy
    def test_sqlalchemy_modules_importable(self):
        """Modules requiring sqlalchemy should import."""
        import importlib
        targets = [
            "backend.services.pipeline",
        ]
        for module_name in targets:
            mod = importlib.import_module(module_name)
            assert mod is not None, f"Failed to import {module_name}"

    @_skip_no_celery
    def test_celery_modules_importable(self):
        """Modules requiring celery should import."""
        import importlib
        targets = [
            "backend.celery_config",
            "backend.services.celery_tasks",
            "backend.routes.async_analyze",
        ]
        for module_name in targets:
            mod = importlib.import_module(module_name)
            assert mod is not None, f"Failed to import {module_name}"

    def test_env_example_exists(self):
        """The .env.example file should exist in the project root."""
        env_example = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            ".env.example",
        )
        assert os.path.isfile(env_example), ".env.example not found"

    def test_config_module_exists(self):
        """The backend/config.py file should exist."""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "backend", "config.py",
        )
        assert os.path.isfile(config_path), "backend/config.py not found"
