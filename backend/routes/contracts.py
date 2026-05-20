"""
Contracts Route — /contracts endpoints
=======================================
Day 5: Contract listing and status retrieval.
Day 12: Enhanced error handling using centralized validators.
Day 13: Added structured logging.
"""

import logging
from typing import List

from fastapi import APIRouter, Query

from backend.schemas.contract_schema import ContractMetadata
from backend.services.tracking import list_contracts
from backend.utils.validators import validate_contract_exists

logger = logging.getLogger("contract_ai.contracts")

router = APIRouter()


@router.get("/contracts/{contract_id}", response_model=ContractMetadata)
async def get_contract_status(contract_id: str):
    """
    Get the current status and metadata of a specific contract.

    Raises:
      - 400: Invalid contract_id format
      - 404: Contract not found
    """
    contract = validate_contract_exists(contract_id)
    logger.info(f"Contract status lookup: id={contract_id}, status={contract.status}")
    return contract


@router.get("/contracts", response_model=List[ContractMetadata])
async def list_all_contracts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
):
    """
    List all contracts with pagination (newest first).

    Query params:
      - skip: offset (default 0)
      - limit: max results (default 20, max 100)
    """
    results = list_contracts(skip=skip, limit=limit)
    logger.info(f"Listed contracts: skip={skip}, limit={limit}, returned={len(results)}")
    return results
