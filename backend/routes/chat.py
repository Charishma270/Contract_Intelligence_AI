"""
Chat Route — /chat endpoint
============================
Day 11: RAG-powered chatbot.
Day 12: Enhanced error handling with typed exceptions and validators.
"""

import logging

from fastapi import APIRouter

from backend.schemas.rag_schema import ChatRequest, ChatResponse
from backend.services.rag import run_rag
from backend.utils.validators import validate_contract_exists, validate_query

logger = logging.getLogger("contract_ai.chat")

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_contract(request: ChatRequest):
    """
    Ask a natural language question about an uploaded contract.

    Uses RAG (Retrieval-Augmented Generation):
      1. Retrieves relevant chunks via FAISS similarity search
      2. Injects context into LLM prompt
      3. Returns grounded answer with page citations

    Raises:
      - 400: Invalid contract_id, empty query, or contract not analyzed
      - 404: Contract not found
      - 500: RAG retrieval error
    """
    # Validate contract exists (UUID format + DB lookup)
    validate_contract_exists(request.contract_id)

    # Validate and clean query
    cleaned_query = validate_query(request.query)

    logger.info(
        f"Chat query for contract {request.contract_id}: "
        f"'{cleaned_query[:80]}...'" if len(cleaned_query) > 80
        else f"Chat query for contract {request.contract_id}: '{cleaned_query}'"
    )

    response = run_rag(request.contract_id, cleaned_query)
    return response
