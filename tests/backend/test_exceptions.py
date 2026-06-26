"""
Day 26 — Unit Tests: Custom Exception Hierarchy
================================================
Verifies that every custom exception class in backend/utils/exceptions.py:
  - Can be instantiated with the expected arguments
  - Carries the correct status_code
  - Carries a human-readable message
  - Participates correctly in the ContractAIError hierarchy
"""

import pytest
from backend.utils.exceptions import (
    ContractAIError,
    ContractNotFoundError,
    ContractAlreadyFailedError,
    ContractNotAnalyzedError,
    FileValidationError,
    FileTooLargeError,
    UnsupportedFileTypeError,
    EmptyFileError,
    PipelineError,
    OCRProcessingError,
    NLPProcessingError,
    EmptyQueryError,
    InvalidContractIdError,
)


# ---------------------------------------------------------------------------
# Base exception
# ---------------------------------------------------------------------------

class TestContractAIError:

    def test_default_status_code(self):
        exc = ContractAIError("something broke")
        assert exc.status_code == 500
        assert exc.message == "something broke"

    def test_custom_status_code(self):
        exc = ContractAIError("bad request", status_code=400)
        assert exc.status_code == 400

    def test_is_exception(self):
        exc = ContractAIError("test")
        assert isinstance(exc, Exception)

    def test_str_representation(self):
        exc = ContractAIError("descriptive error")
        assert "descriptive error" in str(exc)


# ---------------------------------------------------------------------------
# Contract lookup errors
# ---------------------------------------------------------------------------

class TestContractNotFoundError:

    def test_status_code(self):
        exc = ContractNotFoundError("abc-123")
        assert exc.status_code == 404

    def test_message_contains_id(self):
        exc = ContractNotFoundError("my-contract-id")
        assert "my-contract-id" in exc.message

    def test_inherits_base(self):
        exc = ContractNotFoundError("id")
        assert isinstance(exc, ContractAIError)

    def test_contract_id_attribute(self):
        exc = ContractNotFoundError("abc-123")
        assert exc.contract_id == "abc-123"


class TestContractAlreadyFailedError:

    def test_status_code(self):
        exc = ContractAlreadyFailedError("cid")
        assert exc.status_code == 400

    def test_message_without_detail(self):
        exc = ContractAlreadyFailedError("cid")
        assert "cid" in exc.message
        assert "failed" in exc.message.lower()

    def test_message_with_detail(self):
        exc = ContractAlreadyFailedError("cid", "OCR timeout")
        assert "OCR timeout" in exc.message

    def test_inherits_base(self):
        exc = ContractAlreadyFailedError("cid")
        assert isinstance(exc, ContractAIError)


class TestContractNotAnalyzedError:

    def test_status_code(self):
        exc = ContractNotAnalyzedError("cid")
        assert exc.status_code == 400

    def test_message_contains_id(self):
        exc = ContractNotAnalyzedError("cid-42")
        assert "cid-42" in exc.message

    def test_message_mentions_analyze(self):
        exc = ContractNotAnalyzedError("cid")
        assert "analyze" in exc.message.lower()

    def test_inherits_base(self):
        exc = ContractNotAnalyzedError("cid")
        assert isinstance(exc, ContractAIError)


# ---------------------------------------------------------------------------
# File validation errors
# ---------------------------------------------------------------------------

class TestFileValidationError:

    def test_default_status(self):
        exc = FileValidationError("bad file")
        assert exc.status_code == 400

    def test_custom_status(self):
        exc = FileValidationError("bad file", status_code=422)
        assert exc.status_code == 422

    def test_inherits_base(self):
        exc = FileValidationError("bad file")
        assert isinstance(exc, ContractAIError)


class TestFileTooLargeError:

    def test_status_code(self):
        exc = FileTooLargeError(size_mb=25.3, max_mb=20)
        assert exc.status_code == 413

    def test_message_contains_sizes(self):
        exc = FileTooLargeError(size_mb=25.3, max_mb=20)
        assert "25.3" in exc.message
        assert "20" in exc.message

    def test_inherits_file_validation(self):
        exc = FileTooLargeError(size_mb=10.0, max_mb=5)
        assert isinstance(exc, FileValidationError)
        assert isinstance(exc, ContractAIError)


