"""
Day 26 — Integration Tests: All API Endpoints
==============================================
Exercises every route in the FastAPI application via TestClient.
External dependencies (pipeline, Celery, FAISS) are patched so tests
run without GPU, Redis, or Tesseract installations.

Test classes:
  TestSystemEndpoints       — GET / and GET /health
  TestUploadEndpoint        — POST /api/upload
  TestContractsEndpoint     — GET /api/contracts, /api/contracts/{id}
  TestAnalyzeEndpoint       — POST /api/analyze/{id}
  TestRiskEndpoint          — GET /api/risk/risk-score/{id}
  TestChatEndpoint          — POST /api/chat/chat
  TestAsyncAnalyzeEndpoint  — POST /api/analyze/{id}/async
  TestTaskStatusEndpoint    — GET /api/tasks/{task_id}
  TestTaskRevokeEndpoint    — POST /api/tasks/{task_id}/revoke
  TestVectorDBEndpoints     — GET /api/vectordb/status, /chunks, /chunks/{n}
"""

import io
import uuid
from unittest.mock import patch, MagicMock

import pytest


# ===========================================================================
# Helpers
# ===========================================================================

def _make_pdf_upload(pdf_bytes: bytes, filename: str = "contract.pdf"):
    """Build the multipart form files dict for a PDF upload."""
    return {
        "file": (filename, io.BytesIO(pdf_bytes), "application/pdf"),
    }


# ===========================================================================
# System Endpoints
# ===========================================================================

class TestSystemEndpoints:

    def test_root_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_root_contains_message(self, client):
        data = resp = client.get("/")
        data = resp.json()
        assert "message" in data
        assert "docs" in data
        assert "health" in data
        assert "endpoints" in data

    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_status_ok(self, client):
        data = client.get("/health").json()
        assert data["status"] == "ok"

    def test_health_has_version(self, client):
        data = client.get("/health").json()
        assert "version" in data

    def test_health_has_environment(self, client):
        data = client.get("/health").json()
        assert "environment" in data


# ===========================================================================
# Upload Endpoint
# ===========================================================================

class TestUploadEndpoint:

    def test_valid_pdf_returns_201(self, client, valid_pdf_bytes):
        with patch("backend.routes.upload.process_contract", return_value=["chunk1"]):
            resp = client.post(
                "/api/upload",
                files=_make_pdf_upload(valid_pdf_bytes),
            )
        assert resp.status_code == 201

    def test_valid_pdf_response_schema(self, client, valid_pdf_bytes):
        with patch("backend.routes.upload.process_contract", return_value=["chunk1", "chunk2"]):
            data = client.post(
                "/api/upload",
                files=_make_pdf_upload(valid_pdf_bytes),
            ).json()
        assert "contract_id" in data
        assert data["status"] == "uploaded"
        assert "filename" in data
        assert "message" in data

    def test_valid_pdf_contract_id_is_uuid(self, client, valid_pdf_bytes):
        with patch("backend.routes.upload.process_contract", return_value=[]):
            data = client.post(
                "/api/upload",
                files=_make_pdf_upload(valid_pdf_bytes),
            ).json()
        # Should be parseable as UUID
        uuid.UUID(data["contract_id"])

    def test_no_file_returns_422(self, client):
        resp = client.post("/api/upload")
        assert resp.status_code == 422

    def test_wrong_mime_type_returns_415(self, client):
        resp = client.post(
            "/api/upload",
            files={"file": ("doc.pdf", io.BytesIO(b"plain text"), "text/plain")},
        )
        assert resp.status_code == 415

    def test_wrong_extension_returns_415(self, client, valid_pdf_bytes):
        resp = client.post(
            "/api/upload",
            files={
                "file": ("contract.docx", io.BytesIO(valid_pdf_bytes), "application/pdf")
            },
        )
        assert resp.status_code == 415

    def test_empty_file_returns_400(self, client):
        resp = client.post(
            "/api/upload",
            files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")},
        )
        assert resp.status_code == 400

    def test_non_pdf_bytes_returns_415(self, client):
        """File with PDF MIME but no %PDF- magic bytes."""
        resp = client.post(
            "/api/upload",
            files={"file": ("fake.pdf", io.BytesIO(b"not a pdf"), "application/pdf")},
        )
        assert resp.status_code == 415

    def test_ocr_failure_still_returns_201(self, client, valid_pdf_bytes):
        """If OCR ingestion fails, upload should still succeed (chunks=0)."""
        with patch(
            "backend.routes.upload.process_contract",
            side_effect=RuntimeError("OCR crashed"),
        ):
            resp = client.post(
                "/api/upload",
                files=_make_pdf_upload(valid_pdf_bytes),
            )
        assert resp.status_code == 201
        assert "0 chunks" in resp.json()["message"]


