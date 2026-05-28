"""
Celery Tasks Tests
===================
Day 17: Unit tests for Celery async task processing.

Tests cover:
  - Task definition and registration
  - Task execution with mocked pipeline
  - Task state transitions (PENDING → STARTED → SUCCESS)
  - Failure handling (FAILURE state + contract status update)
  - Task info helper function
  - Async API endpoints (submit, poll, revoke)
  - Schema validation for new async models

Run with:
    pytest tests/backend/test_celery_tasks.py -v
"""

import sys
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_contract_id():
    """Generate a fresh UUID for each test."""
    return str(uuid.uuid4())


@pytest.fixture
def mock_contract_metadata(mock_contract_id):
    """Create a mock ContractMetadata object."""
    from backend.schemas.contract_schema import ContractMetadata, ContractStatus

    return ContractMetadata(
        contract_id=mock_contract_id,
        filename="test_contract.pdf",
        upload_time=datetime.now(timezone.utc),
        status=ContractStatus.UPLOADED,
        file_size_bytes=1024,
    )


@pytest.fixture
def mock_analysis_response(mock_contract_id):
    """Create a mock AnalysisResponse for successful pipeline runs."""
    from backend.schemas.contract_schema import (
        AnalysisResponse,
        ContractStatus,
        RiskBreakdown,
    )

    return AnalysisResponse(
        contract_id=mock_contract_id,
        filename="test_contract.pdf",
        status=ContractStatus.COMPLETED,
        risk_score=45,
        risk_severity="medium",
        clauses=[],
        entities=[],
        risk_breakdown=[
            RiskBreakdown(
                factor="Base Contract Risk",
                score=30,
                severity="low",
                description="Baseline risk inherent in any legal contract.",
            )
        ],
    )


# ---------------------------------------------------------------------------
# Test 1: Schema models
# ---------------------------------------------------------------------------
class TestAsyncSchemas:
    """Test the new Pydantic models for async tasks."""

    def test_async_task_response_creation(self, mock_contract_id):
        """AsyncTaskResponse should serialize correctly."""
        from backend.schemas.contract_schema import AsyncTaskResponse

        task_id = str(uuid.uuid4())
        response = AsyncTaskResponse(
            task_id=task_id,
            contract_id=mock_contract_id,
            status="processing",
            message="Test message",
        )
        assert response.task_id == task_id
        assert response.contract_id == mock_contract_id
        assert response.status == "processing"

    def test_task_status_response_success(self):
        """TaskStatusResponse should handle SUCCESS state."""
        from backend.schemas.contract_schema import TaskStatusResponse

        response = TaskStatusResponse(
            task_id="abc-123",
            state="SUCCESS",
            result={"contract_id": "test", "risk_score": 50},
        )
        assert response.state == "SUCCESS"
        assert response.result is not None
        assert response.error is None

    def test_task_status_response_failure(self):
        """TaskStatusResponse should handle FAILURE state."""
        from backend.schemas.contract_schema import TaskStatusResponse

        response = TaskStatusResponse(
            task_id="abc-123",
            state="FAILURE",
            error="Pipeline crashed",
        )
        assert response.state == "FAILURE"
        assert response.error == "Pipeline crashed"
        assert response.result is None

    def test_task_status_response_progress(self):
        """TaskStatusResponse should handle PROGRESS state."""
        from backend.schemas.contract_schema import TaskStatusResponse

        progress = {
            "current_stage": "nlp",
            "stage_label": "NLP Clause Classification & NER",
            "step": 2,
            "total_steps": 4,
            "percent": 25,
        }
        response = TaskStatusResponse(
            task_id="abc-123",
            state="PROGRESS",
            progress=progress,
        )
        assert response.state == "PROGRESS"
        assert response.progress["current_stage"] == "nlp"
        assert response.progress["percent"] == 25

    def test_contract_status_has_processing(self):
        """ContractStatus enum should include PROCESSING."""
        from backend.schemas.contract_schema import ContractStatus

        assert hasattr(ContractStatus, "PROCESSING")
        assert ContractStatus.PROCESSING.value == "processing"


