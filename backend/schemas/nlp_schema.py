from typing import List, Optional
from pydantic import BaseModel, Field


class ClausePrediction(BaseModel):
    clause_type: str = Field(...)
    answer_text: str = Field(...)
    start_char: int = Field(..., ge=0)
    end_char: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    is_present: bool = Field(True)


class EntityPrediction(BaseModel):
    entity_type: str = Field(...)
    value: str = Field(...)
    position: Optional[int] = Field(None)


class NLPOutput(BaseModel):
    contract_id: str
    clauses: List[ClausePrediction] = Field(default_factory=list)
    entities: List[EntityPrediction] = Field(default_factory=list)
