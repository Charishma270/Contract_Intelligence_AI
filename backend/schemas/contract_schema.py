import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction


class ContractStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    OCR_DONE = "ocr_done"
    NLP_DONE = "nlp_done"
    RAG_INDEXED = "rag_indexed"
    COMPLETED = "completed"
    FAILED = "failed"


class ContractMetadata(BaseModel):
    contract_id: str = Field(...)
    filename: str = Field(...)
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    status: ContractStatus = Field(default=ContractStatus.UPLOADED)
    error_message: Optional[str] = Field(None)
    file_size_bytes: Optional[int] = Field(None)


class RiskBreakdown(BaseModel):
    factor: str = Field(...)
    score: int = Field(...)
    severity: str = Field(...)
    description: str = Field(...)


class AnalysisResponse(BaseModel):
    contract_id: str
    filename: str
    status: ContractStatus
    risk_score: int = Field(0, ge=0, le=100)
    risk_severity: str = Field("low")
    clauses: List[ClausePrediction] = Field(default_factory=list)
    entities: List[EntityPrediction] = Field(default_factory=list)
    risk_breakdown: List[RiskBreakdown] = Field(default_factory=list)


class UploadResponse(BaseModel):
    contract_id: str
    filename: str
    status: str = "uploaded"
    message: str = "File uploaded successfully"
