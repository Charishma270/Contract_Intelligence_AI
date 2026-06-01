"""
Test Vector DB Endpoints
=========================
Day 18: Unit tests for /api/vectordb/* endpoints.
Mocks the FAISS index and metadata store globals.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------
# Mock heavy dependencies before importing the app
# ---------------------------------------------------------

# FAISS mock
mock_faiss_index = MagicMock()
mock_faiss_index.ntotal = 5
mock_faiss_index.d = 384
mock_faiss_index.is_trained = True
mock_faiss_index.__class__.__name__ = "IndexFlatIP"

MOCK_METADATA = [
    {
        "text": (
            "The Seller shall not compete with the Buyer "
            "in any market for a period of two years "
            "following the termination of this agreement."
        ),
        "label_name": "Non-Compete",
        "target": 1,
    },
    {
        "text": (
            "Either party may terminate this agreement "
            "for convenience upon thirty days written notice."
        ),
        "label_name": "Termination For Convenience",
        "target": 1,
    },
    {
        "text": (
            "The total liability of the Provider under "
            "this agreement shall not exceed the fees "
            "paid by the Customer in the preceding "
            "twelve months."
        ),
        "label_name": "Cap On Liability",
        "target": 1,
    },
    {
        "text": (
            "This agreement shall automatically renew "
            "for successive one-year periods unless "
            "either party provides written notice of "
            "non-renewal at least sixty days prior."
        ),
        "label_name": "Renewal Term",
        "target": 1,
    },
    {
        "text": (
            "All intellectual property developed during "
            "the term of this agreement shall be owned "
            "exclusively by the Client."
        ),
        "label_name": "Ip Ownership Assignment",
        "target": 1,
    },
]

# Build mock faiss_store module with index + metadata_store
_mock_faiss_store_module = MagicMock()
_mock_faiss_store_module.index = mock_faiss_index
_mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
_mock_faiss_store_module.add_embedding = MagicMock()
_mock_faiss_store_module.search_embedding = MagicMock(return_value=[])
_mock_faiss_store_module.save_index = MagicMock()
_mock_faiss_store_module.load_index = MagicMock()

# Create mock modules for all heavy dependencies
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
    "numpy": MagicMock(),
    "sklearn": MagicMock(),
    "sklearn.feature_extraction": MagicMock(),
    "sklearn.feature_extraction.text": MagicMock(),
    "sklearn.svm": MagicMock(),
    "rank_bm25": MagicMock(),
    # NOTE: Do NOT mock "celery" or "celery.result" here.
    # Mocking them at module level replaces the real celery package in
    # sys.modules, which breaks celery submodule imports (e.g. celery.canvas)
    # for every test collected after this file in a full pytest run.
    # Risk engine hierarchy
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
    "risk_engine.scoring.risk_calculator": MagicMock(
        calculate_risk=MagicMock(return_value="Low"),
    ),
    "risk_engine.scoring.risk_rules": MagicMock(),
    "risk_engine.rules": MagicMock(),
    "risk_engine.rules.risk_rules": MagicMock(),
    # RAG sub-modules
    "rag.retrieval.embedder": MagicMock(),
    "rag.retrieval.bm25_retriever": MagicMock(bm25=MagicMock()),
    "rag.vector_db.faiss_store": _mock_faiss_store_module,
    "rag.pipeline.pipeline": MagicMock(
        run_pipeline=MagicMock(return_value={
            "summary": {
                "overall_risk": "Low",
                "top_detected_labels": [],
                "high_confidence_clauses": 0,
            },
            "results": [],
        }),
    ),
    # OCR pipeline
    "ocr.ocr_pipeline": MagicMock(),
}

# Inject mocks into sys.modules
for mod_name, mock_obj in _mock_modules.items():
    sys.modules[mod_name] = mock_obj

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ================================================================
# Tests
# ================================================================

class TestVectorDBStatus:
    """Tests for GET /api/vectordb/status."""

    def test_status_returns_stats(self):
        """Status endpoint returns correct index statistics."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get("/api/vectordb/status")

        assert response.status_code == 200

        data = response.json()
        assert data["total_vectors"] == 5
        assert data["dimension"] == 384
        assert data["is_trained"] is True
        assert data["metadata_count"] == 5
        assert "index_type" in data

    def test_status_empty_index_returns_503(self):
        """Status returns 503 when the index has 0 vectors."""

        mock_faiss_index.ntotal = 0
        _mock_faiss_store_module.metadata_store = []

        response = client.get("/api/vectordb/status")

        assert response.status_code == 503

        data = response.json()
        assert "not loaded" in data["detail"].lower()

        # Restore
        mock_faiss_index.ntotal = 5
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()