# ===========================================================================
# Contracts Endpoints
# ===========================================================================

class TestContractsEndpoint:

    def test_list_contracts_returns_200(self, client):
        resp = client.get("/api/contracts")
        assert resp.status_code == 200

    def test_list_contracts_returns_list(self, client):
        data = client.get("/api/contracts").json()
        assert isinstance(data, list)

    def test_list_contracts_pagination_skip(self, client):
        resp = client.get("/api/contracts?skip=0&limit=5")
        assert resp.status_code == 200
        assert len(resp.json()) <= 5

    def test_list_contracts_invalid_skip(self, client):
        resp = client.get("/api/contracts?skip=-1")
        assert resp.status_code == 422

    def test_list_contracts_limit_too_large(self, client):
        resp = client.get("/api/contracts?limit=200")
        assert resp.status_code == 422

    def test_get_existing_contract(self, client, sample_contract_id):
        resp = client.get(f"/api/contracts/{sample_contract_id}")
        assert resp.status_code == 200

    def test_get_existing_contract_fields(self, client, sample_contract_id):
        data = client.get(f"/api/contracts/{sample_contract_id}").json()
        assert data["contract_id"] == sample_contract_id
        assert "status" in data
        assert "filename" in data

    def test_get_nonexistent_contract_returns_404(self, client):
        resp = client.get(f"/api/contracts/{uuid.uuid4()}")
        assert resp.status_code == 404

    def test_get_invalid_uuid_returns_400(self, client):
        resp = client.get("/api/contracts/not-a-uuid")
        assert resp.status_code == 400

    def test_error_response_has_detail_field(self, client):
        resp = client.get(f"/api/contracts/{uuid.uuid4()}")
        data = resp.json()
        assert "detail" in data

    def test_error_response_has_error_type(self, client):
        resp = client.get(f"/api/contracts/{uuid.uuid4()}")
        data = resp.json()
        assert "error_type" in data


# ===========================================================================
# Analyze Endpoint
# ===========================================================================

class TestAnalyzeEndpoint:

    def _make_mock_analysis_response(self, contract_id: str):
        from backend.schemas.contract_schema import AnalysisResponse, ContractStatus
        return AnalysisResponse(
            contract_id=contract_id,
            filename="sample_contract.pdf",
            status=ContractStatus.COMPLETED,
            risk_score=45,
            risk_severity="medium",
            clauses=[],
            entities=[],
            risk_breakdown=[],
        )

    def test_analyze_existing_contract_returns_200(self, client, sample_contract_id):
        with patch(
            "backend.routes.analyze.run_pipeline",
            return_value=self._make_mock_analysis_response(sample_contract_id),
        ):
            resp = client.post(f"/api/analyze/{sample_contract_id}")
        assert resp.status_code == 200

    def test_analyze_response_schema(self, client, sample_contract_id):
        with patch(
            "backend.routes.analyze.run_pipeline",
            return_value=self._make_mock_analysis_response(sample_contract_id),
        ):
            data = client.post(f"/api/analyze/{sample_contract_id}").json()
        assert data["contract_id"] == sample_contract_id
        assert "risk_score" in data
        assert "risk_severity" in data
        assert "clauses" in data
        assert "entities" in data

    def test_analyze_nonexistent_returns_404(self, client):
        resp = client.post(f"/api/analyze/{uuid.uuid4()}")
        assert resp.status_code == 404

    def test_analyze_invalid_uuid_returns_400(self, client):
        resp = client.post("/api/analyze/not-a-uuid")
        assert resp.status_code == 400

    def test_analyze_failed_contract_returns_400(self, client, sample_contract_id):
        from backend.services.tracking import update_contract_status
        from backend.schemas.contract_schema import ContractStatus
        update_contract_status(sample_contract_id, ContractStatus.FAILED, "prev error")
        resp = client.post(f"/api/analyze/{sample_contract_id}")
        assert resp.status_code == 400

    def test_analyze_pipeline_error_returns_500(self, client, sample_contract_id):
        from backend.utils.exceptions import PipelineError
        with patch(
            "backend.routes.analyze.run_pipeline",
            side_effect=PipelineError("ocr", sample_contract_id, "disk full"),
        ):
            resp = client.post(f"/api/analyze/{sample_contract_id}")
        assert resp.status_code == 500


