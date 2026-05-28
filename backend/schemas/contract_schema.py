import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction


class ContractStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
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


# ---------------------------------------------------------------------------
# Async task schemas (Day 17: Celery integration)
# ---------------------------------------------------------------------------
class AsyncTaskResponse(BaseModel):
    """Returned when an async analysis task is submitted."""
    task_id: str = Field(..., description="Celery task ID for polling")
    contract_id: str = Field(..., description="Contract being analyzed")
    status: str = Field("processing", description="Initial task status")
    message: str = Field(
        "Analysis task submitted successfully",
        description="Human-readable status message",
    )


class TaskStatusResponse(BaseModel):
    """Returned when polling task status."""
    task_id: str = Field(..., description="Celery task ID")
    state: str = Field(..., description="Task state: PENDING|STARTED|PROGRESS|SUCCESS|FAILURE|REVOKED")
    progress: Optional[dict] = Field(None, description="Progress metadata (current stage, percentage)")
    result: Optional[dict] = Field(None, description="Analysis result on SUCCESS")
    error: Optional[str] = Field(None, description="Error details on FAILURE")

