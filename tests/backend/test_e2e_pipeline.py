"""
End-to-End Pipeline Integration Tests
=======================================
Day 16: Validates the full contract analysis pipeline from upload through
OCR → NLP → RAG indexing → Risk scoring.

All heavy ML dependencies (torch, transformers, spaCy, FAISS, Tesseract,
pdfplumber) are mocked so tests run fast in CI without model weights.

Tests are grouped into:
  1. Happy Path         — full pipeline success scenarios
  2. Error Handling     — failure propagation and error responses
  3. Endpoint Validation— individual endpoint contract compliance
  4. Data Flow          — verify data passes correctly between stages

Uses FastAPI TestClient for HTTP-level integration testing.
"""

import io
import os
import sys
import uuid

import pytest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Pre-mock heavy modules BEFORE any application imports happen.
#
# The import chain is:
#   main.py → backend.routes.upload → ocr.ocr_pipeline
#           → pdf2image, pytesseract, sentence_transformers, faiss
#           → rag.retrieval.embedder, rag.vector_db.faiss_store
#   main.py → backend.routes.rag_routes → backend.services.rag_service
#           → rag.pipeline.pipeline → risk_engine.*, sentence_transformers, faiss
#   main.py → backend.routes.chat → backend.services.rag
#           → rag.retrieval.embedder, rag.vector_db.faiss_store
#   main.py → backend.routes.frontend_analyze → backend.services.rag_service
#
# We mock:
#   1. Third-party ML libs (sentence_transformers, faiss, pdf2image, etc.)
#   2. Specific leaf-level sub-modules with heavy deps (rag.retrieval.embedder,
#      rag.vector_db.faiss_store, rag.pipeline.pipeline, ocr.ocr_pipeline)
#   3. risk_engine.* (not installed as a package, imports will fail)
# ---------------------------------------------------------------------------


# Build mock modules for the generate_embedding return value
_mock_embedding = [0.0] * 384  # plain list, no numpy needed

# Create specific mock modules for rag sub-packages
_mock_embedder_module = MagicMock()
_mock_embedder_module.generate_embedding = MagicMock(return_value=_mock_embedding)
_mock_embedder_module.SentenceTransformer = MagicMock()

_mock_faiss_store_module = MagicMock()
_mock_faiss_store_module.add_embedding = MagicMock()
_mock_faiss_store_module.search_embedding = MagicMock(return_value=[])
_mock_faiss_store_module.save_index = MagicMock()
_mock_faiss_store_module.load_index = MagicMock()

_mock_rag_pipeline_module = MagicMock()
_mock_rag_pipeline_module.run_pipeline = MagicMock(return_value={
    "summary": {"overall_risk": "Low", "top_detected_labels": [], "high_confidence_clauses": 0},
    "results": [],
})

_mock_ocr_pipeline_module = MagicMock()
_mock_ocr_pipeline_module.process_contract = MagicMock(return_value=[])

# Mock heavy third-party libraries AND sub-module paths
_mock_modules = {
    # Third-party ML libraries
    "sentence_transformers": MagicMock(),
    "faiss": MagicMock(),
    "pdf2image": MagicMock(convert_from_path=MagicMock(return_value=[])),
    "pytesseract": MagicMock(),
    "pdfplumber": MagicMock(),
    "torch": MagicMock(),
    "transformers": MagicMock(),
    "spacy": MagicMock(),
    # Risk engine hierarchy (not a proper package on disk)
    "risk_engine": MagicMock(),
    "risk_engine.analysis": MagicMock(),
    "risk_engine.analysis.classifier_inference": MagicMock(
        classify_clause=MagicMock(return_value="Unknown"),
    ),
    "risk_engine.analysis.legal_bert_inference": MagicMock(
        predict_clause_with_legal_bert=MagicMock(
            return_value={"prediction": "Unknown", "confidence": 0.5}
        ),
    ),
    "risk_engine.analysis.multilabel_legal_bert_inference": MagicMock(
        predict_multilabel_legal_bert=MagicMock(return_value=[]),
    ),
    "risk_engine.scoring": MagicMock(),
    "risk_engine.scoring.risk_rules": MagicMock(
        calculate_risk=MagicMock(return_value="Low"),
    ),
    # Leaf-level rag sub-modules with heavy deps
    "rag.retrieval.embedder": _mock_embedder_module,
    "rag.vector_db.faiss_store": _mock_faiss_store_module,
    "rag.pipeline.pipeline": _mock_rag_pipeline_module,
    # OCR pipeline sub-module with heavy deps
    "ocr.ocr_pipeline": _mock_ocr_pipeline_module,
}

