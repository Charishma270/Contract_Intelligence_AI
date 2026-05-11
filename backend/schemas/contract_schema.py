"""
Contract Schemas
================
Pydantic models for contract metadata, status tracking,
and the unified analysis response returned to the frontend.
"""

import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction


class ContractStatus(str, enum.Enum):
    """Processing status workflow for a contract."""
    UPLOADED = "uploaded"
    OCR_DONE = "ocr_done"
    NLP_DONE = "nlp_done"
    RAG_INDEXED = "rag_indexed"
    COMPLETED = "completed"
    FAILED = "failed"


class ContractMetadata(BaseModel):
    """Metadata tracked for every uploaded contract."""
    contract_id: str = Field(..., description="UUID of the contract")
    filename: str = Field(..., description="Original uploaded filename")
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    status: ContractStatus = Field(default=ContractStatus.UPLOADED)
    error_message: Optional[str] = Field(None, description="Error details if status is FAILED")
    file_size_bytes: Optional[int] = Field(None, description="Size of the uploaded PDF")


class RiskBreakdown(BaseModel):
    """Individual risk factor from the rule-based engine."""
    factor: str = Field(..., description="Risk factor name")
    score: int = Field(..., description="Points contributed to overall risk")
    severity: str = Field(..., description="low / medium / high / critical")
    description: str = Field(..., description="Explanation of the risk")


class AnalysisResponse(BaseModel):
    """Unified analysis response combining NLP + risk scoring."""
    contract_id: str
    filename: str
    status: ContractStatus
    risk_score: int = Field(0, ge=0, le=100, description="Overall risk score 0-100")
    risk_severity: str = Field("low", description="low / medium / high / critical")
    clauses: List[ClausePrediction] = Field(default_factory=list)
    entities: List[EntityPrediction] = Field(default_factory=list)
    risk_breakdown: List[RiskBreakdown] = Field(default_factory=list)


class UploadResponse(BaseModel):
    """Response returned after successful PDF upload."""
    contract_id: str
    filename: str
    status: str = "uploaded"
    message: str = "File uploaded successfully"
