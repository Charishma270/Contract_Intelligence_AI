"""
OCR Configuration
==================
Day 14: Externalized OCR settings with environment variable overrides.

All constants can be overridden via environment variables prefixed with OCR_.
"""

import os


# ---------------------------------------------------------------------------
# Tesseract / Poppler paths
# ---------------------------------------------------------------------------
POPPLER_PATH: str = os.environ.get(
    "OCR_POPPLER_PATH",
    r"C:\poppler\poppler-26.02.0\Library\bin",
)

TESSERACT_CMD: str = os.environ.get(
    "OCR_TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
)

# ---------------------------------------------------------------------------
# Extraction thresholds
# ---------------------------------------------------------------------------
# Minimum characters per page from pdfplumber before falling back to Tesseract.
# If pdfplumber extracts fewer chars than this, the page is considered
# "scanned" and Tesseract OCR is used instead.
MIN_TEXT_LENGTH: int = int(os.environ.get("OCR_MIN_TEXT_LENGTH", "50"))

# ---------------------------------------------------------------------------
# Chunking parameters
# ---------------------------------------------------------------------------
CHUNK_SIZE: int = int(os.environ.get("OCR_CHUNK_SIZE", "200"))
CHUNK_OVERLAP: int = int(os.environ.get("OCR_CHUNK_OVERLAP", "50"))

# ---------------------------------------------------------------------------
# DPI for pdf2image conversion (higher = better OCR accuracy, slower)
# ---------------------------------------------------------------------------
OCR_DPI: int = int(os.environ.get("OCR_DPI", "300"))