# Save originals and inject mocks
_originals = {}
for mod_name, mock_obj in _mock_modules.items():
    _originals[mod_name] = sys.modules.get(mod_name)
    sys.modules[mod_name] = mock_obj

# Now we can safely import application modules
from fastapi.testclient import TestClient

from backend.schemas.contract_schema import (
    AnalysisResponse,
    ContractStatus,
    RiskBreakdown,
)
from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction, NLPOutput
from backend.schemas.ocr_schema import OCRChunk, OCROutput
from backend.utils.exceptions import (
    OCRProcessingError,
    NLPProcessingError,
)


# ---------------------------------------------------------------------------
# Helpers: Build realistic mock data
# ---------------------------------------------------------------------------
def _make_minimal_pdf() -> bytes:
    """
    Create a minimal valid PDF in memory (sufficient to pass %PDF- check).
    """
    return (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"xref\n0 4\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer<</Size 4/Root 1 0 R>>\n"
        b"startxref\n183\n%%EOF"
    )


def _make_mock_ocr_output(contract_id: str) -> OCROutput:
    """Build a realistic OCROutput with legal contract text chunks."""
    return OCROutput(
        contract_id=contract_id,
        chunks=[
            OCRChunk(
                contract_id=contract_id,
                chunk_id="chunk-001",
                page=1,
                text=(
                    "MASTER SERVICES AGREEMENT. This Agreement is entered into "
                    "as of January 15, 2025, by and between Acme Corporation, "
                    "a Delaware corporation, and TechServ Solutions Inc., a "
                    "California corporation."
                ),
                source_file=f"uploads/{contract_id}.pdf",
                extraction_method="pdfplumber",
            ),
            OCRChunk(
                contract_id=contract_id,
                chunk_id="chunk-002",
                page=2,
                text=(
                    "2.1 Term. The initial term of this Agreement shall be "
                    "three (3) years from the Effective Date. 2.2 Renewal. "
                    "This Agreement shall automatically renew for successive "
                    "one (1) year periods unless either party provides written "
                    "notice of non-renewal at least ninety (90) days prior to "
                    "the end of the then-current term."
                ),
                source_file=f"uploads/{contract_id}.pdf",
                extraction_method="pdfplumber",
            ),
            OCRChunk(
                contract_id=contract_id,
                chunk_id="chunk-003",
                page=2,
                text=(
                    "2.3 Termination for Convenience. Either party may "
                    "terminate this Agreement for convenience upon sixty (60) "
                    "days' prior written notice to the other party."
                ),
                source_file=f"uploads/{contract_id}.pdf",
                extraction_method="pdfplumber",
            ),
            OCRChunk(
                contract_id=contract_id,
                chunk_id="chunk-004",
                page=3,
                text=(
                    "3.1 Cap on Liability. EXCEPT FOR OBLIGATIONS UNDER "
                    "SECTION 5, NEITHER PARTY'S TOTAL AGGREGATE LIABILITY "
                    "SHALL EXCEED THE AMOUNTS PAID OR PAYABLE UNDER THIS "
                    "AGREEMENT DURING THE TWELVE (12) MONTH PERIOD PRECEDING "
                    "THE CLAIM."
                ),
                source_file=f"uploads/{contract_id}.pdf",
                extraction_method="pdfplumber",
            ),
        ],
        total_pages=3,
        extraction_method="pdfplumber",
        processing_time_seconds=0.42,
    )