# ---------------------------------------------------------------------------
# Test 2: Celery configuration
# ---------------------------------------------------------------------------
class TestCeleryConfig:
    """Test Celery app configuration."""

    def test_celery_app_exists(self):
        """Celery app should be importable."""
        from backend.celery_config import celery_app

        assert celery_app is not None
        assert celery_app.main == "contract_ai"

    def test_celery_config_defaults(self):
        """Celery should have correct default configuration."""
        from backend.celery_config import celery_app

        assert celery_app.conf.task_serializer == "json"
        assert celery_app.conf.result_serializer == "json"
        assert celery_app.conf.task_acks_late is True
        assert celery_app.conf.task_track_started is True
        assert celery_app.conf.task_time_limit == 300
        assert celery_app.conf.task_soft_time_limit == 240
        assert celery_app.conf.result_expires == 86400

    def test_celery_task_routes(self):
        """Task routes should direct to the 'analysis' queue."""
        from backend.celery_config import celery_app

        routes = celery_app.conf.task_routes
        assert "backend.services.celery_tasks.*" in routes
        assert routes["backend.services.celery_tasks.*"]["queue"] == "analysis"


# ---------------------------------------------------------------------------
# Test 3: Task registration
# ---------------------------------------------------------------------------
class TestTaskRegistration:
    """Test that tasks are properly registered with Celery."""

    def test_run_pipeline_async_is_registered(self):
        """The main pipeline task should be importable."""
        from backend.services.celery_tasks import run_pipeline_async

        assert run_pipeline_async is not None
        assert run_pipeline_async.name == "backend.services.celery_tasks.run_pipeline_async"


# ---------------------------------------------------------------------------
# Test 4: Task execution (mocked pipeline)
# ---------------------------------------------------------------------------
class TestTaskExecution:
    """Test task execution with mocked dependencies."""

    @pytest.fixture(autouse=True)
    def _mock_pipeline_module(self):
        """
        Pre-register a fake backend.services.pipeline module in sys.modules
        so that the lazy import inside celery_tasks doesn't cascade into
        RAG/OCR/NLP dependencies that aren't installed in test env.
        """
        mock_pipeline = MagicMock()
        original = sys.modules.get("backend.services.pipeline")
        sys.modules["backend.services.pipeline"] = mock_pipeline
        self._mock_pipeline = mock_pipeline
        yield
        # Restore
        if original is not None:
            sys.modules["backend.services.pipeline"] = original
        else:
            sys.modules.pop("backend.services.pipeline", None)

    @pytest.fixture(autouse=True)
    def _celery_eager_mode(self):
        """
        Configure Celery to run tasks eagerly (in-process, no broker needed)
        so self.update_state() and self.request.id work without Redis.
        """
        from backend.celery_config import celery_app
        celery_app.conf.update(
            task_always_eager=True,
            task_eager_propagates=False,
            result_backend="cache+memory://",
        )
        yield
        celery_app.conf.update(
            task_always_eager=False,
            task_eager_propagates=False,
            result_backend="redis://localhost:6379/1",
        )

    @patch("backend.services.celery_tasks.update_contract_status")
    @patch("backend.services.celery_tasks.get_contract")
    def test_task_fails_for_missing_contract(
        self, mock_get_contract, mock_update_status, mock_contract_id
    ):
        """Task should raise ValueError for non-existent contract."""
        from backend.services.celery_tasks import run_pipeline_async

        mock_get_contract.return_value = None
        mock_update_status.return_value = None

        # .apply() runs the task synchronously with a proper request context
        result = run_pipeline_async.apply(args=[mock_contract_id])
        # Task should fail — check the exception
        assert result.failed()
        assert "not found" in str(result.result)

    @patch("backend.services.celery_tasks.update_contract_status")
    @patch("backend.services.celery_tasks.get_contract")
    def test_task_success_path(
        self,
        mock_get_contract,
        mock_update_status,
        mock_contract_id,
        mock_contract_metadata,
        mock_analysis_response,
    ):
        """Task should return serialized AnalysisResponse on success."""
        from backend.services.celery_tasks import run_pipeline_async

        mock_get_contract.return_value = mock_contract_metadata
        mock_update_status.return_value = None
        self._mock_pipeline.run_pipeline.return_value = mock_analysis_response

        # .apply() runs the task synchronously with a proper request context
        result = run_pipeline_async.apply(args=[mock_contract_id])
        assert result.successful()
        result_dict = result.result

        assert isinstance(result_dict, dict)
        assert result_dict["contract_id"] == mock_contract_id
        assert result_dict["risk_score"] == 45
        assert result_dict["status"] == "completed"

    @patch("backend.services.celery_tasks.update_contract_status")
    @patch("backend.services.celery_tasks.get_contract")
    def test_task_failure_updates_contract_status(
        self,
        mock_get_contract,
        mock_update_status,
        mock_contract_id,
        mock_contract_metadata,
    ):
        """On pipeline failure, contract status should be set to FAILED."""
        from backend.services.celery_tasks import run_pipeline_async
        from backend.schemas.contract_schema import ContractStatus

        mock_get_contract.return_value = mock_contract_metadata
        mock_update_status.return_value = None
        self._mock_pipeline.run_pipeline.side_effect = RuntimeError("OCR crashed")

        # .apply() runs the task synchronously with a proper request context
        result = run_pipeline_async.apply(args=[mock_contract_id])
        assert result.failed()
        assert "OCR crashed" in str(result.result)

        # Verify contract status was updated to FAILED
        mock_update_status.assert_any_call(
            mock_contract_id,
            ContractStatus.FAILED,
            error_message="Async pipeline error: OCR crashed",
        )


