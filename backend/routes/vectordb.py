"""
Vector DB Route — /vectordb endpoints
=======================================
Day 18: Chunk inspection and index status for RAG debugging.
Exposes read-only views into the FAISS vector store.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.utils.jwt_utils import get_current_user_id

from backend.schemas.vectordb_schema import (
    ChunkDetail,
    ChunkListResponse,
    ChunkSearchRequest,
    ChunkSearchResponse,
    VectorDBStatusResponse,
)

from backend.services.vectordb_service import (
    get_vectordb_status,
    get_chunk_by_index,
    list_chunks,
    search_chunks,
)


logger = logging.getLogger("contract_ai.vectordb")

router = APIRouter()


# -------------------------------------------------------------------
# GET /status — index health
# -------------------------------------------------------------------

@router.get(
    "/status",
    response_model=VectorDBStatusResponse,
)
async def vectordb_status(
    user_id: int = Depends(get_current_user_id),
):
    """
    Return FAISS index health and statistics.

    Includes: total vectors, dimension, index type,
    metadata count, BM25 status.

    Raises:
      - 503: Index not loaded (0 vectors)
    """

    status = get_vectordb_status()

    if status.total_vectors == 0:

        logger.warning(
            "Vector DB status requested but "
            "index is empty (0 vectors)"
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "FAISS index is not loaded or empty. "
                "Run the ingestion pipeline first."
            ),
        )

    return status


# -------------------------------------------------------------------
# GET /chunks — paginated listing
# -------------------------------------------------------------------

@router.get(
    "/chunks",
    response_model=ChunkListResponse,
)
async def get_chunks(

    skip: int = Query(
        0,
        ge=0,
        description="Number of chunks to skip",
    ),

    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Number of chunks per page",
    ),

    user_id: int = Depends(get_current_user_id),
):
    """
    List stored chunks with pagination.

    Useful for browsing the vector store contents
    and verifying ingestion quality.

    Raises:
      - 503: Index not loaded (0 vectors)
    """

    status = get_vectordb_status()

    if status.total_vectors == 0:

        raise HTTPException(
            status_code=503,
            detail=(
                "FAISS index is not loaded or empty. "
                "Run the ingestion pipeline first."
            ),
        )

    return list_chunks(skip=skip, limit=limit)


# -------------------------------------------------------------------
# GET /chunks/{index} — single chunk
# -------------------------------------------------------------------

@router.get(
    "/chunks/{index}",
    response_model=ChunkDetail,
)
async def get_single_chunk(
    index: int,
    user_id: int = Depends(get_current_user_id),
):
    """
    Get a single chunk by its FAISS index position.

    Raises:
      - 404: Index out of range
      - 503: Index not loaded
    """

    status = get_vectordb_status()

    if status.total_vectors == 0:

        raise HTTPException(
            status_code=503,
            detail=(
                "FAISS index is not loaded or empty. "
                "Run the ingestion pipeline first."
            ),
        )

    chunk = get_chunk_by_index(index)

    if chunk is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Chunk index {index} is out of range. "
                f"Valid range: 0–{status.metadata_count - 1}."
            ),
        )

    return chunk


# -------------------------------------------------------------------
# POST /chunks/search — filter by label or keyword
# -------------------------------------------------------------------

@router.post(
    "/chunks/search",
    response_model=ChunkSearchResponse,
)
async def search_stored_chunks(
    request: ChunkSearchRequest,
    user_id: int = Depends(get_current_user_id),
):
    """
    Search stored chunks by label name or text keyword.

    Both filters are optional and applied together
    (AND logic) when both are provided.

    Raises:
      - 400: No search criteria provided
      - 503: Index not loaded
    """

    if not request.label and not request.keyword:

        raise HTTPException(
            status_code=400,
            detail=(
                "Provide at least one of 'label' "
                "or 'keyword' to search."
            ),
        )

    status = get_vectordb_status()

    if status.total_vectors == 0:

        raise HTTPException(
            status_code=503,
            detail=(
                "FAISS index is not loaded or empty. "
                "Run the ingestion pipeline first."
            ),
        )

    return search_chunks(
        label=request.label,
        keyword=request.keyword,
        limit=request.limit,
    )
