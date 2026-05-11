"""
NLP Schemas
===========
Pydantic models for NER and clause classification output.
Matches Charishma's CUAD extractive-QA pipeline — spans matter, not just labels.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ClausePrediction(BaseModel):
    """A single clause detected via extractive QA on CUAD."""
    clause_type: str = Field(
        ...,
        description="Clause category, e.g. 'Termination For Convenience', "
                    "'Renewal Term', 'Cap On Liability', 'Uncapped Liability'"
    )
    answer_text: str = Field(..., description="Extracted answer span from the contract")
    start_char: int = Field(..., ge=0, description="Start character offset in source text")
    end_char: int = Field(..., ge=0, description="End character offset in source text")
    page: int = Field(..., ge=1, description="Page where the clause was found")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score")
    is_present: bool = Field(True, description="Whether the clause is present in the contract")


class EntityPrediction(BaseModel):
    """A single named entity extracted via NER."""
    entity_type: str = Field(
        ...,
        description="Entity category, e.g. 'ORGANIZATION', 'DATE', "
                    "'MONETARY_VALUE', 'JURISDICTION', 'PERSON'"
    )
    value: str = Field(..., description="Extracted entity text")
    position: Optional[int] = Field(None, description="Character offset in source text")


class NLPOutput(BaseModel):
    """Combined NLP output for a contract."""
    contract_id: str
    clauses: List[ClausePrediction] = Field(default_factory=list)
    entities: List[EntityPrediction] = Field(default_factory=list)