class TestListChunks:
    """Tests for GET /api/vectordb/chunks."""

    def test_list_chunks_default_pagination(self):
        """Default pagination returns all 5 chunks."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get("/api/vectordb/chunks")

        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 5
        assert data["skip"] == 0
        assert data["limit"] == 20
        assert len(data["chunks"]) == 5

    def test_list_chunks_with_pagination(self):
        """Pagination returns correct slice."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get(
            "/api/vectordb/chunks?skip=2&limit=2"
        )

        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 5
        assert data["skip"] == 2
        assert data["limit"] == 2
        assert len(data["chunks"]) == 2

        # Third chunk (index=2) is Cap On Liability
        assert (
            data["chunks"][0]["label_name"]
            == "Cap On Liability"
        )

    def test_list_chunks_has_required_fields(self):
        """Each chunk has all required fields."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get(
            "/api/vectordb/chunks?limit=1"
        )

        assert response.status_code == 200

        chunk = response.json()["chunks"][0]

        assert "index" in chunk
        assert "text" in chunk
        assert "text_preview" in chunk
        assert "label_name" in chunk
        assert "target" in chunk
        assert "word_count" in chunk


class TestGetSingleChunk:
    """Tests for GET /api/vectordb/chunks/{index}."""

    def test_get_chunk_by_index(self):
        """Returns the correct chunk at a given index."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get("/api/vectordb/chunks/1")

        assert response.status_code == 200

        data = response.json()
        assert data["index"] == 1
        assert (
            data["label_name"]
            == "Termination For Convenience"
        )

    def test_get_chunk_out_of_range(self):
        """Returns 404 for an index beyond the store."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get("/api/vectordb/chunks/999")

        assert response.status_code == 404

        data = response.json()
        assert "out of range" in data["detail"].lower()

    def test_get_chunk_negative_index(self):
        """Returns 404 for a negative index."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.get("/api/vectordb/chunks/-1")

        assert response.status_code == 404


class TestSearchChunks:
    """Tests for POST /api/vectordb/chunks/search."""

    def test_search_by_label(self):
        """Finds chunks matching a label name."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.post(
            "/api/vectordb/chunks/search",
            json={"label": "Non-Compete"},
        )

        assert response.status_code == 200

        data = response.json()
        assert data["match_count"] == 1
        assert (
            data["chunks"][0]["label_name"]
            == "Non-Compete"
        )

    def test_search_by_label_case_insensitive(self):
        """Label search is case-insensitive."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.post(
            "/api/vectordb/chunks/search",
            json={"label": "non-compete"},
        )

        assert response.status_code == 200
        assert response.json()["match_count"] == 1

    def test_search_by_keyword(self):
        """Finds chunks containing a text keyword."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.post(
            "/api/vectordb/chunks/search",
            json={"keyword": "terminate"},
        )

        assert response.status_code == 200

        data = response.json()
        # "terminate" appears in Non-Compete and
        # Termination For Convenience texts
        assert data["match_count"] >= 1

    def test_search_no_criteria_returns_400(self):
        """Returns 400 when no search criteria provided."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.post(
            "/api/vectordb/chunks/search",
            json={},
        )

        assert response.status_code == 400

    def test_search_combined_label_and_keyword(self):
        """AND logic: both label and keyword must match."""

        _mock_faiss_store_module.index = mock_faiss_index
        _mock_faiss_store_module.metadata_store = MOCK_METADATA.copy()
        mock_faiss_index.ntotal = 5

        response = client.post(
            "/api/vectordb/chunks/search",
            json={
                "label": "Renewal",
                "keyword": "renew",
            },
        )

        assert response.status_code == 200

        data = response.json()
        assert data["match_count"] == 1
        assert (
            data["chunks"][0]["label_name"]
            == "Renewal Term"
        )
