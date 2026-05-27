"""
NLP Configuration
==================
Day 15: Configuration constants for the real NLP service.
Mirrors the pattern established by ocr_config.py on Day 14.
"""

import os

# ---------------------------------------------------------------------------
# Model Paths (relative to project root)
# ---------------------------------------------------------------------------
MULTILABEL_MODEL_PATH = os.environ.get(
    "NLP_MULTILABEL_MODEL_PATH",
    "models/legal_bert_multilabel/trained_model",
)

MULTILABEL_TOKENIZER_PATH = os.environ.get(
    "NLP_MULTILABEL_TOKENIZER_PATH",
    "models/legal_bert_multilabel/tokenizer",
)

LABEL_MAP_PATH = os.environ.get(
    "NLP_LABEL_MAP_PATH",
    "models/legal_bert_multilabel/label_mapping.json",
)

# ---------------------------------------------------------------------------
# Inference Settings
# ---------------------------------------------------------------------------
# Confidence threshold for multi-label clause detection.
# Labels with sigmoid probability >= this value are considered "present".
CONFIDENCE_THRESHOLD = float(os.environ.get("NLP_CONFIDENCE_THRESHOLD", "0.30"))

# Maximum sequence length for Legal-BERT tokenizer (must match training config).
MAX_SEQUENCE_LENGTH = 256

# Maximum number of OCR chunks to run through the classifier.
# Set to 0 or negative for unlimited.
MAX_CHUNKS_TO_PROCESS = int(os.environ.get("NLP_MAX_CHUNKS", "50"))

# ---------------------------------------------------------------------------
# spaCy NER Configuration
# ---------------------------------------------------------------------------
SPACY_MODEL = os.environ.get("NLP_SPACY_MODEL", "en_core_web_sm")

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
