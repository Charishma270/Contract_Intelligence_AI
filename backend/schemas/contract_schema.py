"""
Contract Schemas
==================
Pydantic models for contract metadata, analysis responses,
risk scoring, upload responses, and async task management.

Day 3:  Initial schema definitions.
Day 17: Added AsyncTaskResponse, TaskStatusResponse.
Day 19: Consolidated RiskScoreResponse from risk.py,
        added TaskRevokeResponse, enhanced UploadResponse
        with timestamp and file_size_bytes.
"""

import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.schemas.nlp_schema import ClausePrediction, EntityPrediction


# -------------------------------------------------------------------
# Enums
# -------------------------------------------------------------------

class ContractStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    OCR_DONE = "ocr_done"
    NLP_DONE = "nlp_done"
    RAG_INDEXED = "rag_indexed"
    COMPLETED = "completed"
    FAILED = "failed"


# -------------------------------------------------------------------
# Contract metadata
# -------------------------------------------------------------------

class ContractMetadata(BaseModel):
    """Core metadata for a tracked contract."""
    contract_id: str = Field(..., description="Unique contract identifier (UUID)")
    filename: str = Field(..., description="Original uploaded filename")
    upload_time: datetime = Field(default_factory=datetime.utcnow, description="UTC timestamp of upload")
    status: ContractStatus = Field(default=ContractStatus.UPLOADED, description="Current processing status")
    error_message: Optional[str] = Field(None, description="Error details if status is FAILED")
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes")


# -------------------------------------------------------------------
# Risk scoring
# -------------------------------------------------------------------

class RiskBreakdown(BaseModel):
    """Individual risk factor contributing to the overall score."""
    factor: str = Field(..., description="Risk factor name (e.g. 'Unlimited liability')")
    score: int = Field(..., description="Score contribution for this factor")
    severity: str = Field(..., description="Severity level: low, medium, high")
    description: str = Field(..., description="Human-readable explanation")


class RiskScoreResponse(BaseModel):
    """Structured risk score response for a contract.

    Consolidated here from inline definition in risk.py (Day 19).
    """
    contract_id: str = Field(..., description="Contract being scored")
    overall_risk: int = Field(..., ge=0, le=100, description="Aggregate risk score 0-100")
    severity: str = Field(..., description="Overall severity: low, medium, high, critical")
    breakdown: List[RiskBreakdown] = Field(
        default_factory=list,
        description="Individual risk factor breakdown",
    )


# -------------------------------------------------------------------
# Analysis response
# -------------------------------------------------------------------

class AnalysisResponse(BaseModel):
    """Full analysis pipeline result returned by POST /api/analyze/{id}."""
    contract_id: str = Field(..., description="Contract identifier")
    filename: str = Field(..., description="Original filename")
    status: ContractStatus = Field(..., description="Final processing status")
    risk_score: int = Field(0, ge=0, le=100, description="Aggregate risk score")
    risk_severity: str = Field("low", description="Overall risk severity")
    clauses: List[ClausePrediction] = Field(default_factory=list, description="Detected clauses")
    entities: List[EntityPrediction] = Field(default_factory=list, description="Extracted entities")
    risk_breakdown: List[RiskBreakdown] = Field(default_factory=list, description="Risk factor details")


# -------------------------------------------------------------------
# Upload response
# -------------------------------------------------------------------

class UploadResponse(BaseModel):
    """Response returned after a successful contract upload.

    Day 19: Added timestamp and file_size_bytes for richer frontend display.
    """
    contract_id: str = Field(..., description="Assigned contract UUID")
    filename: str = Field(..., description="Original filename")
    status: str = Field("uploaded", description="Initial status")
    message: str = Field("File uploaded successfully", description="Human-readable result message")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of the upload",
    )
    file_size_bytes: Optional[int] = Field(
        None,
        description="Uploaded file size in bytes",
    )


# -------------------------------------------------------------------
# Async task schemas (Day 17: Celery integration)
# -------------------------------------------------------------------

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
    state: str = Field(
        ...,
        description="Task state: PENDING|STARTED|PROGRESS|SUCCESS|FAILURE|REVOKED",
    )
    progress: Optional[dict] = Field(None, description="Progress metadata (current stage, percentage)")
    result: Optional[dict] = Field(None, description="Analysis result on SUCCESS")
    error: Optional[str] = Field(None, description="Error details on FAILURE")


class TaskRevokeResponse(BaseModel):
    """Returned when a task is revoked/cancelled.

    Day 19: Replaces raw dict return in async_analyze.revoke_task.
    """
    task_id: str = Field(..., description="Revoked task ID")
    status: str = Field("revoked", description="Always 'revoked'")
    message: str = Field(..., description="Human-readable confirmation")

