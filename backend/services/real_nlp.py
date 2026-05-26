"""
Real NLP Service
=================
Day 15: Production NLP adapter integrating Charishma's Legal-BERT multi-label
clause classifier and spaCy NER into the backend analysis pipeline.

Strategy:
  1. Lazy-load Legal-BERT multi-label model + tokenizer + label mappings once
  2. Lazy-load spaCy NER model once
  3. For each OCR chunk: run multi-label classification → aggregate per clause type
  4. For concatenated text: run spaCy NER → deduplicate entities
  5. Return structured NLPOutput matching the Pydantic schema contract

The adapter wraps Charishma's trained models (models/legal_bert_multilabel/)
with error handling, logging, and aggregation logic.

All heavy ML imports (torch, transformers, spacy) are lazy to allow the module
to be imported even when these packages are not installed (e.g., in CI).
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from backend.schemas.nlp_schema import (
    ClausePrediction,
    EntityPrediction,
    NLPOutput,
)
from backend.schemas.ocr_schema import OCROutput
from backend.services.nlp_config import (
    CONFIDENCE_THRESHOLD,
    LABEL_MAP_PATH,
    MAX_CHUNKS_TO_PROCESS,
    MAX_SEQUENCE_LENGTH,
    MULTILABEL_MODEL_PATH,
    MULTILABEL_TOKENIZER_PATH,
    SPACY_ENTITY_MAP,
    SPACY_MODEL,
)
from backend.utils.exceptions import NLPProcessingError

logger = logging.getLogger("contract_ai.nlp")


# ---------------------------------------------------------------------------
# Lazy Singleton: Legal-BERT Multi-Label Classifier
# ---------------------------------------------------------------------------
_multilabel_model: Any = None
_multilabel_tokenizer: Any = None
_index_to_label: Optional[Dict[str, str]] = None


def _load_multilabel_model():
    """
    Load the Legal-BERT multi-label classifier, tokenizer, and label mappings.
    Called once on first NLP invocation; cached in module-level globals.
    """
    global _multilabel_model, _multilabel_tokenizer, _index_to_label

    if _multilabel_model is not None:
        return

    # Lazy imports — these are heavy and may not be installed in all envs
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    logger.info("Loading Legal-BERT multi-label model (first call)...")
    start = time.perf_counter()

    _multilabel_tokenizer = AutoTokenizer.from_pretrained(MULTILABEL_TOKENIZER_PATH)
    _multilabel_model = AutoModelForSequenceClassification.from_pretrained(
        MULTILABEL_MODEL_PATH
    )
    _multilabel_model.eval()

    with open(LABEL_MAP_PATH, "r") as f:
        label_mapping = json.load(f)
    _index_to_label = label_mapping["index_to_label"]

    elapsed = time.perf_counter() - start
    logger.info(
        f"Legal-BERT multi-label loaded in {elapsed:.2f}s — "
        f"{len(_index_to_label)} labels"
    )


# ---------------------------------------------------------------------------
# Lazy Singleton: spaCy NER Model
# ---------------------------------------------------------------------------
_spacy_nlp: Any = None


def _load_spacy_model():
    """
    Load the spaCy NER model. Called once on first NLP invocation.
    """
    global _spacy_nlp

    if _spacy_nlp is not None:
        return

    import spacy

    logger.info(f"Loading spaCy model '{SPACY_MODEL}' (first call)...")
    start = time.perf_counter()
    _spacy_nlp = spacy.load(SPACY_MODEL)
    elapsed = time.perf_counter() - start
    logger.info(f"spaCy model loaded in {elapsed:.2f}s")


# ---------------------------------------------------------------------------
# Clause Classification (Multi-Label Legal-BERT)
# ---------------------------------------------------------------------------
def _classify_single_chunk(text: str) -> List[dict]:
    """
    Run multi-label Legal-BERT inference on a single text chunk.

    Returns list of dicts: [{"label": "...", "confidence": 0.XX}, ...]
    Only labels with confidence >= CONFIDENCE_THRESHOLD are included.
    """
    import torch

    _load_multilabel_model()

    inputs = _multilabel_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_SEQUENCE_LENGTH,
    )

    with torch.no_grad():
        outputs = _multilabel_model(**inputs)

    probabilities = torch.sigmoid(outputs.logits)[0]

    detected = []
    for idx, prob in enumerate(probabilities):
        prob_val = prob.item()
        if prob_val >= CONFIDENCE_THRESHOLD:
            label_name = _index_to_label.get(str(idx), f"Label_{idx}")
            detected.append({
                "label": label_name,
                "confidence": round(prob_val, 4),
            })

    # Sort by confidence descending
    detected.sort(key=lambda x: x["confidence"], reverse=True)
    return detected


def _classify_chunks(
    contract_id: str,
    chunks: list,
) -> Tuple[List[ClausePrediction], int]:
    """
    Run clause classification on all OCR chunks and aggregate results.

    For each clause type, keeps the detection with the highest confidence
    across all chunks. Returns (clause_predictions, chunks_processed).
    """
    # Limit number of chunks to process
    process_chunks = chunks
    if MAX_CHUNKS_TO_PROCESS > 0 and len(chunks) > MAX_CHUNKS_TO_PROCESS:
        logger.warning(
            f"[{contract_id}] {len(chunks)} chunks exceed limit "
            f"({MAX_CHUNKS_TO_PROCESS}), processing first {MAX_CHUNKS_TO_PROCESS}"
        )
        process_chunks = chunks[:MAX_CHUNKS_TO_PROCESS]

    # Best detection per clause type: {clause_type: (confidence, text, page, predictions)}
    best_per_type: Dict[str, Tuple[float, str, int, List[dict]]] = {}

    for chunk in process_chunks:
        text = chunk.text.strip()
        if not text:
            continue

        try:
            predictions = _classify_single_chunk(text)
        except Exception as e:
            logger.warning(
                f"[{contract_id}] Classification failed for chunk "
                f"(page {chunk.page}): {e}"
            )
            continue

        for pred in predictions:
            label = pred["label"]
            conf = pred["confidence"]

            if label not in best_per_type or conf > best_per_type[label][0]:
                best_per_type[label] = (conf, text, chunk.page, predictions)

    # Convert to ClausePrediction objects
    clause_predictions = []
    for clause_type, (confidence, answer_text, page, multi_preds) in sorted(
        best_per_type.items(), key=lambda x: x[1][0], reverse=True
    ):
        clause_predictions.append(
            ClausePrediction(
                clause_type=clause_type,
                answer_text=answer_text[:500],  # Truncate long chunks
                start_char=0,
                end_char=len(answer_text[:500]),
                page=page,
                confidence=confidence,
                is_present=True,
                multi_label_predictions=multi_preds,
            )
        )

    return clause_predictions, len(process_chunks)


# ---------------------------------------------------------------------------
# Named Entity Recognition (spaCy)
# ---------------------------------------------------------------------------
def _extract_entities(
    contract_id: str,
    full_text: str,
) -> List[EntityPrediction]:
    """
    Run spaCy NER on the full contract text and return deduplicated entities.

    Maps spaCy entity labels to our schema types using SPACY_ENTITY_MAP.
    Deduplicates by (entity_type, normalized_value) pair.
    """
    _load_spacy_model()

    if not full_text.strip():
        return []

    # spaCy has a max length; process in segments if needed
    max_len = _spacy_nlp.max_length
    text_to_process = full_text[:max_len] if len(full_text) > max_len else full_text

    doc = _spacy_nlp(text_to_process)

    seen = set()  # (entity_type, normalized_value) for dedup
    entities = []

    for ent in doc.ents:
        # Map spaCy label to our schema type
        mapped_type = SPACY_ENTITY_MAP.get(ent.label_)
        if mapped_type is None:
            continue  # Skip unmapped or explicitly None types

        value = ent.text.strip()
        if not value or len(value) < 2:
            continue

        # Deduplicate by (type, normalized value)
        dedup_key = (mapped_type, value.lower())
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        entities.append(
            EntityPrediction(
                entity_type=mapped_type,
                value=value,
                position=ent.start_char,
            )
        )

    return entities


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
def run_real_nlp(contract_id: str, ocr_output: Optional[OCROutput]) -> NLPOutput:
    """
    Execute real NLP analysis on OCR-extracted contract text:
      1. Multi-label clause classification (Legal-BERT) on each chunk
      2. Named Entity Recognition (spaCy) on full concatenated text
      3. Aggregate and return structured NLPOutput

    Args:
        contract_id: Unique contract identifier.
        ocr_output: Structured OCR output with text chunks.

    Returns:
        NLPOutput with detected clauses and named entities.

    Raises:
        NLPProcessingError: If NLP processing fails entirely.
    """
    start_time = time.perf_counter()

    if not ocr_output or not ocr_output.chunks:
        logger.warning(f"[{contract_id}] No OCR chunks to process for NLP")
        return NLPOutput(
            contract_id=contract_id,
            processing_time_seconds=0.0,
        )

    logger.info(
        f"[{contract_id}] Starting NLP — {len(ocr_output.chunks)} chunks, "
        f"{ocr_output.total_pages} pages"
    )

    try:
        # --- Step 1: Clause Classification ---
        logger.info(f"[{contract_id}] Running multi-label clause classification...")
        clauses, chunks_processed = _classify_chunks(contract_id, ocr_output.chunks)
        logger.info(
            f"[{contract_id}] Classification complete — "
            f"{len(clauses)} clause types detected from {chunks_processed} chunks"
        )

        # --- Step 2: Named Entity Recognition ---
        logger.info(f"[{contract_id}] Running NER...")
        full_text = "\n".join(
            chunk.text for chunk in ocr_output.chunks if chunk.text.strip()
        )
        entities = _extract_entities(contract_id, full_text)
        logger.info(f"[{contract_id}] NER complete — {len(entities)} entities found")

    except NLPProcessingError:
        raise
    except Exception as e:
        logger.error(f"[{contract_id}] NLP failed: {e}", exc_info=True)
        raise NLPProcessingError(
            contract_id=contract_id,
            detail=str(e),
        )

    elapsed = time.perf_counter() - start_time

    logger.info(
        f"[{contract_id}] NLP complete — "
        f"{len(clauses)} clauses, {len(entities)} entities, "
        f"time={elapsed:.2f}s"
    )

    return NLPOutput(
        contract_id=contract_id,
        clauses=clauses,
        entities=entities,
        processing_time_seconds=round(elapsed, 3),
    )
