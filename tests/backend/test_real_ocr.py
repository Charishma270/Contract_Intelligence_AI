"""
Tests for Real OCR Service
===========================
Day 14: Comprehensive tests for backend/services/real_ocr.py

Tests cover:
  - pdfplumber fast-path with text-based PDFs
  - Tesseract fallback for scanned/image-based PDFs
  - Error handling for missing files
  - OCROutput schema validation
  - Chunk metadata population
  - OCR config environment variable overrides
"""

import os
import uuid
from unittest.mock import MagicMock, patch

import pytest

from backend.schemas.ocr_schema import OCRChunk, OCROutput
from backend.utils.exceptions import OCRProcessingError

# Import the module so @patch can resolve attributes
import backend.services.real_ocr as real_ocr_mod
from backend.services.real_ocr import run_real_ocr


# Patch targets — using the module where the names live
_PATCH_PLUMBER = "backend.services.real_ocr._extract_with_pdfplumber"
_PATCH_TESS = "backend.services.real_ocr._extract_with_tesseract"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def contract_id():
    """Generate a unique contract ID for each test."""
    return str(uuid.uuid4())


@pytest.fixture
def fake_pdf_path(tmp_path):
    """Create a temporary fake PDF file path."""
    pdf = tmp_path / "test_contract.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake content")
    return str(pdf)


@pytest.fixture
def nonexistent_path():
    """Return a path that definitely doesn't exist."""
    return r"C:\nonexistent\fake_contract.pdf"


