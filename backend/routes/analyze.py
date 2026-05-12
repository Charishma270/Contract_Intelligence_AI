"""
Analyze Route — /analyze endpoint
==================================
Day 8: Main pipeline endpoint. Takes a contract_id, runs it through
OCR → NLP → RAG → Risk scoring sequentially, returns structured analysis.
"""

from fastapi import APIRouter, HTTPException

from backend.schemas.contract_schema import AnalysisResponse
from backend.services.tracking import get_contract
from backend.services.pipeline import run_pipeline

router = APIRouter()


@router.post("/analyze/{contract_id}", response_model=AnalysisResponse)
async def analyze_contract(contract_id: str):
    """
    Run the full analysis pipeline on an uploaded contract.

    Pipeline stages:
      1. OCR text extraction
      2. NLP clause classification + NER
      3. RAG vector indexing
      4. Risk scoring

    Returns a unified AnalysisResponse with clauses, entities, and risk breakdown.
    """
    # Check contract exists
    contract = get_contract(contract_id)
    if not contract:
        raise HTTPException(
            status_code=404,
            detail=f"Contract '{contract_id}' not found. Upload a PDF first via /api/upload."
        )

    # Check it hasn't already failed
    if contract.status == "failed":
        raise HTTPException(
            status_code=400,
            detail=f"Contract '{contract_id}' previously failed: {contract.error_message}"
        )

    try:
        result = run_pipeline(contract_id)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline failed for contract '{contract_id}': {str(e)}"
        )
