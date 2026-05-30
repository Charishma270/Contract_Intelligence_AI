"""
Risk Score Route — /risk-score endpoint
========================================
Day 10: Rule-based risk scoring.
Day 12: Enhanced error handling with typed exceptions and validators.
Day 19: Moved RiskScoreResponse to contract_schema.py (schema consolidation).
"""

import logging

from fastapi import APIRouter
from typing import List

from backend.schemas.contract_schema import (
    RiskBreakdown,
    RiskScoreResponse,
)
from backend.services.pipeline import _compute_risk_score
from backend.services.mock_nlp import run_mock_nlp
from backend.utils.validators import validate_contract_exists

logger = logging.getLogger("contract_ai.risk")

router = APIRouter()


@router.get("/risk-score/{contract_id}", response_model=RiskScoreResponse)
async def get_risk_score(contract_id: str):
    """
    Get the risk score breakdown for a contract.

    Uses Charishma's rule-based scoring:
      - Unlimited liability → +30
      - Auto-renewal → +20
      - Termination for convenience → -5
      - Liability cap present → -10
      - Base contract risk → +30

    Raises:
      - 400: Invalid contract_id format
      - 404: Contract not found
      - 500: Risk scoring error
    """
    # Validate contract exists (UUID format + DB lookup)
    validate_contract_exists(contract_id)

    logger.info(f"Computing risk score for contract {contract_id}")

    # Run NLP to get clauses (mock for now)
    nlp_output = run_mock_nlp(contract_id)
    score, severity, breakdown = _compute_risk_score(nlp_output)

    return RiskScoreResponse(
        contract_id=contract_id,
        overall_risk=score,
        severity=severity,
        breakdown=breakdown,
    )
