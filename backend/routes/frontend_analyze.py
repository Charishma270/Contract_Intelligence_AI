"""
Frontend Analyze Route — POST /analyze
========================================
Bridge endpoint for frontend Analyze page.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from backend.utils.jwt_utils import get_current_user_id

from backend.services.rag_service import (
    analyze_contract_query
)

logger = logging.getLogger(
    "contract_ai.frontend_analyze"
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Frontend Request Schema
# ---------------------------------------------------------------------------

class FrontendAnalyzeRequest(
    BaseModel
):

    query: str = Field(
        ...,
        description="Legal clause search query",
        min_length=1
    )


# ---------------------------------------------------------------------------
# Frontend Response Schema
# ---------------------------------------------------------------------------

class FrontendClauseResult(
    BaseModel
):

    clause_type: str

    retrieved_label: str

    legal_bert_prediction: str

    legal_bert_confidence: float

    risk_level: str

    similarity_score: float

    hybrid_score: float

    model_disagreement: bool

    clause_text: str

    # -----------------------------------------
    # Additional analytics
    # -----------------------------------------

    classical_prediction: Optional[str] = None

    risk_score: Optional[float] = None

    keyword_score: Optional[float] = None

    reliability_band: Optional[str] = None

    weak_prediction: Optional[bool] = None

    explanation: Optional[str] = None

    bm25_score: Optional[float] = None

    fusion_score: Optional[float] = None

    retrieval_rerank_score: Optional[float] = None

    multi_label_predictions: Optional[list] = None


# ---------------------------------------------------------------------------
# Pipeline → Frontend Mapper
# ---------------------------------------------------------------------------

def _map_to_frontend_result(

    pipeline_result: dict
) -> FrontendClauseResult:

    # -----------------------------------------------------
    # Multi-label compatibility handling
    # -----------------------------------------------------

    multi_labels = []

    for label in pipeline_result.get(
        "multi_label_predictions",
        []
    ):

        # ---------------------------------------------
        # New pipeline format (string)
        # ---------------------------------------------

        if isinstance(label, str):

            multi_labels.append({

                "label": label,

                "confidence": None
            })

        # ---------------------------------------------
        # Old pipeline format (dict)
        # ---------------------------------------------

        elif isinstance(label, dict):

            multi_labels.append({

                "label": label.get(
                    "label",
                    "Unknown"
                ),

                "confidence": label.get(
                    "confidence"
                )
            })

    # -----------------------------------------------------
    # Main response mapping
    # -----------------------------------------------------

    return FrontendClauseResult(

        clause_type=pipeline_result.get(
            "retrieved_label",
            "Unknown"
        ),

        retrieved_label=pipeline_result.get(
            "retrieved_label",
            "Unknown"
        ),

        legal_bert_prediction=pipeline_result.get(
            "legal_bert_prediction",
            "Unknown"
        ),

        legal_bert_confidence=round(

            pipeline_result.get(
                "bert_confidence",
                0.0
            ),

            4
        ),

        risk_level=pipeline_result.get(
            "risk_level",
            "Unknown"
        ),

        similarity_score=round(

            pipeline_result.get(
                "semantic_score",
                0.0
            ),

            4
        ),

        hybrid_score=round(

            pipeline_result.get(
                "final_confidence",
                0.0
            ),

            4
        ),

        model_disagreement=pipeline_result.get(
            "model_disagreement",
            False
        ),

        clause_text=pipeline_result.get(
            "clause_text",
            ""
        ),

        # ---------------------------------------------
        # Analytics
        # ---------------------------------------------

        classical_prediction=pipeline_result.get(
            "classical_prediction"
        ),

        risk_score=pipeline_result.get(
            "risk_score"
        ),

        keyword_score=pipeline_result.get(
            "keyword_score"
        ),

        reliability_band=pipeline_result.get(
            "reliability_band"
        ),

        weak_prediction=pipeline_result.get(
            "weak_prediction"
        ),

        explanation=pipeline_result.get(
            "explanation"
        ),

        bm25_score=round(

            pipeline_result.get(
                "bm25_score",
                0.0
            ),

            4
        ),

        fusion_score=round(

            pipeline_result.get(
                "fusion_score",
                0.0
            ),

            4
        ),

        retrieval_rerank_score=round(

            pipeline_result.get(
                "retrieval_rerank_score",
                0.0
            ),

            4
        ),

        multi_label_predictions=multi_labels
    )


# ---------------------------------------------------------------------------
# POST /analyze
# ---------------------------------------------------------------------------

@router.post(

    "/analyze",

    response_model=List[
        FrontendClauseResult
    ],

    summary="Analyze clauses by query",

    description=(
        "Analyze legal clauses using "
        "the hybrid legal retrieval "
        "pipeline."
    ),
)

async def frontend_analyze(

    request: FrontendAnalyzeRequest,

    user_id: int = Depends(get_current_user_id),
):

    query = request.query.strip()

    logger.info(
        f"Frontend analyze request: query='{query}'"
    )

    try:

        # -------------------------------------------------
        # Run Hybrid Pipeline
        # -------------------------------------------------

        pipeline_results = analyze_contract_query(
            query
        )

        # -------------------------------------------------
        # SAFETY FIX
        # -------------------------------------------------

        if isinstance(
            pipeline_results,
            dict
        ):

            pipeline_results = pipeline_results.get(
                "results",
                []
            )

        # -------------------------------------------------
        # Frontend Mapping
        # -------------------------------------------------

        frontend_results = [

            _map_to_frontend_result(result)

            for result in pipeline_results

            if isinstance(result, dict)
        ]

        logger.info(

            f"Frontend analyze complete: "

            f"query='{query}', "

            f"results={len(frontend_results)}"
        )

        return frontend_results

    except Exception as e:

        logger.error(

            f"Frontend analyze failed: "

            f"query='{query}', "

            f"error={e}",

            exc_info=True
        )

        return []