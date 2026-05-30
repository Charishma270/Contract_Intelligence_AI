"""
Day 19 — Schema Contract Tests
================================
Verifies all frontend-facing response schemas:
  - Can be instantiated with valid data
  - Field validation constraints work (ge, le, etc.)
  - Optional fields default correctly
  - __init__.py exports are complete and importable
"""

import pytest
from datetime import datetime


# -------------------------------------------------------------------
# Test: All schemas importable from __init__.py
# -------------------------------------------------------------------

class TestSchemaExports:
    """Verify __init__.py exports are complete."""

    def test_ocr_exports(self):
        from backend.schemas import OCRChunk, OCROutput
        assert OCRChunk is not None
        assert OCROutput is not None

    def test_nlp_exports(self):
        from backend.schemas import (
            ClausePrediction,
            EntityPrediction,
            NLPOutput,
        )
        assert ClausePrediction is not None
        assert EntityPrediction is not None
        assert NLPOutput is not None

    def test_rag_exports(self):
        from backend.schemas import (
            RetrievedChunk,
            ChatRequest,
            ChatResponse,
            QueryRequest,
            QueryResponse,
            MultiLabelPrediction,
            ClauseResult,
            ContractSummary,
        )
        for cls in [
            RetrievedChunk, ChatRequest, ChatResponse,
            QueryRequest, QueryResponse,
            MultiLabelPrediction, ClauseResult, ContractSummary,
        ]:
            assert cls is not None

    def test_contract_exports(self):
        from backend.schemas import (
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
        for cls in [
            ContractStatus, ContractMetadata,
            RiskBreakdown, RiskScoreResponse,
            AnalysisResponse, UploadResponse,
            AsyncTaskResponse, TaskStatusResponse,
            TaskRevokeResponse,
        ]:
            assert cls is not None

    def test_vectordb_exports(self):
        from backend.schemas import (
            VectorDBStatusResponse,
            ChunkDetail,
            ChunkListResponse,
            ChunkSearchRequest,
            ChunkSearchResponse,
        )
        for cls in [
            VectorDBStatusResponse, ChunkDetail,
            ChunkListResponse, ChunkSearchRequest,
            ChunkSearchResponse,
        ]:
            assert cls is not None


# -------------------------------------------------------------------
# Test: ContractMetadata
# -------------------------------------------------------------------

class TestContractMetadata:

    def test_valid_creation(self):
        from backend.schemas.contract_schema import ContractMetadata
        meta = ContractMetadata(
            contract_id="abc-123",
            filename="contract.pdf",
        )
        assert meta.contract_id == "abc-123"
        assert meta.filename == "contract.pdf"
        assert meta.status.value == "uploaded"
        assert meta.error_message is None
        assert meta.file_size_bytes is None

    def test_all_fields(self):
        from backend.schemas.contract_schema import (
            ContractMetadata,
            ContractStatus,
        )
        meta = ContractMetadata(
            contract_id="abc-123",
            filename="contract.pdf",
            status=ContractStatus.COMPLETED,
            error_message=None,
            file_size_bytes=1024,
        )
        assert meta.status == ContractStatus.COMPLETED
        assert meta.file_size_bytes == 1024


# -------------------------------------------------------------------
# Test: UploadResponse (Day 19 enhancements)
# -------------------------------------------------------------------

class TestUploadResponse:

    def test_defaults(self):
        from backend.schemas.contract_schema import UploadResponse
        resp = UploadResponse(
            contract_id="test-id",
            filename="test.pdf",
        )
        assert resp.status == "uploaded"
        assert resp.message == "File uploaded successfully"
        assert resp.file_size_bytes is None
        assert isinstance(resp.timestamp, datetime)

    def test_with_file_size(self):
        from backend.schemas.contract_schema import UploadResponse
        resp = UploadResponse(
            contract_id="test-id",
            filename="test.pdf",
            file_size_bytes=2048576,
        )
        assert resp.file_size_bytes == 2048576

    def test_custom_message(self):
        from backend.schemas.contract_schema import UploadResponse
        resp = UploadResponse(
            contract_id="id",
            filename="f.pdf",
            message="12 chunks indexed",
        )
        assert resp.message == "12 chunks indexed"


# -------------------------------------------------------------------
# Test: RiskScoreResponse (consolidated from risk.py)
# -------------------------------------------------------------------

class TestRiskScoreResponse:

    def test_valid_creation(self):
        from backend.schemas.contract_schema import (
            RiskScoreResponse,
            RiskBreakdown,
        )
        resp = RiskScoreResponse(
            contract_id="test",
            overall_risk=65,
            severity="medium",
            breakdown=[
                RiskBreakdown(
                    factor="Unlimited liability",
                    score=30,
                    severity="high",
                    description="No liability cap found",
                ),
            ],
        )
        assert resp.overall_risk == 65
        assert resp.severity == "medium"
        assert len(resp.breakdown) == 1

    def test_risk_score_bounds(self):
        from backend.schemas.contract_schema import RiskScoreResponse
        with pytest.raises(Exception):
            RiskScoreResponse(
                contract_id="test",
                overall_risk=101,  # exceeds max
                severity="high",
            )

    def test_risk_score_negative(self):
        from backend.schemas.contract_schema import RiskScoreResponse
        with pytest.raises(Exception):
            RiskScoreResponse(
                contract_id="test",
                overall_risk=-1,  # below min
                severity="low",
            )

    def test_empty_breakdown(self):
        from backend.schemas.contract_schema import RiskScoreResponse
        resp = RiskScoreResponse(
            contract_id="test",
            overall_risk=0,
            severity="low",
        )
        assert resp.breakdown == []


# -------------------------------------------------------------------
# Test: TaskRevokeResponse (new Day 19)
# -------------------------------------------------------------------

class TestTaskRevokeResponse:

    def test_valid_creation(self):
        from backend.schemas.contract_schema import TaskRevokeResponse
        resp = TaskRevokeResponse(
            task_id="celery-123",
            message="Task revoked successfully",
        )
        assert resp.task_id == "celery-123"
        assert resp.status == "revoked"
        assert "revoked" in resp.message.lower()


# -------------------------------------------------------------------
# Test: AsyncTaskResponse
# -------------------------------------------------------------------

class TestAsyncTaskResponse:

    def test_defaults(self):
        from backend.schemas.contract_schema import AsyncTaskResponse
        resp = AsyncTaskResponse(
            task_id="task-1",
            contract_id="contract-1",
        )
        assert resp.status == "processing"
        assert resp.message == "Analysis task submitted successfully"


# -------------------------------------------------------------------
# Test: TaskStatusResponse
# -------------------------------------------------------------------

class TestTaskStatusResponse:

    def test_pending(self):
        from backend.schemas.contract_schema import TaskStatusResponse
        resp = TaskStatusResponse(
            task_id="task-1",
            state="PENDING",
        )
        assert resp.progress is None
        assert resp.result is None
        assert resp.error is None

    def test_success(self):
        from backend.schemas.contract_schema import TaskStatusResponse
        resp = TaskStatusResponse(
            task_id="task-1",
            state="SUCCESS",
            result={"risk_score": 42},
        )
        assert resp.result == {"risk_score": 42}

    def test_failure(self):
        from backend.schemas.contract_schema import TaskStatusResponse
        resp = TaskStatusResponse(
            task_id="task-1",
            state="FAILURE",
            error="Model not loaded",
        )
        assert resp.error == "Model not loaded"


# -------------------------------------------------------------------
# Test: ContractSummary (Day 19: average_confidence)
# -------------------------------------------------------------------

class TestContractSummary:

    def test_defaults(self):
        from backend.schemas.rag_schema import ContractSummary
        summary = ContractSummary(overall_risk="Low")
        assert summary.high_confidence_clauses == 0
        assert summary.average_confidence == 0.0
        assert summary.top_detected_labels == []

    def test_with_average_confidence(self):
        from backend.schemas.rag_schema import ContractSummary
        summary = ContractSummary(
            overall_risk="High",
            top_detected_labels=["Termination", "Liability"],
            high_confidence_clauses=5,
            average_confidence=0.87,
        )
        assert summary.average_confidence == 0.87

    def test_average_confidence_bounds(self):
        from backend.schemas.rag_schema import ContractSummary
        with pytest.raises(Exception):
            ContractSummary(
                overall_risk="High",
                average_confidence=1.5,  # exceeds max
            )


# -------------------------------------------------------------------
# Test: ClausePrediction (Day 19: page_label)
# -------------------------------------------------------------------

class TestClausePrediction:

    def test_page_label_default(self):
        from backend.schemas.nlp_schema import ClausePrediction
        clause = ClausePrediction(
            clause_type="Termination",
            answer_text="May be terminated",
            confidence=0.95,
        )
        assert clause.page_label is None
        assert clause.page == 1

    def test_page_label_set(self):
        from backend.schemas.nlp_schema import ClausePrediction
        clause = ClausePrediction(
            clause_type="Termination",
            answer_text="May be terminated",
            confidence=0.95,
            page_label="Page 3 — Termination",
        )
        assert clause.page_label == "Page 3 — Termination"

    def test_confidence_bounds(self):
        from backend.schemas.nlp_schema import ClausePrediction
        with pytest.raises(Exception):
            ClausePrediction(
                clause_type="Test",
                answer_text="text",
                confidence=1.5,  # exceeds max
            )


# -------------------------------------------------------------------
# Test: AnalysisResponse
# -------------------------------------------------------------------

class TestAnalysisResponse:

    def test_valid_creation(self):
        from backend.schemas.contract_schema import (
            AnalysisResponse,
            ContractStatus,
        )
        resp = AnalysisResponse(
            contract_id="test",
            filename="test.pdf",
            status=ContractStatus.COMPLETED,
        )
        assert resp.risk_score == 0
        assert resp.risk_severity == "low"
        assert resp.clauses == []
        assert resp.entities == []
        assert resp.risk_breakdown == []


# -------------------------------------------------------------------
# Test: ChatResponse
# -------------------------------------------------------------------

class TestChatResponse:

    def test_valid_creation(self):
        from backend.schemas.rag_schema import ChatResponse
        resp = ChatResponse(
            answer="The termination clause states...",
        )
        assert resp.answer == "The termination clause states..."
        assert resp.retrieved_chunks == []
        assert resp.citations == []


# -------------------------------------------------------------------
# Test: QueryResponse
# -------------------------------------------------------------------

class TestQueryResponse:

    def test_valid_creation(self):
        from backend.schemas.rag_schema import (
            QueryResponse,
            ContractSummary,
        )
        resp = QueryResponse(
            summary=ContractSummary(overall_risk="Medium"),
            results=[],
        )
        assert resp.summary.overall_risk == "Medium"
        assert resp.results == []
