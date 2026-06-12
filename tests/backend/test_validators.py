"""
Day 26 — Unit Tests: Request Validators
========================================
Verifies all functions in backend/utils/validators.py in isolation,
using a real (temp) SQLite database via conftest.py fixtures.
"""

import uuid
import pytest

from backend.utils.exceptions import (
    ContractAlreadyFailedError,
    ContractNotAnalyzedError,
    ContractNotFoundError,
    EmptyQueryError,
    InvalidContractIdError,
)
from backend.utils.validators import (
    validate_contract_id,
    validate_contract_exists,
    validate_contract_not_failed,
    validate_contract_analyzed,
    validate_query,
)
from backend.schemas.contract_schema import ContractStatus
from backend.services.tracking import update_contract_status


# ---------------------------------------------------------------------------
# validate_contract_id
# ---------------------------------------------------------------------------

class TestValidateContractId:

    def test_valid_uuid_v4(self):
        uid = str(uuid.uuid4())
        # Should not raise
        validate_contract_id(uid)

    def test_valid_uuid_uppercase(self):
        uid = str(uuid.uuid4()).upper()
        validate_contract_id(uid)

    def test_empty_string_raises(self):
        with pytest.raises(InvalidContractIdError):
            validate_contract_id("")

    def test_whitespace_string_raises(self):
        with pytest.raises(InvalidContractIdError):
            validate_contract_id("   ")

    def test_random_string_raises(self):
        with pytest.raises(InvalidContractIdError):
            validate_contract_id("not-a-uuid")

    def test_short_uuid_raises(self):
        with pytest.raises(InvalidContractIdError):
            validate_contract_id("1234-5678")

    def test_integer_string_raises(self):
        with pytest.raises(InvalidContractIdError):
            validate_contract_id("12345")

    def test_none_like_raises(self):
        with pytest.raises((InvalidContractIdError, AttributeError)):
            # None is technically a wrong type; test that it doesn't silently pass
            validate_contract_id("none")


# ---------------------------------------------------------------------------
# validate_contract_exists
# ---------------------------------------------------------------------------

class TestValidateContractExists:

    def test_existing_contract_returns_metadata(self, sample_contract_id):
        result = validate_contract_exists(sample_contract_id)
        assert result.contract_id == sample_contract_id

    def test_nonexistent_contract_raises_not_found(self):
        nonexistent = str(uuid.uuid4())
        with pytest.raises(ContractNotFoundError):
            validate_contract_exists(nonexistent)

    def test_invalid_uuid_raises_invalid_id(self):
        with pytest.raises(InvalidContractIdError):
            validate_contract_exists("bad-id")


# ---------------------------------------------------------------------------
# validate_contract_not_failed
# ---------------------------------------------------------------------------

class TestValidateContractNotFailed:

    def test_uploaded_contract_passes(self, sample_contract_id):
        result = validate_contract_not_failed(sample_contract_id)
        assert result is not None
        assert result.contract_id == sample_contract_id

    def test_failed_contract_raises(self, sample_contract_id):
        update_contract_status(
            sample_contract_id,
            ContractStatus.FAILED,
            "OCR timed out",
        )
        with pytest.raises(ContractAlreadyFailedError):
            validate_contract_not_failed(sample_contract_id)

    def test_nonexistent_raises_not_found(self):
        with pytest.raises(ContractNotFoundError):
            validate_contract_not_failed(str(uuid.uuid4()))


# ---------------------------------------------------------------------------
# validate_contract_analyzed
# ---------------------------------------------------------------------------

class TestValidateContractAnalyzed:

    def test_uploaded_status_raises_not_analyzed(self, sample_contract_id):
        with pytest.raises(ContractNotAnalyzedError):
            validate_contract_analyzed(sample_contract_id)

    def test_nlp_done_status_passes(self, sample_contract_id):
        update_contract_status(sample_contract_id, ContractStatus.NLP_DONE)
        result = validate_contract_analyzed(sample_contract_id)
        assert result.contract_id == sample_contract_id

    def test_completed_status_passes(self, sample_contract_id):
        update_contract_status(sample_contract_id, ContractStatus.COMPLETED)
        result = validate_contract_analyzed(sample_contract_id)
        assert result is not None

    def test_rag_indexed_status_passes(self, sample_contract_id):
        update_contract_status(sample_contract_id, ContractStatus.RAG_INDEXED)
        result = validate_contract_analyzed(sample_contract_id)
        assert result is not None

    def test_ocr_done_status_raises(self, sample_contract_id):
        update_contract_status(sample_contract_id, ContractStatus.OCR_DONE)
        with pytest.raises(ContractNotAnalyzedError):
            validate_contract_analyzed(sample_contract_id)

    def test_nonexistent_raises_not_found(self):
        with pytest.raises(ContractNotFoundError):
            validate_contract_analyzed(str(uuid.uuid4()))


# ---------------------------------------------------------------------------
# validate_query
# ---------------------------------------------------------------------------

class TestValidateQuery:

    def test_normal_query_returned(self):
        result = validate_query("What are the termination clauses?")
        assert result == "What are the termination clauses?"

    def test_leading_trailing_whitespace_stripped(self):
        result = validate_query("  hello world  ")
        assert result == "hello world"

    def test_empty_string_raises(self):
        with pytest.raises(EmptyQueryError):
            validate_query("")

    def test_whitespace_only_raises(self):
        with pytest.raises(EmptyQueryError):
            validate_query("   ")

    def test_none_raises(self):
        with pytest.raises(EmptyQueryError):
            validate_query(None)

    def test_single_word_query(self):
        result = validate_query("termination")
        assert result == "termination"

    def test_long_query_preserved(self):
        long_query = "a " * 500
        result = validate_query(long_query)
        assert len(result) > 0
