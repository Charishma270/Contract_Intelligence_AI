"""
Celery Configuration
=====================
Day 17: Celery application factory and configuration for async task processing.
Day 20: Uses centralized backend.config.settings for all configuration.

The Celery app uses Redis as both the message broker and result backend.
All settings can be overridden via environment variables.

Usage:
    # Start worker:
    celery -A backend.celery_config worker --loglevel=info

    # Start worker with concurrency:
    celery -A backend.celery_config worker --loglevel=info --concurrency=4
"""

import logging

from celery import Celery

from backend.config import settings

logger = logging.getLogger("contract_ai.celery")

# ---------------------------------------------------------------------------
# Broker & Backend URLs (from centralized settings)
# ---------------------------------------------------------------------------
BROKER_URL = settings.CELERY_BROKER_URL

RESULT_BACKEND = settings.CELERY_RESULT_BACKEND


# ---------------------------------------------------------------------------
# Celery App Factory
# ---------------------------------------------------------------------------
def create_celery_app() -> Celery:
    """
    Create and configure the Celery application.

    Returns a configured Celery instance with:
      - Redis broker and result backend
      - JSON serialization for tasks and results
      - 24-hour result expiry
      - Late ack for reliability
      - Task time limits (5 min hard, 4 min soft)
      - Auto-discovery of tasks in backend.services.celery_tasks
    """
    app = Celery(
        "contract_ai",
        broker=BROKER_URL,
        backend=RESULT_BACKEND,
    )

    app.conf.update(
        # --- Serialization ---
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],

        # --- Result expiry ---
        result_expires=settings.CELERY_RESULT_EXPIRES,

        # --- Reliability ---
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        worker_prefetch_multiplier=1,

        # --- Time limits ---
        task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
        task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,

        # --- Timezone ---
        timezone="UTC",
        enable_utc=True,

        # --- Task tracking ---
        task_track_started=True,

        # --- Worker ---
        worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,

        # --- Task routes (optional, for future multi-queue setup) ---
        task_routes={
            "backend.services.celery_tasks.*": {"queue": "analysis"},
        },

        # --- Default queue ---
        task_default_queue="analysis",
    )

    # Auto-discover tasks from the services module
    app.autodiscover_tasks(
        ["backend.services"],
        related_name="celery_tasks",
    )

    logger.info(
        f"Celery app configured — broker={BROKER_URL}, "
        f"backend={RESULT_BACKEND}"
    )

    return app


# ---------------------------------------------------------------------------
# Module-level Celery instance (imported by tasks and workers)
# ---------------------------------------------------------------------------
celery_app = create_celery_app()
