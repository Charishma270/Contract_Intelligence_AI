"""
Contracts Route — /api/contracts
=================================
Endpoints for querying contract status and listing all contracts.
"""

from typing import List

from fastapi import APIRouter, HTTPException, Query

from backend.schemas.contract_schema import ContractMetadata
from backend.services.tracking import get_contract, list_contracts

router = APIRouter()


@router.get("/contracts/{contract_id}", response_model=ContractMetadata)
async def get_contract_status(contract_id: str):
    """Get the current processing status of a contract."""
    contract = get_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail=f"Contract '{contract_id}' not found")
    return contract


@router.get("/contracts", response_model=List[ContractMetadata])
async def list_all_contracts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
):
    """List all contracts with pagination."""
    return list_contracts(skip=skip, limit=limit)
