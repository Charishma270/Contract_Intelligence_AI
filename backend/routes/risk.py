"""
Risk Score Route — /risk-score endpoint
========================================
Day 10: Endpoint that calls Charishma's risk scoring logic (mock for now)
and returns a structured breakdown.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from backend.schemas.contract_schema import RiskBreakdown
from backend.services.tracking import get_contract
from backend.services.pipeline import _compute_risk_score
from backend.services.mock_nlp import run_mock_nlp

router = APIRouter()


class RiskScoreResponse(BaseModel):
    """Structured risk score response for a contract."""
    contract_id: str
    overall_risk: int = Field(..., ge=0, le=100)
    severity: str
    breakdown: List[RiskBreakdown]


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
    """
    contract = get_contract(contract_id)
    if not contract:
        raise HTTPException(
            status_code=404,
            detail=f"Contract '{contract_id}' not found."
        )

    # Run NLP to get clauses (mock for now)
    nlp_output = run_mock_nlp(contract_id)
    score, severity, breakdown = _compute_risk_score(nlp_output)

    return RiskScoreResponse(
        contract_id=contract_id,
        overall_risk=score,
        severity=severity,
        breakdown=breakdown,
    )
