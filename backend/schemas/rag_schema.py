"""
RAG Schemas
===========
Pydantic models for Retrieval-Augmented Generation (RAG) pipeline.
Matches Tisha's FAISS retrieval output format.
"""

from typing import List
from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    """A single chunk returned by FAISS similarity search."""
    chunk_id: str = Field(..., description="ID of the retrieved chunk")
    text: str = Field(..., description="Content of the retrieved chunk")
    page: int = Field(..., ge=1, description="Source page number")
    similarity_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Cosine similarity score from FAISS"
    )


class ChatRequest(BaseModel):
    """User query for the RAG chatbot."""
    contract_id: str = Field(..., description="Contract to query against")
    query: str = Field(..., min_length=1, description="Natural language question")


class ChatResponse(BaseModel):
    """RAG chatbot response with citations."""
    answer: str = Field(..., description="Generated answer from the LLM")
    retrieved_chunks: List[RetrievedChunk] = Field(
        default_factory=list,
        description="Chunks used to generate the answer"
    )
    citations: List[str] = Field(
        default_factory=list,
        description="Human-readable citations, e.g. ['Page 3', 'Page 7']"
    )
