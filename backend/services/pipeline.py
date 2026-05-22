"""
Pipeline Orchestrator
=====================
Central orchestration for the contract analysis pipeline.
Runs: OCR → NLP → RAG indexing sequentially, updating status at each stage.
Each stage is wrapped in try/except for error recovery.

Day 9: Extracted from analyze route into a clean reusable function.
"""

import logging
import uuid
from typing import Optional

from backend.schemas.contract_schema import (
    AnalysisResponse,
    ContractStatus,
    RiskBreakdown,
)
from backend.schemas.ocr_schema import OCRChunk, OCROutput
from backend.schemas.nlp_schema import NLPOutput
from backend.services.tracking import (
    get_contract,
    get_contract_file_path,
    update_contract_status,
)
from backend.services.mock_ocr import run_mock_ocr
from backend.services.mock_nlp import run_mock_nlp
from backend.services.mock_rag import run_mock_rag

logger = logging.getLogger("contract_ai.pipeline")


# ---------------------------------------------------------------------------
# Risk scoring (mock — Charishma will own the real logic)
# ---------------------------------------------------------------------------
def _compute_risk_score(nlp_output: NLPOutput) -> tuple:
    """
    Mock risk scoring based on detected clauses.
    Charishma's rules: unlimited liability → +30, auto-renewal → +20, etc.
    Returns (overall_score, severity, breakdown list).
    """
    breakdown = []
    score = 0

    clause_types = {c.clause_type.lower(): c for c in nlp_output.clauses if c.is_present}

    # Auto-renewal detected
    if "renewal term" in clause_types:
        points = 20
        score += points
        breakdown.append(RiskBreakdown(
            factor="Auto-Renewal Clause",
            score=points,
            severity="medium",
            description="Contract auto-renews, which may lock parties in unexpectedly.",
        ))

    # Uncapped liability detected
    if "uncapped liability" in clause_types:
        points = 30
        score += points
        breakdown.append(RiskBreakdown(
            factor="Uncapped Liability",
            score=points,
            severity="high",
            description="Some liabilities have no cap, exposing parties to unlimited risk.",
        ))

    # Termination for convenience (lowers risk slightly — it's protective)
    if "termination for convenience" in clause_types:
        points = -5
        score += points
        breakdown.append(RiskBreakdown(
            factor="Termination For Convenience",
            score=points,
            severity="low",
            description="Either party can exit with notice — reduces lock-in risk.",
        ))

    # Cap on liability present (lowers risk)
    if "cap on liability" in clause_types:
        points = -10
        score += points
        breakdown.append(RiskBreakdown(
            factor="Liability Cap Present",
            score=points,
            severity="low",
            description="Liability is capped, limiting maximum exposure.",
        ))

    # Base risk for any contract
    base = 30
    score += base
    breakdown.insert(0, RiskBreakdown(
        factor="Base Contract Risk",
        score=base,
        severity="low",
        description="Baseline risk inherent in any legal contract.",
    ))

    # Clamp to 0-100
    score = max(0, min(100, score))

    if score >= 75:
        severity = "critical"
    elif score >= 50:
        severity = "high"
    elif score >= 25:
        severity = "medium"
    else:
        severity = "low"

    return score, severity, breakdown


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline(contract_id: str) -> AnalysisResponse:
    """
    Execute the full analysis pipeline for a contract:
      1. Validate contract exists
      2. OCR extraction
      3. NLP clause classification + NER
      4. RAG indexing (mock)
      5. Risk scoring
      6. Return unified AnalysisResponse
    """
    # --- Validate ---
    contract = get_contract(contract_id)
    if not contract:
        raise ValueError(f"Contract '{contract_id}' not found in database")

    file_path = get_contract_file_path(contract_id)
    if not file_path:
        update_contract_status(contract_id, ContractStatus.FAILED, "File path not found")
        raise FileNotFoundError(f"File for contract '{contract_id}' not found")

    # --- Stage 1: OCR ---
    ocr_output: Optional[OCROutput] = None
    try:
        logger.info(f"[{contract_id}] Stage 1/4: Running OCR...")
        try:
            # Use Sruthi's real OCR pipeline
            from ocr.ocr_pipeline import process_contract
            raw_chunks = process_contract(file_path, contract_id)
            chunks = [
                OCRChunk(
                    contract_id=c["contract_id"],
                    chunk_id=c["chunk_id"],
                    page=c["page"],
                    text=c["text"],
                )
                for c in raw_chunks
            ]
            # Determine total pages from the chunks
            total_pages = max((c.page for c in chunks), default=0)
            ocr_output = OCROutput(
                contract_id=contract_id,
                chunks=chunks,
                total_pages=total_pages,
            )
            logger.info(f"[{contract_id}] Real OCR pipeline used")
        except (ImportError, OSError) as ocr_dep_err:
            # Fallback to mock if Tesseract/Poppler not available
            logger.warning(f"[{contract_id}] Real OCR unavailable ({ocr_dep_err}), using mock OCR")
            ocr_output = run_mock_ocr(contract_id, file_path)
        update_contract_status(contract_id, ContractStatus.OCR_DONE)
        logger.info(f"[{contract_id}] OCR complete — {ocr_output.total_pages} pages, {len(ocr_output.chunks)} chunks")
    except Exception as e:
        logger.error(f"[{contract_id}] OCR failed: {e}")
        update_contract_status(contract_id, ContractStatus.FAILED, f"OCR error: {e}")
        raise

    # --- Stage 2: NLP (NER + Clause Classification) ---
    nlp_output: Optional[NLPOutput] = None
    try:
        logger.info(f"[{contract_id}] Stage 2/4: Running NLP...")
        nlp_output = run_mock_nlp(contract_id)
        update_contract_status(contract_id, ContractStatus.NLP_DONE)
        logger.info(f"[{contract_id}] NLP complete — {len(nlp_output.clauses)} clauses, {len(nlp_output.entities)} entities")
    except Exception as e:
        logger.error(f"[{contract_id}] NLP failed: {e}")
        update_contract_status(contract_id, ContractStatus.FAILED, f"NLP error: {e}")
        raise

    # --- Stage 3: RAG Indexing ---
    try:
        logger.info(f"[{contract_id}] Stage 3/4: Indexing for RAG...")
        
        # Integrate FAISS indexing
        if ocr_output and ocr_output.chunks:
            from rag.chunking.preprocessor import clean_text
            from rag.retrieval.embedder import generate_embedding
            from rag.vector_db.faiss_store import add_embedding
            
            for chunk in ocr_output.chunks:
                cleaned_text = clean_text(chunk.text)
                if cleaned_text.strip():
                    text_with_meta = f"[Contract: {contract_id}, Page: {chunk.page}] {cleaned_text}"
                    embedding = generate_embedding(text_with_meta)
                    add_embedding(embedding, text_with_meta)
                    
        update_contract_status(contract_id, ContractStatus.RAG_INDEXED)
        logger.info(f"[{contract_id}] RAG indexing complete")
    except Exception as e:
        logger.error(f"[{contract_id}] RAG indexing failed: {e}")
        update_contract_status(contract_id, ContractStatus.FAILED, f"RAG error: {e}")
        raise

    # --- Stage 4: Risk Scoring ---
    try:
        logger.info(f"[{contract_id}] Stage 4/4: Computing risk score...")
        risk_score, risk_severity, risk_breakdown = _compute_risk_score(nlp_output)
        update_contract_status(contract_id, ContractStatus.COMPLETED)
        logger.info(f"[{contract_id}] Pipeline complete — risk={risk_score} ({risk_severity})")
    except Exception as e:
        logger.error(f"[{contract_id}] Risk scoring failed: {e}")
        update_contract_status(contract_id, ContractStatus.FAILED, f"Risk scoring error: {e}")
        raise

    # --- Build response ---
    return AnalysisResponse(
        contract_id=contract_id,
        filename=contract.filename,
        status=ContractStatus.COMPLETED,
        risk_score=risk_score,
        risk_severity=risk_severity,
        clauses=nlp_output.clauses,
        entities=nlp_output.entities,
        risk_breakdown=risk_breakdown,
    )
