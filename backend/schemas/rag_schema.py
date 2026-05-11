from typing import List
from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    chunk_id: str = Field(...)
    text: str = Field(...)
    page: int = Field(..., ge=1)
    similarity_score: float = Field(..., ge=0.0, le=1.0)


class ChatRequest(BaseModel):
    contract_id: str = Field(...)
    query: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str = Field(...)
    retrieved_chunks: List[RetrievedChunk] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)