# ---------------------------------------------------------------------------
# Test 5: get_task_info helper
# ---------------------------------------------------------------------------
class TestGetTaskInfo:
    """Test the task info helper function."""

    @patch("backend.services.celery_tasks.AsyncResult")
    def test_pending_state(self, mock_async_result_cls):
        """PENDING state should return waiting progress."""
        from backend.services.celery_tasks import get_task_info

        mock_result = MagicMock()
        mock_result.state = "PENDING"
        mock_async_result_cls.return_value = mock_result

        info = get_task_info("test-task-id")
        assert info["state"] == "PENDING"
        assert info["progress"]["current_stage"] == "pending"

    @patch("backend.services.celery_tasks.AsyncResult")
    def test_success_state(self, mock_async_result_cls):
        """SUCCESS state should return result data."""
        from backend.services.celery_tasks import get_task_info

        mock_result = MagicMock()
        mock_result.state = "SUCCESS"
        mock_result.result = {"contract_id": "abc", "risk_score": 50}
        mock_async_result_cls.return_value = mock_result

        info = get_task_info("test-task-id")
        assert info["state"] == "SUCCESS"
        assert info["result"]["risk_score"] == 50

    @patch("backend.services.celery_tasks.AsyncResult")
    def test_failure_state_with_exception(self, mock_async_result_cls):
        """FAILURE state with exception should return error string."""
        from backend.services.celery_tasks import get_task_info

        mock_result = MagicMock()
        mock_result.state = "FAILURE"
        mock_result.info = RuntimeError("Something broke")
        mock_async_result_cls.return_value = mock_result

        info = get_task_info("test-task-id")
        assert info["state"] == "FAILURE"
        assert "Something broke" in info["error"]

    @patch("backend.services.celery_tasks.AsyncResult")
    def test_progress_state(self, mock_async_result_cls):
        """PROGRESS state should pass through meta info."""
        from backend.services.celery_tasks import get_task_info

        progress_meta = {
            "current_stage": "nlp",
            "stage_label": "NLP Clause Classification & NER",
            "step": 2,
            "total_steps": 4,
            "percent": 25,
        }
        mock_result = MagicMock()
        mock_result.state = "PROGRESS"
        mock_result.info = progress_meta
        mock_async_result_cls.return_value = mock_result

        info = get_task_info("test-task-id")
        assert info["state"] == "PROGRESS"
        assert info["progress"]["current_stage"] == "nlp"

    @patch("backend.services.celery_tasks.AsyncResult")
    def test_revoked_state(self, mock_async_result_cls):
        """REVOKED state should return cancellation error."""
        from backend.services.celery_tasks import get_task_info

        mock_result = MagicMock()
        mock_result.state = "REVOKED"
        mock_async_result_cls.return_value = mock_result

        info = get_task_info("test-task-id")
        assert info["state"] == "REVOKED"
        assert info["error"] == "Task was cancelled"