class TestUnsupportedFileTypeError:

    def test_status_code(self):
        exc = UnsupportedFileTypeError("Only PDF allowed")
        assert exc.status_code == 415

    def test_message_preserved(self):
        exc = UnsupportedFileTypeError("Only PDF allowed")
        assert "Only PDF allowed" in exc.message

    def test_inherits_file_validation(self):
        exc = UnsupportedFileTypeError("detail")
        assert isinstance(exc, FileValidationError)


class TestEmptyFileError:

    def test_status_code(self):
        exc = EmptyFileError()
        assert exc.status_code == 400

    def test_message_mentions_empty(self):
        exc = EmptyFileError()
        assert "empty" in exc.message.lower()

    def test_inherits_file_validation(self):
        exc = EmptyFileError()
        assert isinstance(exc, FileValidationError)


# ---------------------------------------------------------------------------
# Pipeline errors
# ---------------------------------------------------------------------------

class TestPipelineError:

    def test_status_code(self):
        exc = PipelineError(stage="ocr", contract_id="cid", detail="timeout")
        assert exc.status_code == 500

    def test_message_contains_stage(self):
        exc = PipelineError(stage="nlp", contract_id="cid", detail="model error")
        assert "nlp" in exc.message

    def test_message_contains_contract_id(self):
        exc = PipelineError(stage="ocr", contract_id="my-id", detail="fail")
        assert "my-id" in exc.message

    def test_message_contains_detail(self):
        exc = PipelineError(stage="ocr", contract_id="cid", detail="disk full")
        assert "disk full" in exc.message

    def test_inherits_base(self):
        exc = PipelineError(stage="s", contract_id="c", detail="d")
        assert isinstance(exc, ContractAIError)


class TestOCRProcessingError:

    def test_stage_is_ocr(self):
        exc = OCRProcessingError(contract_id="cid", detail="pdf corrupt")
        assert exc.stage == "ocr"

    def test_inherits_pipeline(self):
        exc = OCRProcessingError(contract_id="cid", detail="fail")
        assert isinstance(exc, PipelineError)
        assert isinstance(exc, ContractAIError)

    def test_status_code(self):
        exc = OCRProcessingError(contract_id="cid", detail="fail")
        assert exc.status_code == 500


class TestNLPProcessingError:

    def test_stage_is_nlp(self):
        exc = NLPProcessingError(contract_id="cid", detail="model load failed")
        assert exc.stage == "nlp"

    def test_inherits_pipeline(self):
        exc = NLPProcessingError(contract_id="cid", detail="fail")
        assert isinstance(exc, PipelineError)

    def test_status_code(self):
        exc = NLPProcessingError(contract_id="cid", detail="fail")
        assert exc.status_code == 500


# ---------------------------------------------------------------------------
# Query and ID errors
# ---------------------------------------------------------------------------

class TestEmptyQueryError:

    def test_status_code(self):
        exc = EmptyQueryError()
        assert exc.status_code == 400

    def test_message_mentions_empty(self):
        exc = EmptyQueryError()
        assert "empty" in exc.message.lower()

    def test_inherits_base(self):
        exc = EmptyQueryError()
        assert isinstance(exc, ContractAIError)


class TestInvalidContractIdError:

    def test_status_code(self):
        exc = InvalidContractIdError("not-a-uuid")
        assert exc.status_code == 400

    def test_message_contains_id(self):
        exc = InvalidContractIdError("bad-id")
        assert "bad-id" in exc.message

    def test_inherits_base(self):
        exc = InvalidContractIdError("x")
        assert isinstance(exc, ContractAIError)

    def test_contract_id_attribute(self):
        exc = InvalidContractIdError("bad-id")
        assert exc.contract_id == "bad-id"
