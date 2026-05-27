"""
Tests for Real NLP Service
============================
Day 15: Unit tests for the real NLP integration.

Tests use mocked models to avoid requiring 438MB model weights
and ML dependencies (torch, transformers, spacy) during CI runs.
Tests validate:
  - Entity extraction logic and deduplication
  - Clause classification aggregation (best-per-type)
  - Empty input handling
  - Error propagation as NLPProcessingError
"""

import pytest
from unittest.mock import MagicMock, patch

from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction, NLPOutput
from backend.schemas.ocr_schema import OCRChunk, OCROutput
from backend.utils.exceptions import NLPProcessingError


# ---------------------------------------------------------------------------
# Helpers: Build mock OCR output
# ---------------------------------------------------------------------------
def _make_ocr_output(texts: list, contract_id: str = "test-001") -> OCROutput:
    """Build a minimal OCROutput with the given texts as chunks."""
    chunks = []
    for i, text in enumerate(texts):
        chunks.append(
            OCRChunk(
                contract_id=contract_id,
                chunk_id=f"chunk-{i}",
                page=i + 1,
                text=text,
            )
        )
    return OCROutput(
        contract_id=contract_id,
        chunks=chunks,
        total_pages=len(texts),
        extraction_method="pdfplumber",
    )


# ---------------------------------------------------------------------------
# Test: Empty OCR input returns empty NLPOutput
# ---------------------------------------------------------------------------
class TestRunRealNlpEmptyInput:
    """Verify graceful handling of empty/no OCR output."""

    def test_no_chunks(self):
        """NLP with zero chunks should return empty clauses and entities."""
        from backend.services.real_nlp import run_real_nlp

        ocr = OCROutput(
            contract_id="empty-001",
            chunks=[],
            total_pages=0,
        )
        result = run_real_nlp("empty-001", ocr)

        assert isinstance(result, NLPOutput)
        assert result.contract_id == "empty-001"
        assert result.clauses == []
        assert result.entities == []
        assert result.processing_time_seconds == 0.0

    def test_none_ocr(self):
        """NLP with None OCR output should return empty NLPOutput."""
        from backend.services.real_nlp import run_real_nlp

        result = run_real_nlp("none-001", None)
        assert result.clauses == []
        assert result.entities == []


# ---------------------------------------------------------------------------
# Test: Entity extraction with spaCy
# ---------------------------------------------------------------------------
class TestExtractEntities:
    """Test the NER extraction and deduplication logic."""

    def test_entities_mapped_and_deduplicated(self):
        """Entities should be mapped from spaCy labels and deduplicated."""
        import backend.services.real_nlp as nlp_module

        # Create a mock spaCy doc with entities
        mock_ent1 = MagicMock()
        mock_ent1.label_ = "ORG"
        mock_ent1.text = "Acme Corporation"
        mock_ent1.start_char = 10

        mock_ent2 = MagicMock()
        mock_ent2.label_ = "ORG"
        mock_ent2.text = "Acme Corporation"  # Duplicate
        mock_ent2.start_char = 200

        mock_ent3 = MagicMock()
        mock_ent3.label_ = "GPE"
        mock_ent3.text = "Delaware"
        mock_ent3.start_char = 50

        mock_ent4 = MagicMock()
        mock_ent4.label_ = "DATE"
        mock_ent4.text = "January 15, 2025"
        mock_ent4.start_char = 75

        mock_ent5 = MagicMock()
        mock_ent5.label_ = "CARDINAL"  # Should be filtered out (mapped to None)
        mock_ent5.text = "42"
        mock_ent5.start_char = 100

        mock_doc = MagicMock()
        mock_doc.ents = [mock_ent1, mock_ent2, mock_ent3, mock_ent4, mock_ent5]

        mock_nlp = MagicMock()
        mock_nlp.max_length = 1000000
        mock_nlp.return_value = mock_doc

        # Inject mock spaCy model
        original = nlp_module._spacy_nlp
        nlp_module._spacy_nlp = mock_nlp

        try:
            entities = nlp_module._extract_entities("test-001", "Some legal contract text")

            # Should have 3 unique entities (ORG dedup'd, CARDINAL filtered)
            assert len(entities) == 3

            entity_types = {e.entity_type for e in entities}
            assert "ORGANIZATION" in entity_types
            assert "JURISDICTION" in entity_types
            assert "DATE" in entity_types

            # Verify deduplication — only one "Acme Corporation"
            org_entities = [e for e in entities if e.entity_type == "ORGANIZATION"]
            assert len(org_entities) == 1
            assert org_entities[0].value == "Acme Corporation"

        finally:
            nlp_module._spacy_nlp = original

    def test_empty_text_returns_no_entities(self):
        """Empty text should return empty entity list without calling spaCy."""
        import backend.services.real_nlp as nlp_module

        # Even without a real spaCy model loaded, empty text should return []
        # because the function checks before calling the model
        original = nlp_module._spacy_nlp
        mock_nlp = MagicMock()
        mock_nlp.max_length = 1000000
        nlp_module._spacy_nlp = mock_nlp

        try:
            entities = nlp_module._extract_entities("test-002", "")
            assert entities == []

            entities = nlp_module._extract_entities("test-003", "   ")
            assert entities == []

            # spaCy model should NOT have been called
            mock_nlp.assert_not_called()
        finally:
            nlp_module._spacy_nlp = original


