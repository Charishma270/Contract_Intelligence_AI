from fastapi import APIRouter, Depends

from backend.utils.jwt_utils import get_current_user_id

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
    request: QueryRequest,
    user_id: int = Depends(get_current_user_id),
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