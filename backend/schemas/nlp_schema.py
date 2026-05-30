"""
NLP Schemas
============
Pydantic models for NLP clause classification and
named entity recognition outputs.

Day 3:  Initial schema definitions.
Day 19: Added page_label to ClausePrediction,
        added field descriptions throughout.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ClausePrediction(BaseModel):
    """A single clause classification prediction."""
    clause_type: str = Field(..., description="CUAD clause type label")
    answer_text: str = Field(..., description="Extracted answer text for the clause")
    start_char: int = Field(0, ge=0, description="Start character offset in source text")
    end_char: int = Field(0, ge=0, description="End character offset in source text")
    page: int = Field(1, ge=1, description="Source page number (1-indexed)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence 0-1")
    is_present: bool = Field(True, description="Whether the clause is present in the contract")
    multi_label_predictions: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Raw multi-label predictions from Legal-BERT for this chunk",
    )
    page_label: Optional[str] = Field(
        None,
        description="Human-friendly page label for frontend display (e.g. 'Page 3 — Termination')",
    )


class EntityPrediction(BaseModel):
    """A single named entity extracted from contract text."""
    entity_type: str = Field(..., description="Entity type (e.g. PERSON, ORG, DATE, MONEY)")
    value: str = Field(..., description="Extracted entity text")
    position: Optional[int] = Field(None, description="Character position in source text")


class NLPOutput(BaseModel):
    """Complete NLP processing output for a contract."""
    contract_id: str = Field(..., description="Contract being processed")
    clauses: List[ClausePrediction] = Field(default_factory=list, description="Detected clauses")
    entities: List[EntityPrediction] = Field(default_factory=list, description="Extracted entities")
    processing_time_seconds: Optional[float] = Field(
        None, description="Total NLP processing time in seconds"
    )

