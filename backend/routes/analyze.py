"""
Analyze Route — /analyze endpoint
==================================
Day 8: Main pipeline endpoint.
Day 12: Enhanced error handling with typed exceptions and validators.
"""

import logging

from fastapi import APIRouter

from backend.schemas.contract_schema import AnalysisResponse
from backend.services.pipeline import run_pipeline
from backend.utils.exceptions import PipelineError
from backend.utils.validators import validate_contract_not_failed

logger = logging.getLogger("contract_ai.analyze")

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

    Raises:
      - 400: Invalid contract_id or contract previously failed
      - 404: Contract not found
      - 500: Pipeline processing error

    Returns a unified AnalysisResponse with clauses, entities, and risk breakdown.
    """
    # Validates: UUID format, exists, not failed
    contract = validate_contract_not_failed(contract_id)
    logger.info(f"Starting analysis pipeline for contract {contract_id}")

    try:
        result = run_pipeline(contract_id)
        logger.info(f"Pipeline completed for contract {contract_id}")
        return result
    except FileNotFoundError as e:
        raise PipelineError(
            stage="file_lookup",
            contract_id=contract_id,
            detail=str(e),
        )
    except ValueError as e:
        raise PipelineError(
            stage="validation",
            contract_id=contract_id,
            detail=str(e),
        )
