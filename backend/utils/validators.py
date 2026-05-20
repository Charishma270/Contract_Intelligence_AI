"""
Request Validators
===================
Day 12: Reusable validation helpers for route handlers.
Keeps route code clean by extracting common validation patterns.
"""

import re
from typing import Optional

from backend.schemas.contract_schema import ContractStatus
from backend.services.tracking import get_contract
from backend.utils.exceptions import (
    ContractAlreadyFailedError,
    ContractNotAnalyzedError,
    ContractNotFoundError,
    EmptyQueryError,
    InvalidContractIdError,
)

# UUID v4 pattern (standard format)
UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def validate_contract_id(contract_id: str) -> None:
    """Validate that a contract_id is a properly-formatted UUID."""
    if not contract_id or not contract_id.strip():
        raise InvalidContractIdError(contract_id)
    if not UUID_PATTERN.match(contract_id.strip()):
        raise InvalidContractIdError(contract_id)


def validate_contract_exists(contract_id: str):
    """
    Validate contract_id format AND that the contract exists in the database.
    Returns the ContractMetadata if found.
    """
    validate_contract_id(contract_id)
    contract = get_contract(contract_id)
    if not contract:
        raise ContractNotFoundError(contract_id)
    return contract


def validate_contract_not_failed(contract_id: str):
    """
    Validate that a contract exists and hasn't previously failed.
    Returns the ContractMetadata if valid.
    """
    contract = validate_contract_exists(contract_id)
    if contract.status == ContractStatus.FAILED:
        raise ContractAlreadyFailedError(
            contract_id, contract.error_message or ""
        )
    return contract


def validate_contract_analyzed(contract_id: str):
    """
    Validate that a contract has been fully analyzed (status >= nlp_done).
    Returns the ContractMetadata if valid.
    """
    contract = validate_contract_exists(contract_id)
    analyzed_statuses = {
        ContractStatus.NLP_DONE,
        ContractStatus.RAG_INDEXED,
        ContractStatus.COMPLETED,
    }
    if contract.status not in analyzed_statuses:
        raise ContractNotAnalyzedError(contract_id)
    return contract


def validate_query(query: Optional[str]) -> str:
    """Validate and clean a chat query string. Returns the cleaned query."""
    if not query or not query.strip():
        raise EmptyQueryError()
    return query.strip()
