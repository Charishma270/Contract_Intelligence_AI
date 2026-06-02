"""
OCR Configuration
==================
Day 14: Externalized OCR settings with environment variable overrides.
Day 20: Delegates to centralized backend.config.settings.

All constants can be overridden via environment variables prefixed with OCR_.
"""

from backend.config import settings


# ---------------------------------------------------------------------------
# Tesseract / Poppler paths
# ---------------------------------------------------------------------------
POPPLER_PATH: str = settings.OCR_POPPLER_PATH

TESSERACT_CMD: str = settings.OCR_TESSERACT_CMD

# ---------------------------------------------------------------------------
# Extraction thresholds
# ---------------------------------------------------------------------------
# Minimum characters per page from pdfplumber before falling back to Tesseract.
# If pdfplumber extracts fewer chars than this, the page is considered
# "scanned" and Tesseract OCR is used instead.
MIN_TEXT_LENGTH: int = settings.OCR_MIN_TEXT_LENGTH

# ---------------------------------------------------------------------------
# Chunking parameters
# ---------------------------------------------------------------------------
CHUNK_SIZE: int = settings.OCR_CHUNK_SIZE
CHUNK_OVERLAP: int = settings.OCR_CHUNK_OVERLAP

# ---------------------------------------------------------------------------
# DPI for pdf2image conversion (higher = better OCR accuracy, slower)
# ---------------------------------------------------------------------------
OCR_DPI: int = settings.OCR_DPI
