from fastapi import APIRouter

from backend.schemas.rag_schema import (
    QueryRequest,
    QueryResponse
)

from backend.services.rag_service import (
    analyze_contract_query
)

router = APIRouter()


@router.post(
    "/rag/analyze",
    response_model=QueryResponse
)
def analyze_query(
    request: QueryRequest
):

    pipeline_output = (
        analyze_contract_query(
            request.query
        )
    )

    return {

        "summary":
            pipeline_output["summary"],

        "results":
            pipeline_output["results"]
    }