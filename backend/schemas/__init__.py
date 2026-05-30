"""
Backend Schemas Package
========================
Day 19: Comprehensive re-export of all public schemas.
"""

from backend.schemas.ocr_schema import OCRChunk, OCROutput

from backend.schemas.nlp_schema import (
    ClausePrediction,
    EntityPrediction,
    NLPOutput,
)

from backend.schemas.rag_schema import (
    RetrievedChunk,
    ChatRequest,
    ChatResponse,
    QueryRequest,
    QueryResponse,
    MultiLabelPrediction,
    ClauseResult,
    ContractSummary,
)

from backend.schemas.contract_schema import (
    ContractStatus,
    ContractMetadata,
    RiskBreakdown,
    RiskScoreResponse,
    AnalysisResponse,
    UploadResponse,
    AsyncTaskResponse,
    TaskStatusResponse,
    TaskRevokeResponse,
)

from backend.schemas.vectordb_schema import (
    VectorDBStatusResponse,
    ChunkDetail,
    ChunkListResponse,
    ChunkSearchRequest,
    ChunkSearchResponse,
)

__all__ = [
    # OCR
    "OCRChunk", "OCROutput",
    # NLP
    "ClausePrediction", "EntityPrediction", "NLPOutput",
    # RAG
    "RetrievedChunk", "ChatRequest", "ChatResponse",
    "QueryRequest", "QueryResponse",
    "MultiLabelPrediction", "ClauseResult", "ContractSummary",
    # Contract
    "ContractStatus", "ContractMetadata",
    "RiskBreakdown", "RiskScoreResponse",
    "AnalysisResponse", "UploadResponse",
    "AsyncTaskResponse", "TaskStatusResponse", "TaskRevokeResponse",
    # Vector DB
    "VectorDBStatusResponse", "ChunkDetail",
    "ChunkListResponse", "ChunkSearchRequest", "ChunkSearchResponse",
]