# ---------------------------------------------------------------------------
# Test: pdfplumber fast-path
# ---------------------------------------------------------------------------
class TestPdfplumberFastPath:
    """Tests for the pdfplumber extraction path."""

    def test_uses_pdfplumber_when_text_is_sufficient(
        self, contract_id, fake_pdf_path
    ):
        """When pdfplumber returns enough text, Tesseract is NOT called."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS) as mock_tess:
            mock_plumber.return_value = [
                (1, "This is a long enough contract text that exceeds the minimum threshold. " * 5),
                (2, "Second page with plenty of legal language and terms and conditions. " * 5),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

            # Tesseract should NOT have been called
            mock_tess.assert_not_called()

        assert isinstance(result, OCROutput)
        assert result.contract_id == contract_id
        assert result.total_pages == 2
        assert result.extraction_method == "pdfplumber"
        assert len(result.chunks) > 0

    def test_pdfplumber_output_has_correct_chunk_fields(
        self, contract_id, fake_pdf_path
    ):
        """Each chunk should have source_file and extraction_method populated."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS):
            mock_plumber.return_value = [
                (1, "A sufficiently long text extracted by pdfplumber for testing purposes. " * 5),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

        for chunk in result.chunks:
            assert chunk.source_file == fake_pdf_path
            assert chunk.extraction_method == "pdfplumber"
            assert chunk.contract_id == contract_id
            assert chunk.page == 1
            assert chunk.chunk_id  # UUID string, non-empty
            assert chunk.text.strip()  # Non-empty text


# ---------------------------------------------------------------------------
# Test: Tesseract fallback
# ---------------------------------------------------------------------------
class TestTesseractFallback:
    """Tests for the Tesseract OCR fallback path."""

    def test_falls_back_to_tesseract_for_sparse_pages(
        self, contract_id, fake_pdf_path
    ):
        """When pdfplumber returns too little text, Tesseract is called."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS) as mock_tess:
            # pdfplumber returns minimal text (below threshold)
            mock_plumber.return_value = [
                (1, "ok"),  # Too short — will trigger fallback
            ]
            # Tesseract returns proper text
            mock_tess.return_value = [
                (1, "This is a scanned contract with OCR extracted text. " * 5),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

            mock_tess.assert_called_once()

        assert result.total_pages == 1
        assert result.extraction_method == "tesseract"
        assert len(result.chunks) > 0

        for chunk in result.chunks:
            assert chunk.extraction_method == "tesseract"

    def test_full_tesseract_when_pdfplumber_fails_entirely(
        self, contract_id, fake_pdf_path
    ):
        """When pdfplumber returns empty list, full Tesseract is used."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS) as mock_tess:
            mock_plumber.return_value = []  # pdfplumber failed
            mock_tess.return_value = [
                (1, "OCR text from scanned page one of the contract document. " * 3),
                (2, "OCR text from scanned page two with additional clauses. " * 3),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

            mock_tess.assert_called_once()

        assert result.total_pages == 2
        assert result.extraction_method == "tesseract"

    def test_mixed_pages_use_both_methods(
        self, contract_id, fake_pdf_path
    ):
        """Some pages use pdfplumber, others fall back to Tesseract."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS) as mock_tess:
            mock_plumber.return_value = [
                (1, "Digital text page with lots of contract content. " * 5),  # Sufficient
                (2, "x"),  # Too short — fallback
                (3, "Another digital page with enough content for extraction. " * 5),  # Sufficient
            ]
            mock_tess.return_value = [
                (1, "tesseract page 1"),
                (2, "Scanned text from page two with enough content for chunking. " * 3),
                (3, "tesseract page 3"),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

        assert result.total_pages == 3
        # primary_method should be pdfplumber since 2 out of 3 pages used it
        assert result.extraction_method == "pdfplumber"

        methods = {chunk.extraction_method for chunk in result.chunks}
        assert "pdfplumber" in methods
        assert "tesseract" in methods


# ---------------------------------------------------------------------------
# Test: Error handling
# ---------------------------------------------------------------------------
class TestOCRErrorHandling:
    """Tests for OCR error scenarios."""

    def test_nonexistent_file_raises_ocr_error(self, contract_id, nonexistent_path):
        """Missing PDF file raises OCRProcessingError."""
        with pytest.raises(OCRProcessingError) as exc_info:
            run_real_ocr(contract_id, nonexistent_path)

        assert contract_id in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    def test_both_methods_fail_raises_ocr_error(
        self, contract_id, fake_pdf_path
    ):
        """When both extraction methods fail, OCRProcessingError is raised."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS) as mock_tess:
            mock_plumber.return_value = []
            mock_tess.side_effect = RuntimeError("Tesseract binary not found")

            with pytest.raises(OCRProcessingError):
                run_real_ocr(contract_id, fake_pdf_path)

    def test_ocr_error_inherits_from_pipeline_error(self):
        """OCRProcessingError should be a PipelineError."""
        from backend.utils.exceptions import PipelineError

        err = OCRProcessingError(contract_id="test-123", detail="test failure")
        assert isinstance(err, PipelineError)
        assert err.stage == "ocr"
        assert err.contract_id == "test-123"
        assert err.status_code == 500


# ---------------------------------------------------------------------------
# Test: Output schema validation
# ---------------------------------------------------------------------------
class TestOCROutputSchema:
    """Tests that OCROutput conforms to the Pydantic schema."""

    def test_output_is_valid_ocr_output(
        self, contract_id, fake_pdf_path
    ):
        """Returned object is a valid OCROutput Pydantic model."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS):
            mock_plumber.return_value = [
                (1, "Contract text for schema validation testing purposes. " * 5),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

        assert isinstance(result, OCROutput)
        assert isinstance(result.chunks, list)
        assert all(isinstance(c, OCRChunk) for c in result.chunks)
        assert result.total_pages >= 1
        assert result.processing_time_seconds is not None
        assert result.processing_time_seconds >= 0

    def test_output_serializes_to_dict(
        self, contract_id, fake_pdf_path
    ):
        """OCROutput should serialize cleanly to dict (for JSON responses)."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS):
            mock_plumber.return_value = [
                (1, "Text for serialization test with enough content to pass threshold. " * 3),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

        data = result.model_dump()
        assert "contract_id" in data
        assert "chunks" in data
        assert "total_pages" in data
        assert "extraction_method" in data
        assert "processing_time_seconds" in data


# ---------------------------------------------------------------------------
# Test: OCR config env var overrides
# ---------------------------------------------------------------------------
class TestOCRConfigOverrides:
    """Tests that OCR config values can be overridden via env vars."""

    def test_min_text_length_default(self):
        """Default MIN_TEXT_LENGTH should be 50."""
        import importlib
        import backend.services.ocr_config as cfg
        importlib.reload(cfg)
        assert cfg.MIN_TEXT_LENGTH == 50

    def test_chunk_size_default(self):
        """Default CHUNK_SIZE should be 200."""
        import importlib
        import backend.services.ocr_config as cfg
        importlib.reload(cfg)
        assert cfg.CHUNK_SIZE == 200

    def test_env_var_override_min_text_length(self, monkeypatch):
        """OCR_MIN_TEXT_LENGTH env var should override the default."""
        monkeypatch.setenv("OCR_MIN_TEXT_LENGTH", "100")

        import importlib
        import backend.services.ocr_config as cfg
        importlib.reload(cfg)

        assert cfg.MIN_TEXT_LENGTH == 100

    def test_env_var_override_chunk_size(self, monkeypatch):
        """OCR_CHUNK_SIZE env var should override the default."""
        monkeypatch.setenv("OCR_CHUNK_SIZE", "500")

        import importlib
        import backend.services.ocr_config as cfg
        importlib.reload(cfg)

        assert cfg.CHUNK_SIZE == 500


# ---------------------------------------------------------------------------
# Test: Empty PDF handling
# ---------------------------------------------------------------------------
class TestEmptyPDFHandling:
    """Tests for edge cases with empty or minimal PDFs."""

    def test_empty_pages_produce_no_chunks(
        self, contract_id, fake_pdf_path
    ):
        """Pages with empty text should not produce any chunks."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS) as mock_tess:
            mock_plumber.return_value = [
                (1, ""),
                (2, ""),
            ]
            mock_tess.return_value = [
                (1, ""),
                (2, ""),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

        assert result.total_pages == 2
        assert len(result.chunks) == 0

    def test_single_page_pdf(self, contract_id, fake_pdf_path):
        """Single page PDF should work correctly."""
        with patch(_PATCH_PLUMBER) as mock_plumber, \
             patch(_PATCH_TESS):
            mock_plumber.return_value = [
                (1, "Single page contract with all terms and conditions. " * 5),
            ]

            result = run_real_ocr(contract_id, fake_pdf_path)

        assert result.total_pages == 1
        assert len(result.chunks) >= 1
        assert all(c.page == 1 for c in result.chunks)
