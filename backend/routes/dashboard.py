"""
Dashboard Routes
=================
Endpoint for aggregated dashboard statistics.

Queries the existing contracts database to provide counts
matching the frontend dashboard stat cards.
"""

import logging

from fastapi import APIRouter

from backend.services.tracking import (
    SessionLocal,
    ContractRecord,
)

logger = logging.getLogger("contract_ai.dashboard")

router = APIRouter()


# -----------------------------------------------------------------
# GET /api/dashboard/stats
# -----------------------------------------------------------------
@router.get("/stats")
async def dashboard_stats():
    """Return aggregated dashboard statistics.

    Pulls from the existing contracts table to provide:
    - Total contracts
    - Status breakdown (uploaded, processing, completed, failed)
    - Counts for the frontend's stat cards
    """
    db = SessionLocal()
    try:
        total = db.query(ContractRecord).count()

        uploaded = db.query(ContractRecord).filter(
            ContractRecord.status == "uploaded"
        ).count()

        processing = db.query(ContractRecord).filter(
            ContractRecord.status == "processing"
        ).count()

        completed = db.query(ContractRecord).filter(
            ContractRecord.status == "completed"
        ).count()

        failed = db.query(ContractRecord).filter(
            ContractRecord.status == "failed"
        ).count()

        return {
            "success": True,
            "stats": {
                "total_contracts": total,
                "uploaded": uploaded,
                "processing": processing,
                "completed": completed,
                "failed": failed,
                # Placeholder risk counts — will be
                # populated from actual analysis results
                # once the frontend integrates these.
                "high_risk_clauses": 0,
                "medium_risk_clauses": 0,
                "low_risk_clauses": 0,
            },
        }
    finally:
        db.close()
