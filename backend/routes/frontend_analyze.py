"""
Frontend Analyze Route — POST /analyze
========================================
Bridge endpoint for Mukt's frontend Analyze page.

Accepts:  { "query": "termination clause" }
Returns:  List of clause results matching the frontend's expected shape.

Internally delegates to the RAG hybrid pipeline
(rag/pipeline/pipeline.py → run_pipeline) which performs:
  - Query expansion
  - FAISS semantic retrieval
  - Classical ML + Legal-BERT classification
  - Multi-label prediction
  - Risk scoring + explainability

The response is re-shaped to match what the frontend expects,
mapping the pipeline's internal field names to the frontend's schema.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.rag_service import analyze_contract_query

logger = logging.getLogger("contract_ai.frontend_analyze")

router = APIRouter()


# ---------------------------------------------------------------------------
# Frontend-facing schemas (matching Mukt's expected format)
# ---------------------------------------------------------------------------
class FrontendAnalyzeRequest(BaseModel):
    """Request body from the frontend Analyze page."""
    query: str = Field(..., description="Legal clause search query", min_length=1)


class FrontendClauseResult(BaseModel):
    """Single clause result in the format the frontend expects."""
    clause_type: str = Field(..., description="The type/label of the clause")
    retrieved_label: str = Field(..., description="Label from FAISS retrieval")
    legal_bert_prediction: str = Field(..., description="Legal-BERT predicted label")
    legal_bert_confidence: float = Field(..., description="Legal-BERT confidence score")
    risk_level: str = Field(..., description="Risk level: High/Medium/Low")
    similarity_score: float = Field(..., description="Semantic similarity score from FAISS")
    hybrid_score: float = Field(..., description="Weighted hybrid confidence score")
    model_disagreement: bool = Field(..., description="Whether models disagree on prediction")
    clause_text: str = Field(..., description="The actual clause text")
    # Additional fields from the pipeline (bonus for frontend)
    classical_prediction: Optional[str] = Field(None, description="Classical ML prediction")
    risk_score: Optional[float] = Field(None, description="Risk score (0-100)")
    keyword_score: Optional[float] = Field(None, description="Keyword overlap score")
    reliability_band: Optional[str] = Field(None, description="Reliability band label")
    weak_prediction: Optional[bool] = Field(None, description="Whether prediction is weak")
    explanation: Optional[str] = Field(None, description="Human-readable explanation")


# ---------------------------------------------------------------------------
# Pipeline result → Frontend shape mapping
# ---------------------------------------------------------------------------
def _map_to_frontend_result(pipeline_result: dict) -> FrontendClauseResult:
    """
    Map the RAG pipeline's internal result dict to the frontend's
    expected FrontendClauseResult format.

    Pipeline fields → Frontend fields:
      retrieved_label       → retrieved_label, clause_type
      legal_bert_prediction → legal_bert_prediction
      bert_confidence       → legal_bert_confidence
      risk_level            → risk_level
      semantic_score        → similarity_score
      final_confidence      → hybrid_score
      model_disagreement    → model_disagreement
      clause_text           → clause_text
    """
    return FrontendClauseResult(
        clause_type=pipeline_result.get("retrieved_label", "Unknown"),
        retrieved_label=pipeline_result.get("retrieved_label", "Unknown"),
        legal_bert_prediction=pipeline_result.get("legal_bert_prediction", "Unknown"),
        legal_bert_confidence=pipeline_result.get("bert_confidence", 0.0),
        risk_level=pipeline_result.get("risk_level", "Unknown"),
        similarity_score=round(pipeline_result.get("semantic_score", 0.0), 4),
        hybrid_score=round(pipeline_result.get("final_confidence", 0.0), 4),
        model_disagreement=pipeline_result.get("model_disagreement", False),
        clause_text=pipeline_result.get("clause_text", ""),
        # Bonus fields
        classical_prediction=pipeline_result.get("classical_prediction"),
        risk_score=pipeline_result.get("risk_score"),
        keyword_score=pipeline_result.get("keyword_score"),
        reliability_band=pipeline_result.get("reliability_band"),
        weak_prediction=pipeline_result.get("weak_prediction"),
        explanation=pipeline_result.get("explanation"),
    )


# ---------------------------------------------------------------------------
# POST /analyze
# ---------------------------------------------------------------------------
@router.post(
    "/analyze",
    response_model=List[FrontendClauseResult],
    summary="Analyze clauses by query (Frontend Integration)",
    description=(
        "Accepts a natural language query and returns matching legal clauses "
        "with classification predictions, risk levels, and confidence scores. "
        "Powers the frontend Analyze page."
    ),
)
async def frontend_analyze(request: FrontendAnalyzeRequest):
    """
    Frontend-facing analyze endpoint.

    Accepts: { "query": "termination clause" }
    Returns: List of clause results with predictions and risk levels.
    """
    query = request.query.strip()
    logger.info(f"Frontend analyze request: query='{query}'")

    try:
        # Run the full RAG hybrid pipeline
        pipeline_results = analyze_contract_query(query)

        # Map pipeline results to frontend-expected format
        frontend_results = [
            _map_to_frontend_result(result)
            for result in pipeline_results
        ]

        logger.info(
            f"Frontend analyze complete: query='{query}', "
            f"results={len(frontend_results)}"
        )

        return frontend_results

    except Exception as e:
        logger.error(f"Frontend analyze failed: query='{query}', error={e}", exc_info=True)
        # Return empty list rather than 500 — frontend can show "no results" gracefully
        return []
