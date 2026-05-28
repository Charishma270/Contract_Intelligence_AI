"""
Celery Task Definitions
========================
Day 17: Async task wrappers for the contract analysis pipeline.

These tasks are auto-discovered by the Celery app via autodiscover_tasks().
Each task wraps the existing synchronous pipeline and reports progress
through Celery's update_state() mechanism.

Usage:
    from backend.services.celery_tasks import run_pipeline_async
    result = run_pipeline_async.delay(contract_id)
    print(result.id)  # Celery task ID for polling
"""

import logging
import traceback

from backend.celery_config import celery_app
from backend.schemas.contract_schema import ContractStatus
from backend.services.tracking import (
    get_contract,
    update_contract_status,
)

logger = logging.getLogger("contract_ai.celery_tasks")


# ---------------------------------------------------------------------------
# Progress stage definitions
# ---------------------------------------------------------------------------
PIPELINE_STAGES = {
    "ocr": {"step": 1, "total": 4, "label": "OCR Text Extraction"},
    "nlp": {"step": 2, "total": 4, "label": "NLP Clause Classification & NER"},
    "rag": {"step": 3, "total": 4, "label": "RAG Vector Indexing"},
    "risk": {"step": 4, "total": 4, "label": "Risk Scoring"},
}


# ---------------------------------------------------------------------------
# Main async pipeline task
# ---------------------------------------------------------------------------
@celery_app.task(
    bind=True,
    name="backend.services.celery_tasks.run_pipeline_async",
    max_retries=1,
    default_retry_delay=30,
    acks_late=True,
)
def run_pipeline_async(self, contract_id: str) -> dict:
    """
    Execute the full analysis pipeline asynchronously via Celery.

    This task wraps the existing `run_pipeline()` function and adds:
      - Progress reporting via self.update_state()
      - Contract status tracking (PROCESSING → COMPLETED / FAILED)
      - Structured error handling with traceback capture

    Args:
        contract_id: UUID of the contract to analyze.

    Returns:
        dict: Serialized AnalysisResponse on success.

    Raises:
        Exception: Re-raised after updating contract status to FAILED.
    """
    task_id = self.request.id
    logger.info(
        f"[Task {task_id}] Starting async pipeline for contract {contract_id}"
    )

    # --- Validate contract exists ---
    contract = get_contract(contract_id)
    if not contract:
        error_msg = f"Contract '{contract_id}' not found in database"
        logger.error(f"[Task {task_id}] {error_msg}")
        self.update_state(
            state="FAILURE",
            meta={"error": error_msg, "contract_id": contract_id},
        )
        raise ValueError(error_msg)

    # --- Mark as processing ---
    update_contract_status(contract_id, ContractStatus.PROCESSING)

    # --- Report initial progress ---
    self.update_state(
        state="PROGRESS",
        meta={
            "contract_id": contract_id,
            "current_stage": "starting",
            "stage_label": "Initializing pipeline",
            "step": 0,
            "total_steps": 4,
            "percent": 0,
        },
    )

    try:
        # Import here to avoid circular imports and heavy model loading
        # at Celery app import time
        from backend.services.pipeline import run_pipeline

        # --- Run the pipeline with progress updates ---
        # We report progress before each stage starts
        for stage_key, stage_info in PIPELINE_STAGES.items():
            self.update_state(
                state="PROGRESS",
                meta={
                    "contract_id": contract_id,
                    "current_stage": stage_key,
                    "stage_label": stage_info["label"],
                    "step": stage_info["step"],
                    "total_steps": stage_info["total"],
                    "percent": int(
                        (stage_info["step"] - 1) / stage_info["total"] * 100
                    ),
                },
            )

        # Execute the full pipeline (this is the heavy synchronous work)
        result = run_pipeline(contract_id)

        # --- Report completion ---
        self.update_state(
            state="PROGRESS",
            meta={
                "contract_id": contract_id,
                "current_stage": "completed",
                "stage_label": "Pipeline completed",
                "step": 4,
                "total_steps": 4,
                "percent": 100,
            },
        )

        # Serialize the AnalysisResponse to dict for JSON storage
        result_dict = result.model_dump(mode="json")

        logger.info(
            f"[Task {task_id}] Pipeline completed for contract {contract_id} — "
            f"risk_score={result.risk_score} ({result.risk_severity})"
        )

        return result_dict

    except Exception as exc:
        # --- Handle failure ---
        error_msg = str(exc)
        tb = traceback.format_exc()

        logger.error(
            f"[Task {task_id}] Pipeline failed for contract {contract_id}: "
            f"{error_msg}\n{tb}"
        )

        # Update contract status to FAILED
        update_contract_status(
            contract_id,
            ContractStatus.FAILED,
            error_message=f"Async pipeline error: {error_msg}",
        )

        # Update Celery task state with error details
        self.update_state(
            state="FAILURE",
            meta={
                "contract_id": contract_id,
                "error": error_msg,
                "traceback": tb,
            },
        )

        # Re-raise so Celery marks the task as FAILURE
        raise


# ---------------------------------------------------------------------------
# Helper: Query task info from the result backend
# ---------------------------------------------------------------------------
from celery.result import AsyncResult


def get_task_info(task_id: str) -> dict:
    """
    Query the current state and result of a Celery task.

    Args:
        task_id: The Celery task ID returned at submission time.

    Returns:
        dict with keys: task_id, state, progress, result, error
    """
    result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "state": result.state,
        "progress": None,
        "result": None,
        "error": None,
    }

    if result.state == "PENDING":
        # Task not yet picked up (or unknown task_id)
        response["progress"] = {
            "current_stage": "pending",
            "stage_label": "Waiting for worker",
            "step": 0,
            "total_steps": 4,
            "percent": 0,
        }

    elif result.state == "STARTED":
        response["progress"] = {
            "current_stage": "started",
            "stage_label": "Worker picked up task",
            "step": 0,
            "total_steps": 4,
            "percent": 0,
        }

    elif result.state == "PROGRESS":
        # Custom state — meta contains progress info
        response["progress"] = result.info

    elif result.state == "SUCCESS":
        response["result"] = result.result
        response["progress"] = {
            "current_stage": "completed",
            "stage_label": "Pipeline completed",
            "step": 4,
            "total_steps": 4,
            "percent": 100,
        }

    elif result.state == "FAILURE":
        # result.info is the exception instance or meta dict
        error_info = result.info
        if isinstance(error_info, dict):
            response["error"] = error_info.get("error", str(error_info))
        elif isinstance(error_info, Exception):
            response["error"] = str(error_info)
        else:
            response["error"] = str(error_info)

    elif result.state == "REVOKED":
        response["error"] = "Task was cancelled"

    return response
