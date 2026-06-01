"""
NLP Configuration
==================
Day 15: Configuration constants for the real NLP service.
Day 20: Delegates to centralized backend.config.settings.
"""

from backend.config import settings

# ---------------------------------------------------------------------------
# Model Paths (relative to project root)
# ---------------------------------------------------------------------------
MULTILABEL_MODEL_PATH = settings.NLP_MULTILABEL_MODEL_PATH

MULTILABEL_TOKENIZER_PATH = settings.NLP_MULTILABEL_TOKENIZER_PATH

LABEL_MAP_PATH = settings.NLP_LABEL_MAP_PATH

# ---------------------------------------------------------------------------
# Inference Settings
# ---------------------------------------------------------------------------
# Confidence threshold for multi-label clause detection.
# Labels with sigmoid probability >= this value are considered "present".
CONFIDENCE_THRESHOLD = settings.NLP_CONFIDENCE_THRESHOLD

# Maximum sequence length for Legal-BERT tokenizer (must match training config).
MAX_SEQUENCE_LENGTH = settings.NLP_MAX_SEQUENCE_LENGTH

# Maximum number of OCR chunks to run through the classifier.
# Set to 0 or negative for unlimited.
MAX_CHUNKS_TO_PROCESS = settings.NLP_MAX_CHUNKS

# ---------------------------------------------------------------------------
# spaCy NER Configuration
# ---------------------------------------------------------------------------
SPACY_MODEL = settings.NLP_SPACY_MODEL

# Mapping from spaCy entity labels → our schema entity types.
# Only these types are kept; everything else is discarded.
SPACY_ENTITY_MAP = {
    "ORG": "ORGANIZATION",
    "PERSON": "PERSON",
    "GPE": "JURISDICTION",      # Geopolitical entities → Jurisdiction
    "LOC": "JURISDICTION",      # Locations → Jurisdiction (fallback)
    "DATE": "DATE",
    "MONEY": "MONETARY_VALUE",
    "TIME": "DURATION",
    "CARDINAL": None,           # Discard plain numbers
    "ORDINAL": None,            # Discard ordinals
    "PERCENT": None,            # Discard percentages
}