# ---------------------------------------------------------------------------
# Test 6: API endpoints (via TestClient)
# ---------------------------------------------------------------------------
# Skip endpoint tests if OCR dependencies are missing (pdf2image, etc.)
try:
    from main import app as _test_app
    _HAS_APP = True
except ImportError:
    _test_app = None
    _HAS_APP = False


@pytest.mark.skipif(not _HAS_APP, reason="OCR dependencies not installed (pdf2image)")
class TestAsyncEndpoints:
    """Test the async analysis API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a FastAPI test client."""
        return TestClient(_test_app)

    @patch("backend.routes.async_analyze.run_pipeline_async")
    @patch("backend.routes.async_analyze.update_contract_status")
    @patch("backend.routes.async_analyze.validate_contract_not_failed")
    def test_submit_async_analysis(
        self,
        mock_validate,
        mock_update_status,
        mock_task,
        client,
        mock_contract_id,
        mock_contract_metadata,
    ):
        """POST /api/analyze/{id}/async should return 202 with task_id."""
        mock_validate.return_value = mock_contract_metadata

        mock_async_result = MagicMock()
        mock_async_result.id = "celery-task-123"
        mock_task.delay.return_value = mock_async_result

        response = client.post(f"/api/analyze/{mock_contract_id}/async")

        assert response.status_code == 202
        data = response.json()
        assert data["task_id"] == "celery-task-123"
        assert data["contract_id"] == mock_contract_id
        assert data["status"] == "processing"

    @patch("backend.routes.async_analyze.get_task_info")
    def test_get_task_status_success(self, mock_get_info, client):
        """GET /api/tasks/{task_id} should return task status."""
        mock_get_info.return_value = {
            "task_id": "celery-task-123",
            "state": "SUCCESS",
            "progress": {
                "current_stage": "completed",
                "stage_label": "Pipeline completed",
                "step": 4,
                "total_steps": 4,
                "percent": 100,
            },
            "result": {"contract_id": "abc", "risk_score": 50},
            "error": None,
        }

        response = client.get("/api/tasks/celery-task-123")

        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "SUCCESS"
        assert data["result"]["risk_score"] == 50

    @patch("backend.routes.async_analyze.get_task_info")
    def test_get_task_status_progress(self, mock_get_info, client):
        """GET /api/tasks/{task_id} should return progress info."""
        mock_get_info.return_value = {
            "task_id": "celery-task-123",
            "state": "PROGRESS",
            "progress": {
                "current_stage": "nlp",
                "stage_label": "NLP Clause Classification & NER",
                "step": 2,
                "total_steps": 4,
                "percent": 25,
            },
            "result": None,
            "error": None,
        }

        response = client.get("/api/tasks/celery-task-123")

        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "PROGRESS"
        assert data["progress"]["current_stage"] == "nlp"

    @patch("backend.routes.async_analyze.AsyncResult")
    def test_revoke_task(self, mock_async_result_cls, client):
        """POST /api/tasks/{task_id}/revoke should return confirmation."""
        mock_result = MagicMock()
        mock_async_result_cls.return_value = mock_result

        response = client.post("/api/tasks/celery-task-123/revoke")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "revoked"
        assert data["task_id"] == "celery-task-123"
        mock_result.revoke.assert_called_once_with(
            terminate=True, signal="SIGTERM"
        )


# ---------------------------------------------------------------------------
# Test 7: Pipeline stage definitions
# ---------------------------------------------------------------------------
class TestPipelineStages:
    """Test pipeline stage metadata constants."""

    def test_pipeline_stages_count(self):
        """Should have exactly 4 pipeline stages."""
        from backend.services.celery_tasks import PIPELINE_STAGES

        assert len(PIPELINE_STAGES) == 4

    def test_pipeline_stages_keys(self):
        """Should have ocr, nlp, rag, risk stages."""
        from backend.services.celery_tasks import PIPELINE_STAGES

        expected = {"ocr", "nlp", "rag", "risk"}
        assert set(PIPELINE_STAGES.keys()) == expected

    def test_pipeline_stages_order(self):
        """Stages should be numbered 1-4."""
        from backend.services.celery_tasks import PIPELINE_STAGES

        steps = [v["step"] for v in PIPELINE_STAGES.values()]
        assert sorted(steps) == [1, 2, 3, 4]
