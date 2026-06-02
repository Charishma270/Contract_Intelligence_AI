"""
OCR Configuration
==================
Day 14: Externalized OCR settings with environment variable overrides.
Day 20: Delegates to centralized backend.config settings.

All constants can be overridden via environment variables prefixed with OCR_.
"""

from backend.config import Settings

# Create fresh settings instance so environment-variable overrides
# are reloaded when this module is reloaded in tests.
_config = Settings()

# ---------------------------------------------------------------------------
# Tesseract / Poppler paths
# ---------------------------------------------------------------------------
POPPLER_PATH: str = _config.OCR_POPPLER_PATH

TESSERACT_CMD: str = _config.OCR_TESSERACT_CMD

# ---------------------------------------------------------------------------
# Extraction thresholds
# ---------------------------------------------------------------------------
# Minimum characters per page from pdfplumber before falling back to Tesseract.
# If pdfplumber extracts fewer chars than this, the page is considered
# "scanned" and Tesseract OCR is used instead.
MIN_TEXT_LENGTH: int = _config.OCR_MIN_TEXT_LENGTH

# ---------------------------------------------------------------------------
# Chunking parameters
# ---------------------------------------------------------------------------
CHUNK_SIZE: int = _config.OCR_CHUNK_SIZE
CHUNK_OVERLAP: int = _config.OCR_CHUNK_OVERLAP

# ---------------------------------------------------------------------------
# DPI for pdf2image conversion (higher = better OCR accuracy, slower)
# ---------------------------------------------------------------------------
OCR_DPI: int = _config.OCR_DPI