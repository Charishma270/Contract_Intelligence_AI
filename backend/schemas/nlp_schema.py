from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ClausePrediction(BaseModel):
    clause_type: str = Field(...)
    answer_text: str = Field(...)
    start_char: int = Field(0, ge=0)
    end_char: int = Field(0, ge=0)
    page: int = Field(1, ge=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    is_present: bool = Field(True)
    multi_label_predictions: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Raw multi-label predictions from Legal-BERT for this chunk",
    )


class EntityPrediction(BaseModel):
    entity_type: str = Field(...)
    value: str = Field(...)
    position: Optional[int] = Field(None)


class NLPOutput(BaseModel):
    contract_id: str
    clauses: List[ClausePrediction] = Field(default_factory=list)
    entities: List[EntityPrediction] = Field(default_factory=list)
    processing_time_seconds: Optional[float] = Field(
        None, description="Total NLP processing time in seconds"
    )
