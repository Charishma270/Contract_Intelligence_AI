from typing import List

from fastapi import APIRouter, HTTPException, Query

from backend.schemas.contract_schema import ContractMetadata
from backend.services.tracking import get_contract, list_contracts

router = APIRouter()


@router.get("/contracts/{contract_id}", response_model=ContractMetadata)
async def get_contract_status(contract_id: str):
    contract = get_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail=f"Contract '{contract_id}' not found")
    return contract


@router.get("/contracts", response_model=List[ContractMetadata])
async def list_all_contracts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return list_contracts(skip=skip, limit=limit)
