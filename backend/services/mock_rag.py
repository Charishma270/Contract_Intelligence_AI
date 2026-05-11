from backend.schemas.rag_schema import ChatResponse, RetrievedChunk


def run_mock_rag(contract_id: str, query: str) -> ChatResponse:
    retrieved_chunks = [
        RetrievedChunk(
            chunk_id="chunk-001",
            text=(
                "2.3 Termination for Convenience. Either party may terminate this "
                "Agreement for convenience upon sixty (60) days' prior written notice "
                "to the other party."
            ),
            page=2,
            similarity_score=0.92,
        ),
        RetrievedChunk(
            chunk_id="chunk-002",
            text=(
                "2.2 Renewal. This Agreement shall automatically renew for successive "
                "one (1) year periods unless either party provides written notice of "
                "non-renewal at least ninety (90) days prior to the end of the "
                "then-current term."
            ),
            page=2,
            similarity_score=0.85,
        ),
        RetrievedChunk(
            chunk_id="chunk-003",
            text=(
                "3.1 Cap on Liability. EXCEPT FOR OBLIGATIONS UNDER SECTION 5, "
                "NEITHER PARTY'S TOTAL AGGREGATE LIABILITY SHALL EXCEED THE AMOUNTS "
                "PAID OR PAYABLE UNDER THIS AGREEMENT DURING THE TWELVE (12) MONTH "
                "PERIOD PRECEDING THE CLAIM."
            ),
            page=3,
            similarity_score=0.78,
        ),
    ]

    answer = (
        f"Based on the contract for '{contract_id}', regarding your question: "
        f"'{query}' — The agreement includes a termination for convenience clause "
        f"allowing either party to terminate with 60 days' written notice (Page 2). "
        f"The contract automatically renews annually unless 90 days' notice is given "
        f"(Page 2). The liability is generally capped at 12 months of payments (Page 3), "
        f"but exceptions exist for confidentiality breaches and gross negligence."
    )

    citations = [f"Page {c.page}" for c in retrieved_chunks]
    seen = set()
    unique_citations = []
    for c in citations:
        if c not in seen:
            seen.add(c)
            unique_citations.append(c)

    return ChatResponse(
        answer=answer,
        retrieved_chunks=retrieved_chunks,
        citations=unique_citations,
    )