# ---------------------------------------------------------------------------
# Test: Clause classification aggregation
# ---------------------------------------------------------------------------
class TestClassifyChunks:
    """Test multi-label clause classification and aggregation."""

    def test_best_confidence_per_clause_type(self):
        """When the same clause appears in multiple chunks, keep highest confidence."""
        import backend.services.real_nlp as nlp_module

        call_count = [0]
        side_effects = [
            [{"label": "Termination For Convenience", "confidence": 0.80}],
            [
                {"label": "Termination For Convenience", "confidence": 0.95},
                {"label": "Renewal Term", "confidence": 0.70},
            ],
        ]

        original_fn = nlp_module._classify_single_chunk

        def mock_classify(text):
            result = side_effects[call_count[0]]
            call_count[0] += 1
            return result

        nlp_module._classify_single_chunk = mock_classify

        try:
            ocr = _make_ocr_output([
                "Either party may terminate this agreement...",
                "This agreement shall auto-renew and may be terminated...",
            ])

            clauses, chunks_processed = nlp_module._classify_chunks("test-001", ocr.chunks)

            assert chunks_processed == 2
            assert len(clauses) == 2  # Two unique clause types

            # Termination should have 0.95 (from chunk 2)
            term_clause = next(c for c in clauses if c.clause_type == "Termination For Convenience")
            assert term_clause.confidence == 0.95
            assert term_clause.page == 2  # From chunk 2

            # Renewal should have 0.70
            renewal_clause = next(c for c in clauses if c.clause_type == "Renewal Term")
            assert renewal_clause.confidence == 0.70

        finally:
            nlp_module._classify_single_chunk = original_fn

    def test_empty_chunks_returns_empty(self):
        """Empty text chunks should be skipped."""
        import backend.services.real_nlp as nlp_module

        call_count = [0]

        def mock_classify(text):
            call_count[0] += 1
            return []

        original_fn = nlp_module._classify_single_chunk
        nlp_module._classify_single_chunk = mock_classify

        try:
            ocr = _make_ocr_output(["", "   ", ""])
            clauses, _ = nlp_module._classify_chunks("test-002", ocr.chunks)

            assert clauses == []
            assert call_count[0] == 0  # Should not have been called
        finally:
            nlp_module._classify_single_chunk = original_fn

    def test_classification_error_skips_chunk(self):
        """If classification fails for one chunk, others should still process."""
        import backend.services.real_nlp as nlp_module

        call_count = [0]

        def mock_classify(text):
            idx = call_count[0]
            call_count[0] += 1
            if idx == 0:
                raise RuntimeError("CUDA OOM")
            return [{"label": "Cap On Liability", "confidence": 0.85}]

        original_fn = nlp_module._classify_single_chunk
        nlp_module._classify_single_chunk = mock_classify

        try:
            ocr = _make_ocr_output(["Chunk 1 text", "Chunk 2 text"])
            clauses, chunks_processed = nlp_module._classify_chunks("test-003", ocr.chunks)

            assert len(clauses) == 1
            assert clauses[0].clause_type == "Cap On Liability"
        finally:
            nlp_module._classify_single_chunk = original_fn


# ---------------------------------------------------------------------------
# Test: Full run_real_nlp integration (mocked models)
# ---------------------------------------------------------------------------
class TestRunRealNlpIntegration:
    """Integration test for the full NLP pipeline with mocked sub-functions."""

    def test_full_pipeline_returns_nlp_output(self):
        """Full pipeline should combine clauses and entities into NLPOutput."""
        import backend.services.real_nlp as nlp_module

        mock_clauses = [
            ClausePrediction(
                clause_type="Termination For Convenience",
                answer_text="Either party may terminate...",
                confidence=0.92,
                page=1,
            )
        ]
        mock_entities = [
            EntityPrediction(entity_type="ORGANIZATION", value="Acme Corp", position=10),
            EntityPrediction(entity_type="DATE", value="2025-01-15", position=50),
        ]

        orig_classify = nlp_module._classify_chunks
        orig_extract = nlp_module._extract_entities

        nlp_module._classify_chunks = lambda cid, chunks: (mock_clauses, 2)
        nlp_module._extract_entities = lambda cid, text: mock_entities

        try:
            ocr = _make_ocr_output(["Some text", "More text"])
            result = nlp_module.run_real_nlp("test-full-001", ocr)

            assert isinstance(result, NLPOutput)
            assert result.contract_id == "test-full-001"
            assert len(result.clauses) == 1
            assert len(result.entities) == 2
            assert result.processing_time_seconds is not None
            assert result.processing_time_seconds >= 0
        finally:
            nlp_module._classify_chunks = orig_classify
            nlp_module._extract_entities = orig_extract

    def test_pipeline_raises_nlp_error_on_failure(self):
        """Unexpected errors should be wrapped in NLPProcessingError."""
        import backend.services.real_nlp as nlp_module

        orig_classify = nlp_module._classify_chunks
        nlp_module._classify_chunks = MagicMock(side_effect=RuntimeError("Model corrupted"))

        try:
            ocr = _make_ocr_output(["Some text"])

            with pytest.raises(NLPProcessingError) as exc_info:
                nlp_module.run_real_nlp("test-fail-001", ocr)

            assert "test-fail-001" in str(exc_info.value)
            assert exc_info.value.stage == "nlp"
        finally:
            nlp_module._classify_chunks = orig_classify
