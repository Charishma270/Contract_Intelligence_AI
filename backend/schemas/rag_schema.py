from typing import List

from pydantic import BaseModel


class QueryRequest(BaseModel):

    query: str


class ClauseResult(BaseModel):

    retrieved_label: str

    classical_prediction: str

    legal_bert_prediction: str

    risk_level: str

    semantic_score: float

    bert_confidence: float

    bert_confidence_band: str

    final_confidence: float

    reliability_band: str

    model_disagreement: bool

    weak_prediction: bool

    target: int

    clause_text: str


class QueryResponse(BaseModel):

    results: List[ClauseResult]