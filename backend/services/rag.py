from backend.schemas.rag_schema import (
    ChatResponse,
    RetrievedChunk
)

from rag.pipeline.pipeline import (
    run_pipeline
)


# ---------------------------------------------------------
# RAG Service
# ---------------------------------------------------------

def run_rag(

    contract_id: str,

    query: str
) -> ChatResponse:

    # -----------------------------------------------------
    # Run Hybrid Retrieval Pipeline
    # -----------------------------------------------------

    pipeline_output = run_pipeline(
        query
    )

    results = pipeline_output.get(
        "results",
        []
    )

    retrieved_chunks = []

    # -----------------------------------------------------
    # Convert Pipeline Results
    # -----------------------------------------------------

    for i, result in enumerate(results):

        chunk = RetrievedChunk(

            chunk_id=f"chunk-{i+1}",

            text=result.get(
                "clause_text",
                "No clause text available."
            ),

            page=result.get(
                "page",
                1
            ),

            similarity_score=float(

                result.get(
                    "fusion_score",
                    0.0
                )
            )
        )

        retrieved_chunks.append(
            chunk
        )

    # -----------------------------------------------------
    # Generate Answer
    # -----------------------------------------------------

    if not retrieved_chunks:

        answer = (
            "I could not find relevant "
            "contract information."
        )

        citations = []

    else:

        answer = (
            "Based on the hybrid legal "
            "retrieval pipeline, the "
            "following clauses were "
            "identified:\n\n"
        )

        for chunk in retrieved_chunks:

            answer += (
                f"- {chunk.text[:300]}...\n"
            )

        citations = list(

            set([
                f"Page {c.page}"
                for c in retrieved_chunks
            ])
        )

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return ChatResponse(

        answer=answer,

        retrieved_chunks=retrieved_chunks,

        citations=citations,
    )