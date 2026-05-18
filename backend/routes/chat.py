"""
Chat Route — /chat endpoint
============================
Day 11: RAG-powered chatbot. Accepts a query + contract_id,
calls Tisha's FAISS retrieval, returns answer with citations.
"""

from fastapi import APIRouter, HTTPException

from backend.schemas.rag_schema import ChatRequest, ChatResponse
from backend.services.tracking import get_contract
from backend.services.rag import run_rag

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_contract(request: ChatRequest):
    """
    Ask a natural language question about an uploaded contract.

    Uses RAG (Retrieval-Augmented Generation):
      1. Retrieves relevant chunks via FAISS similarity search
      2. Injects context into LLM prompt
      3. Returns grounded answer with page citations
    """
    contract = get_contract(request.contract_id)
    if not contract:
        raise HTTPException(
            status_code=404,
            detail=f"Contract '{request.contract_id}' not found."
        )

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:
        response = run_rag(request.contract_id, request.query)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat query failed: {str(e)}"
        )