# ===========================================================================
# Risk Score Endpoint
# ===========================================================================

class TestRiskEndpoint:

    def test_risk_score_existing_contract_returns_200(self, client, sample_contract_id):
        resp = client.get(f"/api/risk/risk-score/{sample_contract_id}")
        assert resp.status_code == 200

    def test_risk_score_response_schema(self, client, sample_contract_id):
        data = client.get(f"/api/risk/risk-score/{sample_contract_id}").json()
        assert data["contract_id"] == sample_contract_id
        assert "overall_risk" in data
        assert "severity" in data
        assert "breakdown" in data
        assert isinstance(data["breakdown"], list)

    def test_risk_score_value_in_range(self, client, sample_contract_id):
        data = client.get(f"/api/risk/risk-score/{sample_contract_id}").json()
        assert 0 <= data["overall_risk"] <= 100

    def test_risk_score_nonexistent_returns_404(self, client):
        resp = client.get(f"/api/risk/risk-score/{uuid.uuid4()}")
        assert resp.status_code == 404

    def test_risk_score_invalid_uuid_returns_400(self, client):
        resp = client.get("/api/risk/risk-score/bad-id")
        assert resp.status_code == 400

    def test_risk_score_severity_is_valid(self, client, sample_contract_id):
        data = client.get(f"/api/risk/risk-score/{sample_contract_id}").json()
        assert data["severity"] in {"low", "medium", "high", "critical"}


# ===========================================================================
# Chat Endpoint
# ===========================================================================

class TestChatEndpoint:

    def _mock_rag_response(self):
        from backend.schemas.rag_schema import ChatResponse
        return ChatResponse(
            answer="The termination clause allows 30-day notice.",
            retrieved_chunks=[],
            citations=[],
        )

    def test_chat_valid_request_returns_200(self, client, sample_contract_id):
        with patch("backend.routes.chat.run_rag", return_value=self._mock_rag_response()):
            resp = client.post(
                "/api/chat/chat",
                json={
                    "contract_id": sample_contract_id,
                    "query": "What are the termination clauses?",
                },
            )
        assert resp.status_code == 200

    def test_chat_response_has_answer(self, client, sample_contract_id):
        with patch("backend.routes.chat.run_rag", return_value=self._mock_rag_response()):
            data = client.post(
                "/api/chat/chat",
                json={
                    "contract_id": sample_contract_id,
                    "query": "What is the liability cap?",
                },
            ).json()
        assert "answer" in data

    def test_chat_empty_query_returns_400(self, client, sample_contract_id):
        resp = client.post(
            "/api/chat/chat",
            json={"contract_id": sample_contract_id, "query": ""},
        )
        assert resp.status_code == 400

    def test_chat_whitespace_query_returns_400(self, client, sample_contract_id):
        resp = client.post(
            "/api/chat/chat",
            json={"contract_id": sample_contract_id, "query": "   "},
        )
        assert resp.status_code == 400

    def test_chat_nonexistent_contract_returns_404(self, client):
        resp = client.post(
            "/api/chat/chat",
            json={
                "contract_id": str(uuid.uuid4()),
                "query": "What is the payment term?",
            },
        )
        assert resp.status_code == 404

    def test_chat_invalid_contract_id_returns_400(self, client):
        resp = client.post(
            "/api/chat/chat",
            json={"contract_id": "not-a-uuid", "query": "Any question"},
        )
        assert resp.status_code == 400

    def test_chat_missing_body_returns_422(self, client):
        resp = client.post("/api/chat/chat")
        assert resp.status_code == 422

    def test_chat_rag_error_returns_500(self, client, sample_contract_id):
        with patch(
            "backend.routes.chat.run_rag",
            side_effect=RuntimeError("FAISS index not loaded"),
        ):
            resp = client.post(
                "/api/chat/chat",
                json={
                    "contract_id": sample_contract_id,
                    "query": "question",
                },
            )
        assert resp.status_code == 500