def _make_mock_nlp_output(contract_id: str) -> NLPOutput:
    """Build a realistic NLPOutput with clause predictions and entities."""
    return NLPOutput(
        contract_id=contract_id,
        clauses=[
            ClausePrediction(
                clause_type="Termination For Convenience",
                answer_text=(
                    "Either party may terminate this Agreement for convenience "
                    "upon sixty (60) days' prior written notice."
                ),
                start_char=0,
                end_char=95,
                page=2,
                confidence=0.94,
                is_present=True,
            ),
            ClausePrediction(
                clause_type="Renewal Term",
                answer_text=(
                    "This Agreement shall automatically renew for successive "
                    "one (1) year periods."
                ),
                start_char=0,
                end_char=75,
                page=2,
                confidence=0.91,
                is_present=True,
            ),
            ClausePrediction(
                clause_type="Cap On Liability",
                answer_text=(
                    "NEITHER PARTY'S TOTAL AGGREGATE LIABILITY SHALL EXCEED "
                    "THE AMOUNTS PAID OR PAYABLE."
                ),
                start_char=0,
                end_char=80,
                page=3,
                confidence=0.88,
                is_present=True,
            ),
        ],
        entities=[
            EntityPrediction(
                entity_type="ORGANIZATION",
                value="Acme Corporation",
                position=10,
            ),
            EntityPrediction(
                entity_type="ORGANIZATION",
                value="TechServ Solutions Inc.",
                position=50,
            ),
            EntityPrediction(
                entity_type="JURISDICTION",
                value="Delaware",
                position=30,
            ),
            EntityPrediction(
                entity_type="DATE",
                value="January 15, 2025",
                position=5,
            ),
        ],
        processing_time_seconds=1.23,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def _test_dirs():
    """Ensure uploads/ and data/ directories exist for the test session."""
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    yield


@pytest.fixture(autouse=True)
def _setup_test_env(_test_dirs):
    """Set up isolated test environment for each test."""
    from backend.services.tracking import init_db
    init_db()
    yield


@pytest.fixture
def client():
    """
    Create a FastAPI TestClient.

    Heavy ML modules are already pre-mocked at module level above,
    so the app can be imported safely.
    """
    from main import app
    with TestClient(app) as tc:
        yield tc


@pytest.fixture
def uploaded_contract(client):
    """
    Upload a test PDF and return the contract_id.
    Cleans up the uploaded file after the test.
    """
    pdf_bytes = _make_minimal_pdf()
    response = client.post(
        "/api/upload",
        files={"file": ("test_contract.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
    )
    assert response.status_code == 201, f"Upload failed: {response.text}"
    data = response.json()
    contract_id = data["contract_id"]

    yield contract_id

    # Cleanup: remove uploaded file
    upload_path = os.path.join("uploads", f"{contract_id}.pdf")
    if os.path.exists(upload_path):
        os.remove(upload_path)


# ===========================================================================
# Test Group 1: Full Pipeline Happy Path
# ===========================================================================
class TestE2EPipelineHappyPath:
    """Verify the full analysis pipeline produces correct results."""

    def test_upload_then_analyze_full_pipeline(self, client, uploaded_contract):
        """
        Upload a PDF → /api/analyze/{id} → assert AnalysisResponse has
        status=completed, non-empty clauses, entities, and valid risk score.
        """
        contract_id = uploaded_contract
        mock_ocr = _make_mock_ocr_output(contract_id)
        mock_nlp = _make_mock_nlp_output(contract_id)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch("backend.services.pipeline.run_real_nlp", return_value=mock_nlp):

            response = client.post(f"/api/analyze/{contract_id}")

        assert response.status_code == 200, f"Analyze failed: {response.text}"

        data = response.json()
        assert data["contract_id"] == contract_id
        assert data["status"] == "completed"
        assert len(data["clauses"]) > 0, "Expected non-empty clauses"
        assert len(data["entities"]) > 0, "Expected non-empty entities"
        assert len(data["risk_breakdown"]) > 0, "Expected non-empty risk breakdown"
        assert 0 <= data["risk_score"] <= 100

    def test_pipeline_status_transitions(self, client, uploaded_contract):
        """
        Track contract status through each pipeline stage:
        uploaded → ocr_done → nlp_done → rag_indexed → completed
        """
        from backend.services.tracking import get_contract

        contract_id = uploaded_contract

        # Initially should be uploaded
        contract = get_contract(contract_id)
        assert contract is not None
        assert contract.status == ContractStatus.UPLOADED

        mock_ocr = _make_mock_ocr_output(contract_id)
        mock_nlp = _make_mock_nlp_output(contract_id)

        # Track status changes through the pipeline
        status_log = []

        from backend.services import tracking as tracking_module
        original_update = tracking_module.update_contract_status

        def tracking_spy(cid, status, error_message=None):
            status_log.append(status)
            return original_update(cid, status, error_message)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch("backend.services.pipeline.run_real_nlp", return_value=mock_nlp), \
             patch("backend.services.pipeline.update_contract_status", side_effect=tracking_spy):

            response = client.post(f"/api/analyze/{contract_id}")

        assert response.status_code == 200

        # Verify all status transitions occurred in order
        expected_transitions = [
            ContractStatus.OCR_DONE,
            ContractStatus.NLP_DONE,
            ContractStatus.RAG_INDEXED,
            ContractStatus.COMPLETED,
        ]
        assert status_log == expected_transitions, (
            f"Expected {expected_transitions}, got {status_log}"
        )

    def test_analysis_response_schema_compliance(self, client, uploaded_contract):
        """Assert all fields in the response match the AnalysisResponse Pydantic model."""
        contract_id = uploaded_contract
        mock_ocr = _make_mock_ocr_output(contract_id)
        mock_nlp = _make_mock_nlp_output(contract_id)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch("backend.services.pipeline.run_real_nlp", return_value=mock_nlp):

            response = client.post(f"/api/analyze/{contract_id}")

        data = response.json()

        # Validate top-level fields
        assert "contract_id" in data
        assert "filename" in data
        assert "status" in data
        assert "risk_score" in data
        assert "risk_severity" in data
        assert "clauses" in data
        assert "entities" in data
        assert "risk_breakdown" in data

        # Validate clause shape
        for clause in data["clauses"]:
            assert "clause_type" in clause
            assert "answer_text" in clause
            assert "confidence" in clause
            assert "is_present" in clause
            assert "page" in clause
            assert 0.0 <= clause["confidence"] <= 1.0

        # Validate entity shape
        for entity in data["entities"]:
            assert "entity_type" in entity
            assert "value" in entity

        # Validate risk breakdown shape
        for item in data["risk_breakdown"]:
            assert "factor" in item
            assert "score" in item
            assert "severity" in item
            assert "description" in item

        # Validate AnalysisResponse can be deserialized
        parsed = AnalysisResponse(**data)
        assert parsed.contract_id == contract_id

    def test_risk_score_within_bounds(self, client, uploaded_contract):
        """Verify risk_score is 0-100 and severity is a valid enum value."""
        contract_id = uploaded_contract
        mock_ocr = _make_mock_ocr_output(contract_id)
        mock_nlp = _make_mock_nlp_output(contract_id)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch("backend.services.pipeline.run_real_nlp", return_value=mock_nlp):

            response = client.post(f"/api/analyze/{contract_id}")

        data = response.json()
        assert 0 <= data["risk_score"] <= 100
        assert data["risk_severity"] in ["low", "medium", "high", "critical"]


# ===========================================================================
# Test Group 2: Pipeline Error Handling
# ===========================================================================
class TestE2EPipelineErrorHandling:
    """Verify pipeline handles failures gracefully with proper error responses."""

    def test_analyze_nonexistent_contract(self, client):
        """Call /api/analyze/{random_uuid} → 404 error."""
        fake_id = str(uuid.uuid4())
        response = client.post(f"/api/analyze/{fake_id}")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_analyze_invalid_contract_id(self, client):
        """Call /api/analyze/not-a-uuid → 400 error."""
        response = client.post("/api/analyze/not-a-uuid")
        assert response.status_code == 400
        data = response.json()
        assert "invalid" in data["detail"].lower() or "uuid" in data["detail"].lower()

    def test_analyze_already_failed_contract(self, client, uploaded_contract):
        """Insert a contract with status=failed, then analyze → 400 error."""
        from backend.services.tracking import update_contract_status

        contract_id = uploaded_contract
        update_contract_status(contract_id, ContractStatus.FAILED, "Previous OCR failure")

        response = client.post(f"/api/analyze/{contract_id}")
        assert response.status_code == 400
        data = response.json()
        assert "failed" in data["detail"].lower()

    def test_pipeline_ocr_failure_sets_failed_status(self, client, uploaded_contract):
        """Mock OCR to raise → contract status becomes 'failed' with error message."""
        from backend.services.tracking import get_contract

        contract_id = uploaded_contract

        with patch(
            "backend.services.pipeline.run_real_ocr",
            side_effect=OCRProcessingError(
                contract_id=contract_id,
                detail="Tesseract not found on system PATH",
            ),
        ):
            response = client.post(f"/api/analyze/{contract_id}")

        # The pipeline should propagate the error
        assert response.status_code == 500

        # Contract should be marked as failed in DB
        contract = get_contract(contract_id)
        assert contract is not None
        assert contract.status == ContractStatus.FAILED
        assert contract.error_message is not None
        assert "ocr" in contract.error_message.lower()

    def test_pipeline_nlp_failure_sets_failed_status(self, client, uploaded_contract):
        """Mock NLP to raise → contract status becomes 'failed' with error message."""
        from backend.services.tracking import get_contract

        contract_id = uploaded_contract
        mock_ocr = _make_mock_ocr_output(contract_id)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch(
                 "backend.services.pipeline.run_real_nlp",
                 side_effect=NLPProcessingError(
                     contract_id=contract_id,
                     detail="Legal-BERT model weights corrupted",
                 ),
             ):
            response = client.post(f"/api/analyze/{contract_id}")

        assert response.status_code == 500

        contract = get_contract(contract_id)
        assert contract is not None
        assert contract.status == ContractStatus.FAILED
        assert contract.error_message is not None
        assert "nlp" in contract.error_message.lower()


# ===========================================================================
# Test Group 3: Individual Endpoint Validation
# ===========================================================================
class TestEndpointIntegration:
    """Validate individual API endpoints work correctly."""

    def test_upload_returns_contract_id(self, client):
        """POST /api/upload with valid PDF → 201, response has contract_id."""
        pdf_bytes = _make_minimal_pdf()
        response = client.post(
            "/api/upload",
            files={"file": ("contract.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        )
        assert response.status_code == 201

        data = response.json()
        assert "contract_id" in data
        assert "filename" in data
        assert data["filename"] == "contract.pdf"
        assert data["status"] == "uploaded"

        # Validate UUID format
        parsed_uuid = uuid.UUID(data["contract_id"])
        assert str(parsed_uuid) == data["contract_id"]

        # Cleanup
        path = os.path.join("uploads", f"{data['contract_id']}.pdf")
        if os.path.exists(path):
            os.remove(path)

    def test_upload_invalid_file_type(self, client):
        """Upload a .txt file → 415 error."""
        response = client.post(
            "/api/upload",
            files={"file": ("document.txt", io.BytesIO(b"Hello world"), "text/plain")},
        )
        assert response.status_code == 415

    def test_upload_empty_file(self, client):
        """Upload 0-byte file → 400 error."""
        response = client.post(
            "/api/upload",
            files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")},
        )
        assert response.status_code == 400

    def test_contracts_list_after_upload(self, client, uploaded_contract):
        """Upload a file, then GET /api/contracts → contract appears in list."""
        contract_id = uploaded_contract

        response = client.get("/api/contracts")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        contract_ids = [c["contract_id"] for c in data]
        assert contract_id in contract_ids

    def test_contract_status_after_upload(self, client, uploaded_contract):
        """GET /api/contracts/{id} → status is 'uploaded'."""
        contract_id = uploaded_contract

        response = client.get(f"/api/contracts/{contract_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["contract_id"] == contract_id
        assert data["status"] == "uploaded"
        assert "filename" in data

    def test_risk_score_endpoint(self, client, uploaded_contract):
        """GET /api/risk/risk-score/{id} → returns RiskScoreResponse with breakdown."""
        contract_id = uploaded_contract

        response = client.get(f"/api/risk/risk-score/{contract_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["contract_id"] == contract_id
        assert "overall_risk" in data
        assert 0 <= data["overall_risk"] <= 100
        assert "severity" in data
        assert data["severity"] in ["low", "medium", "high", "critical"]
        assert "breakdown" in data
        assert isinstance(data["breakdown"], list)
        assert len(data["breakdown"]) > 0


# ===========================================================================
# Test Group 4: Pipeline Data Flow Validation
# ===========================================================================
class TestDataFlowIntegration:
    """Verify data passes correctly between pipeline stages."""

    def test_ocr_output_flows_to_nlp(self, client, uploaded_contract):
        """
        Verify the OCR output produced is actually passed to NLP.
        Uses a spy on run_real_nlp to inspect its ocr_output argument.
        """
        contract_id = uploaded_contract
        mock_ocr = _make_mock_ocr_output(contract_id)
        mock_nlp = _make_mock_nlp_output(contract_id)

        nlp_spy = MagicMock(return_value=mock_nlp)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch("backend.services.pipeline.run_real_nlp", nlp_spy):

            response = client.post(f"/api/analyze/{contract_id}")

        assert response.status_code == 200

        # Verify NLP was called with the contract_id and the OCR output
        nlp_spy.assert_called_once()
        call_args = nlp_spy.call_args
        assert call_args[0][0] == contract_id  # first positional arg
        passed_ocr = call_args[0][1]  # second positional arg
        assert isinstance(passed_ocr, OCROutput)
        assert passed_ocr.contract_id == contract_id
        assert len(passed_ocr.chunks) == 4  # our mock has 4 chunks

    def test_nlp_clauses_flow_to_risk_scoring(self, client, uploaded_contract):
        """
        Verify detected clauses correctly influence the risk score.
        Renewal Term → +20, Termination For Convenience → -5,
        Cap On Liability → -10, Base → +30. Expected = 35.
        """
        contract_id = uploaded_contract
        mock_ocr = _make_mock_ocr_output(contract_id)
        mock_nlp = _make_mock_nlp_output(contract_id)

        with patch("backend.services.pipeline.run_real_ocr", return_value=mock_ocr), \
             patch("backend.services.pipeline.run_real_nlp", return_value=mock_nlp):

            response = client.post(f"/api/analyze/{contract_id}")

        data = response.json()

        # Our mock NLP has: Renewal Term (+20), Termination For Convenience (-5),
        # Cap On Liability (-10), Base (+30) = 35
        assert data["risk_score"] == 35
        assert data["risk_severity"] == "medium"

        # Verify breakdown factors match
        factor_names = {b["factor"] for b in data["risk_breakdown"]}
        assert "Base Contract Risk" in factor_names
        assert "Auto-Renewal Clause" in factor_names
        assert "Termination For Convenience" in factor_names
        assert "Liability Cap Present" in factor_names

    def test_empty_ocr_produces_empty_nlp(self, client, uploaded_contract):
        """
        If OCR returns 0 chunks → NLP returns empty clauses/entities,
        pipeline still completes with base risk score only.
        """
        contract_id = uploaded_contract

        empty_ocr = OCROutput(
            contract_id=contract_id,
            chunks=[],
            total_pages=0,
            extraction_method="pdfplumber",
            processing_time_seconds=0.01,
        )

        empty_nlp = NLPOutput(
            contract_id=contract_id,
            clauses=[],
            entities=[],
            processing_time_seconds=0.0,
        )

        with patch("backend.services.pipeline.run_real_ocr", return_value=empty_ocr), \
             patch("backend.services.pipeline.run_real_nlp", return_value=empty_nlp):

            response = client.post(f"/api/analyze/{contract_id}")

        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "completed"
        assert data["clauses"] == []
        assert data["entities"] == []
        # With no clauses detected, only base risk (30)
        assert data["risk_score"] == 30
        assert data["risk_severity"] == "medium"
        assert len(data["risk_breakdown"]) == 1
        assert data["risk_breakdown"][0]["factor"] == "Base Contract Risk"


# ===========================================================================
# Test: Health & Root Endpoints (smoke tests)
# ===========================================================================
class TestSystemEndpoints:
    """Smoke tests for system endpoints."""

    def test_health_check(self, client):
        """GET /health returns ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_root_endpoint(self, client):
        """GET / returns API info with endpoint listing."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "upload" in data["endpoints"]
        assert "analyze" in data["endpoints"]
