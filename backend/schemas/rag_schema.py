"""
RAG Schemas
============
Pydantic models for RAG (Retrieval-Augmented Generation) pipeline,
chat interface, and hybrid legal retrieval responses.

Day 11: Initial RAG schemas.
Day 19: Added average_confidence to ContractSummary,
        added field descriptions throughout.
"""

from typing import List, Dict, Any

from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# OLD MOCK RAG SCHEMAS
# (required by existing backend pipeline)
# -------------------------------------------------------------------

class RetrievedChunk(BaseModel):
    """A single chunk retrieved from the vector store."""

    chunk_id: str = Field(..., description="Unique chunk identifier")

    text: str = Field(..., description="Chunk text content")

    page: int = Field(..., description="Source page number")

    similarity_score: float = Field(..., description="Cosine similarity score")


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""

    contract_id: str = Field(..., description="Contract to query against")

    query: str = Field(..., description="Natural language question")


class ChatResponse(BaseModel):
    """Response from the /chat endpoint.

    The `answer` field is the canonical response — frontend should
    use `data.answer` to display the chatbot reply.
    """

    answer: str = Field(..., description="Generated answer from RAG pipeline")

    retrieved_chunks: List[RetrievedChunk] = Field(
        default_factory=list,
        description="Source chunks used to generate the answer",
    )

    citations: List[str] = Field(
        default_factory=list,
        description="Page-level citations for the answer",
    )


# -------------------------------------------------------------------
# NEW HYBRID RAG PIPELINE SCHEMAS
# (Legal-BERT + FAISS integration)
# -------------------------------------------------------------------

class QueryRequest(BaseModel):
    """Request body for the hybrid RAG analyze endpoint."""

    query: str = Field(..., description="Legal clause search query")


# -------------------------------------------------------------------
# Multi-label prediction structure
# -------------------------------------------------------------------

class MultiLabelPrediction(BaseModel):
    """A single label prediction from multi-label Legal-BERT."""

    label: str = Field(..., description="CUAD label name")

    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence")


# -------------------------------------------------------------------
# Main clause result schema
# -------------------------------------------------------------------

class ClauseResult(BaseModel):
    """Detailed result for a single clause from the hybrid pipeline."""

    retrieved_label: str = Field(..., description="Label from retrieval")

    classical_prediction: str = Field(..., description="Classical ML prediction")

    legal_bert_prediction: str = Field(..., description="Legal-BERT prediction")

    multi_label_predictions: List[
        MultiLabelPrediction
    ] = Field(default_factory=list, description="All multi-label predictions")

    risk_level: str = Field(..., description="Risk level: Low, Medium, High")

    risk_score: float = Field(..., description="Numeric risk score")

    semantic_score: float = Field(..., description="FAISS semantic similarity score")

    keyword_score: float = Field(..., description="BM25 keyword match score")

    bert_confidence: float = Field(..., description="Legal-BERT confidence")

    final_confidence: float = Field(..., description="Hybrid fusion confidence")

    retrieval_rerank_score: float = Field(..., description="Reranking score")

    reliability_band: str = Field(..., description="Confidence band: high, medium, low")

    model_disagreement: bool = Field(..., description="True if retrieval and BERT disagree")

    weak_prediction: bool = Field(..., description="True if confidence is below threshold")

    explanation: str = Field(..., description="AI-generated explanation of the prediction")

    target: int = Field(..., description="Binary target (1=positive, 0=negative)")

    clause_text: str = Field(..., description="Full clause text")


# -------------------------------------------------------------------
# Final API response
# -------------------------------------------------------------------

class ContractSummary(BaseModel):
    """Aggregate summary statistics for the analysis results.

    Day 19: Added average_confidence — the Analyze.jsx frontend
    renders this in the summary dashboard.
    """

    overall_risk: str = Field(..., description="Overall risk level: Low, Medium, High")

    top_detected_labels: List[str] = Field(
        default_factory=list,
        description="Most frequently detected CUAD labels",
    )

    high_confidence_clauses: int = Field(
        0,
        description="Count of clauses with confidence above threshold",
    )

    average_confidence: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Mean confidence across all detected clauses",
    )


class QueryResponse(BaseModel):
    """Top-level response for the hybrid RAG pipeline."""

    summary: ContractSummary = Field(..., description="Aggregate analysis summary")

    results: List[ClauseResult] = Field(
        default_factory=list,
        description="Per-clause detailed results",
    )