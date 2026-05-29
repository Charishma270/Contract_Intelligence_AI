"""
Vector DB Schemas
==================
Day 18: Pydantic models for FAISS vector store inspection
and chunk debugging endpoints.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# Index-level status
# -------------------------------------------------------------------

class VectorDBStatusResponse(BaseModel):
    """Health and statistics for the loaded FAISS index."""

    total_vectors: int = Field(
        ...,
        description="Number of vectors in the FAISS index",
    )

    dimension: int = Field(
        ...,
        description="Embedding dimension (e.g. 384)",
    )

    is_trained: bool = Field(
        ...,
        description="Whether the FAISS index is trained",
    )

    metadata_count: int = Field(
        ...,
        description=(
            "Number of metadata entries "
            "(should match total_vectors)"
        ),
    )

    index_type: str = Field(
        ...,
        description="FAISS index class name (e.g. IndexFlatIP)",
    )

    bm25_loaded: bool = Field(
        ...,
        description="Whether the BM25 lexical index is built",
    )


# -------------------------------------------------------------------
# Single chunk detail
# -------------------------------------------------------------------

class ChunkDetail(BaseModel):
    """A single stored chunk from the metadata store."""

    index: int = Field(
        ...,
        description="Position in the FAISS index",
    )

    text: str = Field(
        ...,
        description="Full clause text",
    )

    text_preview: str = Field(
        ...,
        description="First 200 characters of the clause",
    )

    label_name: str = Field(
        ...,
        description="CUAD label name",
    )

    target: Optional[int] = Field(
        None,
        description="Binary target (1 = positive, 0 = negative)",
    )

    word_count: int = Field(
        ...,
        description="Number of words in the clause",
    )


# -------------------------------------------------------------------
# Paginated chunk list
# -------------------------------------------------------------------

class ChunkListResponse(BaseModel):
    """Paginated list of stored chunks."""

    total: int = Field(
        ...,
        description="Total number of chunks in the store",
    )

    skip: int = Field(
        ...,
        description="Offset used for this page",
    )

    limit: int = Field(
        ...,
        description="Page size",
    )

    chunks: List[ChunkDetail] = Field(
        ...,
        description="Chunk details for this page",
    )


# -------------------------------------------------------------------
# Chunk search
# -------------------------------------------------------------------

class ChunkSearchRequest(BaseModel):
    """Search stored chunks by label or text keyword."""

    label: Optional[str] = Field(
        None,
        description=(
            "Filter by CUAD label name "
            "(case-insensitive partial match)"
        ),
    )

    keyword: Optional[str] = Field(
        None,
        description=(
            "Filter by text keyword "
            "(case-insensitive substring match)"
        ),
    )

    limit: int = Field(
        50,
        ge=1,
        le=200,
        description="Max results to return",
    )


class ChunkSearchResponse(BaseModel):
    """Filtered chunk search results."""

    match_count: int = Field(
        ...,
        description="Number of chunks matching the query",
    )

    chunks: List[ChunkDetail] = Field(
        ...,
        description="Matching chunk details",
    )
