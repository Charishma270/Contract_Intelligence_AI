from typing import List

from pydantic import BaseModel


# -------------------------------------------------------------------
# OLD MOCK RAG SCHEMAS
# (required by existing backend pipeline)
# -------------------------------------------------------------------

class RetrievedChunk(BaseModel):

    chunk_id: str

    text: str

    page: int

    similarity_score: float


class ChatRequest(BaseModel):

    query: str


class ChatResponse(BaseModel):

    answer: str

    retrieved_chunks: List[RetrievedChunk]

    citations: List[str]


# -------------------------------------------------------------------
# NEW HYBRID RAG PIPELINE SCHEMAS
# (Legal-BERT + FAISS integration)
# -------------------------------------------------------------------

class QueryRequest(BaseModel):

    query: str


class ClauseResult(BaseModel):

    retrieved_label: str

    classical_prediction: str

    legal_bert_prediction: str

    multi_label_predictions: List[str]

    risk_level: str

    semantic_score: float

    keyword_score: float

    bert_confidence: float

    final_confidence: float

    retrieval_rerank_score: float

    reliability_band: str

    model_disagreement: bool

    weak_prediction: bool

    explanation: str

    target: int

    clause_text: str


class QueryResponse(BaseModel):

    results: List[ClauseResult]