# ===========================================================================
# Async Analysis Endpoint
# ===========================================================================

class TestAsyncAnalyzeEndpoint:

    def test_async_submit_returns_202(self, client, sample_contract_id):
        mock_task = MagicMock()
        mock_task.id = "celery-task-abc123"
        with patch(
            "backend.routes.async_analyze.run_pipeline_async.delay",
            return_value=mock_task,
        ):
            resp = client.post(f"/api/analyze/{sample_contract_id}/async")
        assert resp.status_code == 202

    def test_async_submit_response_schema(self, client, sample_contract_id):
        mock_task = MagicMock()
        mock_task.id = "celery-task-abc123"
        with patch(
            "backend.routes.async_analyze.run_pipeline_async.delay",
            return_value=mock_task,
        ):
            data = client.post(f"/api/analyze/{sample_contract_id}/async").json()
        assert "task_id" in data
        assert data["task_id"] == "celery-task-abc123"
        assert data["contract_id"] == sample_contract_id

    def test_async_submit_nonexistent_returns_404(self, client):
        resp = client.post(f"/api/analyze/{uuid.uuid4()}/async")
        assert resp.status_code == 404

    def test_async_submit_invalid_uuid_returns_400(self, client):
        resp = client.post("/api/analyze/bad-uuid/async")
        assert resp.status_code == 400


# ===========================================================================
# Task Status Endpoint
# ===========================================================================

class TestTaskStatusEndpoint:

    def test_pending_task_returns_200(self, client):
        pending_info = {
            "task_id": "task-pending-123",
            "state": "PENDING",
            "progress": None,
            "result": None,
            "error": None,
        }
        with patch(
            "backend.routes.async_analyze.get_task_info",
            return_value=pending_info,
        ):
            resp = client.get("/api/tasks/task-pending-123")
        assert resp.status_code == 200

    def test_pending_task_response(self, client):
        pending_info = {
            "task_id": "task-pending-123",
            "state": "PENDING",
            "progress": None,
            "result": None,
            "error": None,
        }
        with patch(
            "backend.routes.async_analyze.get_task_info",
            return_value=pending_info,
        ):
            data = client.get("/api/tasks/task-pending-123").json()
        assert data["state"] == "PENDING"
        assert data["result"] is None

    def test_success_task_returns_result(self, client):
        success_info = {
            "task_id": "task-success-456",
            "state": "SUCCESS",
            "progress": None,
            "result": {"risk_score": 45},
            "error": None,
        }
        with patch(
            "backend.routes.async_analyze.get_task_info",
            return_value=success_info,
        ):
            data = client.get("/api/tasks/task-success-456").json()
        assert data["state"] == "SUCCESS"
        assert data["result"] == {"risk_score": 45}

    def test_failure_task_returns_error(self, client):
        failure_info = {
            "task_id": "task-fail-789",
            "state": "FAILURE",
            "progress": None,
            "result": None,
            "error": "OCR pipeline crashed",
        }
        with patch(
            "backend.routes.async_analyze.get_task_info",
            return_value=failure_info,
        ):
            data = client.get("/api/tasks/task-fail-789").json()
        assert data["state"] == "FAILURE"
        assert data["error"] == "OCR pipeline crashed"


# ===========================================================================
# Task Revoke Endpoint
# ===========================================================================

class TestTaskRevokeEndpoint:

    def test_revoke_returns_200(self, client):
        mock_result = MagicMock()
        with patch("backend.routes.async_analyze.AsyncResult", return_value=mock_result):
            resp = client.post("/api/tasks/task-abc-123/revoke")
        assert resp.status_code == 200

    def test_revoke_response_schema(self, client):
        mock_result = MagicMock()
        with patch("backend.routes.async_analyze.AsyncResult", return_value=mock_result):
            data = client.post("/api/tasks/task-abc-123/revoke").json()
        assert data["task_id"] == "task-abc-123"
        assert data["status"] == "revoked"
        assert "message" in data

    def test_revoke_calls_revoke_on_result(self, client):
        mock_result = MagicMock()
        with patch("backend.routes.async_analyze.AsyncResult", return_value=mock_result):
            client.post("/api/tasks/any-task/revoke")
        mock_result.revoke.assert_called_once()


