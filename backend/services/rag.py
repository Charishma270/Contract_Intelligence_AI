from backend.schemas.rag_schema import ChatResponse, RetrievedChunk
from rag.retrieval.embedder import generate_embedding
from rag.vector_db.faiss_store import search_embedding
import re

def run_rag(contract_id: str, query: str) -> ChatResponse:
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    # Search similar clauses
    results = search_embedding(query_embedding, top_k=5)
    
    # Filter results by contract_id
    contract_results = []
    for res in results:
        if f"[Contract: {contract_id}" in res:
            contract_results.append(res)
            
    # Remove duplicates
    unique_results = list(set(contract_results))
    
    # We will format it as retrieved chunks
    retrieved_chunks = []
    for i, res in enumerate(unique_results):
        # Extract page number using regex
        page_match = re.search(r"Page: (\d+)", res)
        page = int(page_match.group(1)) if page_match else 1
        
        # Clean the meta tag for display
        clean_res = re.sub(r"\[Contract: .*, Page: \d+\] ", "", res)
        
        chunk = RetrievedChunk(
            chunk_id=f"chunk-{i+1}",
            text=clean_res,
            page=page,
            similarity_score=0.9 # We don't get score from our simple faiss_store
        )
        retrieved_chunks.append(chunk)

    if not retrieved_chunks:
        answer = "I could not find any relevant information for this query in the given contract."
        citations = []
    else:
        answer = "Based on the retrieved context, here are the most relevant sections of the contract:\n\n"
        for chunk in retrieved_chunks:
            answer += f"- {chunk.text}\n"
        citations = list(set([f"Page {c.page}" for c in retrieved_chunks]))

    return ChatResponse(
        answer=answer,
        retrieved_chunks=retrieved_chunks,
        citations=citations,
    )
