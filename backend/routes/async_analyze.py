"""
Async Analyze Route — /analyze/{id}/async & /tasks endpoints
=============================================================
Day 17: Asynchronous contract analysis via Celery.
Day 19: Added TaskRevokeResponse schema for revoke endpoint.

Provides:
  - POST /api/analyze/{contract_id}/async  → Submit analysis as background task
  - GET  /api/tasks/{task_id}              → Poll task status and progress
  - POST /api/tasks/{task_id}/revoke       → Cancel a running/pending task
"""

import logging

from fastapi import APIRouter, Depends

from celery.result import AsyncResult

from backend.utils.jwt_utils import get_current_user_id

from backend.celery_config import celery_app
from backend.schemas.contract_schema import (
    AsyncTaskResponse,
    ContractStatus,
    TaskStatusResponse,
    TaskRevokeResponse,
)
from backend.services.celery_tasks import (
    get_task_info,
    run_pipeline_async,
)
from backend.services.tracking import update_contract_status
from backend.utils.exceptions import ContractAIError
from backend.utils.validators import validate_contract_not_failed

logger = logging.getLogger("contract_ai.async_analyze")

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /api/analyze/{contract_id}/async — Submit async analysis
# ---------------------------------------------------------------------------
@router.post(
    "/analyze/{contract_id}/async",
    response_model=AsyncTaskResponse,
    status_code=202,
    summary="Submit async analysis",
    description=(
        "Submit a contract for asynchronous analysis via Celery. "
        "Returns immediately with a task_id for polling."
    ),
)
async def submit_async_analysis(
    contract_id: str,
    user_id: int = Depends(get_current_user_id),
):
    """
    Submit the analysis pipeline as an async Celery task.

    1. Validates contract exists and hasn't failed
    2. Submits run_pipeline_async.delay(contract_id) to Celery
    3. Updates contract status to PROCESSING
    4. Returns task_id for status polling

    Raises:
      - 400: Invalid contract_id or contract previously failed
      - 404: Contract not found
    """
    # Validate contract
    contract = validate_contract_not_failed(contract_id)

    logger.info(
        f"Submitting async analysis for contract {contract_id}"
    )

    # Submit to Celery
    task = run_pipeline_async.delay(contract_id)

    # Update status to processing
    update_contract_status(contract_id, ContractStatus.PROCESSING)

    logger.info(
        f"Async task submitted: task_id={task.id}, "
        f"contract_id={contract_id}"
    )

    return AsyncTaskResponse(
        task_id=task.id,
        contract_id=contract_id,
        status="processing",
        message=(
            f"Analysis task submitted for contract '{contract.filename}'. "
            f"Poll GET /api/tasks/{task.id} for progress."
        ),
    )


# ---------------------------------------------------------------------------
# GET /api/tasks/{task_id} — Poll task status
# ---------------------------------------------------------------------------
@router.get(
    "/tasks/{task_id}",
    response_model=TaskStatusResponse,
    summary="Get task status",
    description=(
        "Poll the current status of an async analysis task. "
        "States: PENDING, STARTED, PROGRESS, SUCCESS, FAILURE, REVOKED."
    ),
)
async def get_task_status(
    task_id: str,
    user_id: int = Depends(get_current_user_id),
):
    """
    Query the current state and result of a Celery task.

    Returns:
      - PENDING: Task not yet picked up by a worker
      - STARTED: Worker has received the task
      - PROGRESS: Task is running, includes stage info
      - SUCCESS: Task completed, includes AnalysisResponse result
      - FAILURE: Task failed, includes error details
      - REVOKED: Task was cancelled
    """
    logger.info(f"Task status query: task_id={task_id}")

    info = get_task_info(task_id)

    return TaskStatusResponse(
        task_id=info["task_id"],
        state=info["state"],
        progress=info["progress"],
        result=info["result"],
        error=info["error"],
    )


# ---------------------------------------------------------------------------
# POST /api/tasks/{task_id}/revoke — Cancel a task
# ---------------------------------------------------------------------------
@router.post(
    "/tasks/{task_id}/revoke",
    response_model=TaskRevokeResponse,
    summary="Cancel a task",
    description="Revoke (cancel) a pending or running async analysis task.",
)
async def revoke_task(
    task_id: str,
    user_id: int = Depends(get_current_user_id),
):
    """
    Cancel a Celery task by ID.

    - If PENDING: removed from the queue
    - If STARTED: sent SIGTERM to the worker process (terminate=True)

    Returns confirmation of the revocation request.
    """
    logger.info(f"Revoking task: task_id={task_id}")

    result = AsyncResult(task_id, app=celery_app)

    # Revoke with terminate=True to kill running tasks
    result.revoke(terminate=True, signal="SIGTERM")

    logger.info(f"Task revoked: task_id={task_id}")

    return TaskRevokeResponse(
        task_id=task_id,
        status="revoked",
        message=(
            f"Task {task_id} has been revoked. "
            "If the task was running, it will be terminated."
        ),
    )

