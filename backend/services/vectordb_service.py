"""
Vector DB Service
==================
Day 18: Read-only service layer for inspecting the FAISS
vector store and its metadata. All functions are safe —
no mutations to the index or metadata.
"""

import logging

from typing import List, Optional

from backend.schemas.vectordb_schema import (
    ChunkDetail,
    ChunkListResponse,
    ChunkSearchResponse,
    VectorDBStatusResponse,
)

from rag.vector_db import faiss_store


logger = logging.getLogger("contract_ai.vectordb")


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _metadata_to_chunk(
    idx: int,
    meta: dict,
) -> ChunkDetail:
    """Convert a raw metadata dict to a ChunkDetail schema."""

    text = meta.get("text", "")

    return ChunkDetail(

        index=idx,

        text=text,

        text_preview=text[:200],

        label_name=meta.get(
            "label_name",
            "Unknown",
        ),

        target=meta.get("target"),

        word_count=len(text.split()),
    )


# -------------------------------------------------------------------
# Status
# -------------------------------------------------------------------

def get_vectordb_status() -> VectorDBStatusResponse:
    """Return index-level health and statistics."""

    index = faiss_store.index
    metadata = faiss_store.metadata_store

    # Check if BM25 is loaded by looking for the
    # global bm25 object in the bm25_retriever module
    bm25_loaded = False

    try:
        from rag.retrieval import bm25_retriever

        bm25_loaded = (
            hasattr(bm25_retriever, "bm25")
            and bm25_retriever.bm25 is not None
        )

    except ImportError:
        pass

    status = VectorDBStatusResponse(

        total_vectors=index.ntotal,

        dimension=index.d,

        is_trained=index.is_trained,

        metadata_count=len(metadata),

        index_type=type(index).__name__,

        bm25_loaded=bm25_loaded,
    )

    logger.info(
        f"Vector DB status: {status.total_vectors} vectors, "
        f"dim={status.dimension}, "
        f"metadata={status.metadata_count}"
    )

    return status


# -------------------------------------------------------------------
# List chunks (paginated)
# -------------------------------------------------------------------

def list_chunks(
    skip: int = 0,
    limit: int = 20,
) -> ChunkListResponse:
    """Return a paginated slice of stored chunks."""

    metadata = faiss_store.metadata_store
    total = len(metadata)

    page = metadata[skip : skip + limit]

    chunks = [
        _metadata_to_chunk(skip + i, meta)
        for i, meta in enumerate(page)
    ]

    logger.info(
        f"Listed chunks: skip={skip}, "
        f"limit={limit}, "
        f"returned={len(chunks)}/{total}"
    )

    return ChunkListResponse(

        total=total,

        skip=skip,

        limit=limit,

        chunks=chunks,
    )


# -------------------------------------------------------------------
# Get single chunk by index
# -------------------------------------------------------------------

def get_chunk_by_index(
    idx: int,
) -> Optional[ChunkDetail]:
    """Return a single chunk at the given index, or None."""

    metadata = faiss_store.metadata_store

    if idx < 0 or idx >= len(metadata):
        return None

    return _metadata_to_chunk(
        idx,
        metadata[idx],
    )


# -------------------------------------------------------------------
# Search chunks
# -------------------------------------------------------------------

def search_chunks(
    label: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 50,
) -> ChunkSearchResponse:
    """Filter chunks by label and/or text keyword."""

    metadata = faiss_store.metadata_store
    matches: List[ChunkDetail] = []

    label_lower = (
        label.lower() if label else None
    )

    keyword_lower = (
        keyword.lower() if keyword else None
    )

    for idx, meta in enumerate(metadata):

        # Label filter (case-insensitive partial)
        if label_lower:

            chunk_label = meta.get(
                "label_name", ""
            ).lower()

            if label_lower not in chunk_label:
                continue

        # Text filter (case-insensitive substring)
        if keyword_lower:

            chunk_text = meta.get(
                "text", ""
            ).lower()

            if keyword_lower not in chunk_text:
                continue

        matches.append(
            _metadata_to_chunk(idx, meta)
        )

        if len(matches) >= limit:
            break

    logger.info(
        f"Chunk search: label={label}, "
        f"keyword={keyword}, "
        f"matches={len(matches)}"
    )

    return ChunkSearchResponse(

        match_count=len(matches),

        chunks=matches,
    )
