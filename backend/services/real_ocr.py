"""
Real OCR Service
=================
Day 14: Production OCR adapter integrating Sruthi's pipeline into the backend.

Strategy:
  1. Fast-path: pdfplumber for native/digital PDFs (no OCR overhead)
  2. Fallback: Tesseract OCR via pdf2image for scanned documents
  3. Cleans text using ocr.preprocessing.text_preprocessing.clean_text()
  4. Chunks text using ocr.chunking.chunking.chunk_text()
  5. Returns structured OCROutput matching the Pydantic schema contract

The adapter never modifies Sruthi's original OCR modules — it imports
their functions directly and wraps them with error handling + logging.
"""

import logging
import os
import time
import uuid
from typing import List, Optional, Tuple

import pdfplumber
from pdf2image import convert_from_path
import pytesseract

from backend.schemas.ocr_schema import OCRChunk, OCROutput
from backend.services.ocr_config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    MIN_TEXT_LENGTH,
    OCR_DPI,
    POPPLER_PATH,
    TESSERACT_CMD,
)
from backend.utils.exceptions import OCRProcessingError

# Import Sruthi's modules (now importable via __init__.py files)
from ocr.preprocessing.text_preprocessing import clean_text
from ocr.chunking.chunking import chunk_text

logger = logging.getLogger("contract_ai.ocr")

# Configure Tesseract binary path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _extract_with_pdfplumber(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Extract text from each page using pdfplumber (fast, works on digital PDFs).
    Returns list of (page_number, raw_text) tuples.
    """
    pages: List[Tuple[int, str]] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                pages.append((page_num, text))
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {e}")
        return []
    return pages


def _extract_with_tesseract(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Extract text from each page using Tesseract OCR via pdf2image.
    Slower but handles scanned/image-based PDFs.
    Returns list of (page_number, raw_text) tuples.
    """
    pages: List[Tuple[int, str]] = []
    try:
        images = convert_from_path(
            pdf_path,
            dpi=OCR_DPI,
            poppler_path=POPPLER_PATH,
        )
        for page_num, img in enumerate(images, start=1):
            text = pytesseract.image_to_string(img)
            pages.append((page_num, text))
    except Exception as e:
        logger.error(f"Tesseract extraction failed: {e}")
        raise
    return pages


def _page_has_sufficient_text(text: str) -> bool:
    """Check if pdfplumber extracted enough text for a page."""
    return len(text.strip()) >= MIN_TEXT_LENGTH