# ===========================================================================
# VectorDB Endpoints
# ===========================================================================

class TestVectorDBEndpoints:

    def _status_response(self, total_vectors: int = 10):
        from backend.schemas.vectordb_schema import VectorDBStatusResponse
        return VectorDBStatusResponse(
            total_vectors=total_vectors,
            dimension=384,
            index_type="IndexFlatIP",
            is_trained=True,
            metadata_count=total_vectors,
            bm25_loaded=True,
        )

    def _chunk_list_response(self):
        from backend.schemas.vectordb_schema import ChunkListResponse
        return ChunkListResponse(total=0, skip=0, limit=20, chunks=[])

    def test_vectordb_status_returns_200_when_loaded(self, client):
        with patch(
            "backend.routes.vectordb.get_vectordb_status",
            return_value=self._status_response(total_vectors=42),
        ):
            resp = client.get("/api/vectordb/status")
        assert resp.status_code == 200

    def test_vectordb_status_response_fields(self, client):
        with patch(
            "backend.routes.vectordb.get_vectordb_status",
            return_value=self._status_response(total_vectors=42),
        ):
            data = client.get("/api/vectordb/status").json()
        assert data["total_vectors"] == 42
        assert "dimension" in data
        assert "index_type" in data

    def test_vectordb_status_empty_returns_503(self, client):
        with patch(
            "backend.routes.vectordb.get_vectordb_status",
            return_value=self._status_response(total_vectors=0),
        ):
            resp = client.get("/api/vectordb/status")
        assert resp.status_code == 503

    def test_vectordb_chunks_returns_200_when_loaded(self, client):
        with (
            patch(
                "backend.routes.vectordb.get_vectordb_status",
                return_value=self._status_response(total_vectors=10),
            ),
            patch(
                "backend.routes.vectordb.list_chunks",
                return_value=self._chunk_list_response(),
            ),
        ):
            resp = client.get("/api/vectordb/chunks")
        assert resp.status_code == 200

    def test_vectordb_chunks_returns_503_when_empty(self, client):
        with patch(
            "backend.routes.vectordb.get_vectordb_status",
            return_value=self._status_response(total_vectors=0),
        ):
            resp = client.get("/api/vectordb/chunks")
        assert resp.status_code == 503

    def test_vectordb_chunks_pagination_params(self, client):
        with (
            patch(
                "backend.routes.vectordb.get_vectordb_status",
                return_value=self._status_response(total_vectors=10),
            ),
            patch(
                "backend.routes.vectordb.list_chunks",
                return_value=self._chunk_list_response(),
            ),
        ):
            resp = client.get("/api/vectordb/chunks?skip=5&limit=10")
        assert resp.status_code == 200

    def test_vectordb_chunks_search_no_criteria_returns_400(self, client):
        with patch(
            "backend.routes.vectordb.get_vectordb_status",
            return_value=self._status_response(total_vectors=10),
        ):
            resp = client.post(
                "/api/vectordb/chunks/search",
                json={},
            )
        assert resp.status_code == 400

    def test_vectordb_chunks_search_with_keyword(self, client):
        from backend.schemas.vectordb_schema import ChunkSearchResponse
        mock_response = ChunkSearchResponse(match_count=0, chunks=[])
        with (
            patch(
                "backend.routes.vectordb.get_vectordb_status",
                return_value=self._status_response(total_vectors=10),
            ),
            patch(
                "backend.routes.vectordb.search_chunks",
                return_value=mock_response,
            ),
        ):
            resp = client.post(
                "/api/vectordb/chunks/search",
                json={"keyword": "termination"},
            )
        assert resp.status_code == 200


# ===========================================================================
# Response Header Tests
# ===========================================================================

class TestResponseHeaders:

    def test_request_id_header_present(self, client):
        resp = client.get("/health")
        assert "x-request-id" in resp.headers

    def test_process_time_header_present(self, client):
        resp = client.get("/health")
        assert "x-process-time" in resp.headers

    def test_process_time_is_numeric(self, client):
        resp = client.get("/health")
        process_time = resp.headers.get("x-process-time", "")
        assert float(process_time) >= 0