def _build_chunks(
    contract_id: str,
    page_num: int,
    cleaned_text: str,
    source_file: str,
    extraction_method: str,
) -> List[OCRChunk]:
    """
    Split cleaned text into overlapping chunks and wrap each in an OCRChunk.
    Uses Sruthi's chunk_text() with configurable size/overlap.
    """
    if not cleaned_text.strip():
        return []

    raw_chunks = chunk_text(cleaned_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    ocr_chunks = []
    for chunk_text_content in raw_chunks:
        if chunk_text_content.strip():
            ocr_chunks.append(
                OCRChunk(
                    contract_id=contract_id,
                    chunk_id=str(uuid.uuid4()),
                    page=page_num,
                    text=chunk_text_content,
                    source_file=source_file,
                    extraction_method=extraction_method,
                )
            )
    return ocr_chunks


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def run_real_ocr(contract_id: str, file_path: str) -> OCROutput:
    """
    Extract text from a PDF contract using pdfplumber (fast)
    or Tesseract OCR (fallback for scanned docs).

    Pipeline:
      1. Validate file exists
      2. Try pdfplumber extraction (fast-path)
      3. For pages with insufficient text, fall back to Tesseract
      4. Clean text with Sruthi's preprocessor
      5. Chunk text with Sruthi's chunker
      6. Return structured OCROutput

    Args:
        contract_id: Unique contract identifier.
        file_path: Path to the uploaded PDF file.

    Returns:
        OCROutput with chunks, total_pages, extraction metadata.

    Raises:
        OCRProcessingError: If text extraction fails entirely.
    """
    start_time = time.perf_counter()

    # --- Validate file exists ---
    if not os.path.exists(file_path):
        raise OCRProcessingError(
            contract_id=contract_id,
            detail=f"PDF file not found: {file_path}",
        )

    logger.info(f"[{contract_id}] Starting OCR for: {file_path}")

    all_chunks: List[OCRChunk] = []
    total_pages = 0
    primary_method: Optional[str] = None
    pdfplumber_pages_used = 0
    tesseract_pages_used = 0

    try:
        # --- Step 1: Try pdfplumber fast-path ---
        logger.info(f"[{contract_id}] Attempting pdfplumber extraction...")
        plumber_pages = _extract_with_pdfplumber(file_path)

        if plumber_pages:
            total_pages = len(plumber_pages)
            logger.info(
                f"[{contract_id}] pdfplumber found {total_pages} pages"
            )

            # Check which pages have sufficient text
            pages_needing_ocr: List[int] = []
            plumber_results: dict = {}

            for page_num, text in plumber_pages:
                if _page_has_sufficient_text(text):
                    plumber_results[page_num] = text
                    pdfplumber_pages_used += 1
                else:
                    pages_needing_ocr.append(page_num)
                    logger.debug(
                        f"[{contract_id}] Page {page_num}: insufficient text "
                        f"({len(text.strip())} chars < {MIN_TEXT_LENGTH}), "
                        f"will use Tesseract"
                    )

            # --- Step 2: Tesseract fallback for sparse pages ---
            tesseract_results: dict = {}
            if pages_needing_ocr:
                logger.info(
                    f"[{contract_id}] Falling back to Tesseract for "
                    f"{len(pages_needing_ocr)} page(s): {pages_needing_ocr}"
                )
                try:
                    tess_pages = _extract_with_tesseract(file_path)
                    for page_num, text in tess_pages:
                        if page_num in pages_needing_ocr:
                            tesseract_results[page_num] = text
                            tesseract_pages_used += 1
                except Exception as e:
                    logger.warning(
                        f"[{contract_id}] Tesseract fallback failed: {e}. "
                        f"Using pdfplumber text for all pages."
                    )
                    # Use whatever pdfplumber got, even if sparse
                    for page_num in pages_needing_ocr:
                        raw = dict(plumber_pages).get(page_num, "")
                        plumber_results[page_num] = raw
                        pdfplumber_pages_used += 1

            # --- Step 3: Clean + chunk all pages ---
            for page_num in range(1, total_pages + 1):
                if page_num in tesseract_results:
                    raw_text = tesseract_results[page_num]
                    method = "tesseract"
                elif page_num in plumber_results:
                    raw_text = plumber_results[page_num]
                    method = "pdfplumber"
                else:
                    continue

                cleaned = clean_text(raw_text)
                chunks = _build_chunks(
                    contract_id=contract_id,
                    page_num=page_num,
                    cleaned_text=cleaned,
                    source_file=file_path,
                    extraction_method=method,
                )
                all_chunks.extend(chunks)

        else:
            # pdfplumber failed entirely — try full Tesseract
            logger.warning(
                f"[{contract_id}] pdfplumber returned no pages, "
                f"falling back to full Tesseract OCR"
            )
            tess_pages = _extract_with_tesseract(file_path)
            total_pages = len(tess_pages)
            tesseract_pages_used = total_pages

            for page_num, raw_text in tess_pages:
                cleaned = clean_text(raw_text)
                chunks = _build_chunks(
                    contract_id=contract_id,
                    page_num=page_num,
                    cleaned_text=cleaned,
                    source_file=file_path,
                    extraction_method="tesseract",
                )
                all_chunks.extend(chunks)

    except OCRProcessingError:
        raise
    except Exception as e:
        logger.error(f"[{contract_id}] OCR extraction failed: {e}", exc_info=True)
        raise OCRProcessingError(
            contract_id=contract_id,
            detail=str(e),
        )

    # --- Determine primary method ---
    if tesseract_pages_used > pdfplumber_pages_used:
        primary_method = "tesseract"
    elif pdfplumber_pages_used > 0:
        primary_method = "pdfplumber"
    else:
        primary_method = "unknown"

    elapsed = time.perf_counter() - start_time

    logger.info(
        f"[{contract_id}] OCR complete — {total_pages} pages, "
        f"{len(all_chunks)} chunks, method={primary_method}, "
        f"pdfplumber={pdfplumber_pages_used} pages, "
        f"tesseract={tesseract_pages_used} pages, "
        f"time={elapsed:.2f}s"
    )

    return OCROutput(
        contract_id=contract_id,
        chunks=all_chunks,
        total_pages=total_pages,
        extraction_method=primary_method,
        processing_time_seconds=round(elapsed, 3),
    )
