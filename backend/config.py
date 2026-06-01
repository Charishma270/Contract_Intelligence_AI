"""
Application Configuration
==========================
Day 20: Centralized configuration for the Contract Intelligence AI backend.

All settings are read from environment variables at instantiation time.
Each setting has a sensible default for local development.
For production, create a `.env` file or set env vars directly.

Usage:
    from backend.config import settings
    print(settings.APP_VERSION)
"""

import os
from typing import List


def _bool(value: str) -> bool:
    """Parse a boolean env var (case-insensitive)."""
    return value.strip().lower() in ("1", "true", "yes", "on")


def _list(value: str) -> List[str]:
    """Parse a comma-separated env var into a list of strings."""
    return [v.strip() for v in value.split(",") if v.strip()]


class Settings:
    """
    Application settings loaded from environment variables.

    Environment variables are read when __init__ is called, so creating
    a new Settings() after changing os.environ will pick up the changes.

    Grouped by concern:
      - App metadata
      - Server / CORS
      - File upload
      - Database
      - Logging
      - OCR
      - NLP
      - Celery / Redis
    """

    __slots__ = (
        "APP_NAME", "APP_VERSION", "APP_ENV", "DEBUG",
        "HOST", "PORT",
        "CORS_ORIGINS", "CORS_ALLOW_CREDENTIALS",
        "UPLOAD_DIR", "MAX_FILE_SIZE_MB",
        "DATABASE_DIR", "DATABASE_FILENAME",
        "LOG_LEVEL", "LOG_DIR", "LOG_FILENAME", "LOG_RETENTION_DAYS",
        "OCR_POPPLER_PATH", "OCR_TESSERACT_CMD",
        "OCR_MIN_TEXT_LENGTH", "OCR_CHUNK_SIZE", "OCR_CHUNK_OVERLAP",
        "OCR_DPI",
        "NLP_MULTILABEL_MODEL_PATH", "NLP_MULTILABEL_TOKENIZER_PATH",
        "NLP_LABEL_MAP_PATH", "NLP_CONFIDENCE_THRESHOLD",
        "NLP_MAX_SEQUENCE_LENGTH", "NLP_MAX_CHUNKS", "NLP_SPACY_MODEL",
        "CELERY_BROKER_URL", "CELERY_RESULT_BACKEND",
        "CELERY_WORKER_CONCURRENCY", "CELERY_TASK_TIME_LIMIT",
        "CELERY_TASK_SOFT_TIME_LIMIT", "CELERY_RESULT_EXPIRES",
    )

    def __init__(self) -> None:
        """Read all settings from environment variables (with defaults)."""

        # --- App Metadata ---
        self.APP_NAME: str = os.environ.get(
            "APP_NAME", "Contract Intelligence AI",
        )
        self.APP_VERSION: str = os.environ.get(
            "APP_VERSION", "0.6.0",
        )
        self.APP_ENV: str = os.environ.get(
            "APP_ENV", "development",
        )
        self.DEBUG: bool = _bool(os.environ.get(
            "DEBUG", "false",
        ))

        # --- Server ---
        self.HOST: str = os.environ.get(
            "HOST", "0.0.0.0",
        )
        self.PORT: int = int(os.environ.get(
            "PORT", "8000",
        ))

        # --- CORS ---
        self.CORS_ORIGINS: List[str] = _list(
            os.environ.get("CORS_ORIGINS", "*"),
        )
        self.CORS_ALLOW_CREDENTIALS: bool = _bool(os.environ.get(
            "CORS_ALLOW_CREDENTIALS", "true",
        ))

        # --- File Upload ---
        self.UPLOAD_DIR: str = os.environ.get(
            "UPLOAD_DIR", "uploads",
        )
        self.MAX_FILE_SIZE_MB: int = int(os.environ.get(
            "MAX_FILE_SIZE_MB", "20",
        ))

        # --- Database (SQLite) ---
        self.DATABASE_DIR: str = os.environ.get(
            "DATABASE_DIR", "data",
        )
        self.DATABASE_FILENAME: str = os.environ.get(
            "DATABASE_FILENAME", "contracts.db",
        )

        # --- Logging ---
        self.LOG_LEVEL: str = os.environ.get(
            "LOG_LEVEL", "INFO",
        ).upper()
        self.LOG_DIR: str = os.environ.get(
            "LOG_DIR", "logs",
        )
        self.LOG_FILENAME: str = os.environ.get(
            "LOG_FILENAME", "contract_ai.log",
        )
        self.LOG_RETENTION_DAYS: int = int(os.environ.get(
            "LOG_RETENTION_DAYS", "30",
        ))

        # --- OCR (Tesseract / pdfplumber) ---
        self.OCR_POPPLER_PATH: str = os.environ.get(
            "OCR_POPPLER_PATH",
            r"C:\poppler\poppler-26.02.0\Library\bin",
        )
        self.OCR_TESSERACT_CMD: str = os.environ.get(
            "OCR_TESSERACT_CMD",
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        )
        self.OCR_MIN_TEXT_LENGTH: int = int(os.environ.get(
            "OCR_MIN_TEXT_LENGTH", "50",
        ))
        self.OCR_CHUNK_SIZE: int = int(os.environ.get(
            "OCR_CHUNK_SIZE", "200",
        ))
        self.OCR_CHUNK_OVERLAP: int = int(os.environ.get(
            "OCR_CHUNK_OVERLAP", "50",
        ))
        self.OCR_DPI: int = int(os.environ.get(
            "OCR_DPI", "300",
        ))

        # --- NLP (Legal-BERT + spaCy) ---
        self.NLP_MULTILABEL_MODEL_PATH: str = os.environ.get(
            "NLP_MULTILABEL_MODEL_PATH",
            "models/legal_bert_multilabel/trained_model",
        )
        self.NLP_MULTILABEL_TOKENIZER_PATH: str = os.environ.get(
            "NLP_MULTILABEL_TOKENIZER_PATH",
            "models/legal_bert_multilabel/tokenizer",
        )
        self.NLP_LABEL_MAP_PATH: str = os.environ.get(
            "NLP_LABEL_MAP_PATH",
            "models/legal_bert_multilabel/label_mapping.json",
        )
        self.NLP_CONFIDENCE_THRESHOLD: float = float(os.environ.get(
            "NLP_CONFIDENCE_THRESHOLD", "0.30",
        ))
        self.NLP_MAX_SEQUENCE_LENGTH: int = int(os.environ.get(
            "NLP_MAX_SEQUENCE_LENGTH", "256",
        ))
        self.NLP_MAX_CHUNKS: int = int(os.environ.get(
            "NLP_MAX_CHUNKS", "50",
        ))
        self.NLP_SPACY_MODEL: str = os.environ.get(
            "NLP_SPACY_MODEL", "en_core_web_sm",
        )

        # --- Celery / Redis ---
        self.CELERY_BROKER_URL: str = os.environ.get(
            "CELERY_BROKER_URL", "redis://localhost:6379/0",
        )
        self.CELERY_RESULT_BACKEND: str = os.environ.get(
            "CELERY_RESULT_BACKEND", "redis://localhost:6379/1",
        )
        self.CELERY_WORKER_CONCURRENCY: int = int(os.environ.get(
            "CELERY_WORKER_CONCURRENCY", "2",
        ))
        self.CELERY_TASK_TIME_LIMIT: int = int(os.environ.get(
            "CELERY_TASK_TIME_LIMIT", "300",
        ))
        self.CELERY_TASK_SOFT_TIME_LIMIT: int = int(os.environ.get(
            "CELERY_TASK_SOFT_TIME_LIMIT", "240",
        ))
        self.CELERY_RESULT_EXPIRES: int = int(os.environ.get(
            "CELERY_RESULT_EXPIRES", "86400",
        ))

    # -------------------------------------------------------------------
    # Derived properties
    # -------------------------------------------------------------------
    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        """Max upload size in bytes, derived from MAX_FILE_SIZE_MB."""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    @property
    def DATABASE_PATH(self) -> str:
        """Full path to the SQLite database file."""
        return os.path.join(self.DATABASE_DIR, self.DATABASE_FILENAME)

    @property
    def DATABASE_URL(self) -> str:
        """SQLAlchemy connection string for the SQLite database."""
        return f"sqlite:///{self.DATABASE_PATH}"

    @property
    def LOG_PATH(self) -> str:
        """Full path to the log file."""
        return os.path.join(self.LOG_DIR, self.LOG_FILENAME)

    def summary(self) -> dict:
        """Return a dict of all settings for logging / debugging."""
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "app_env": self.APP_ENV,
            "debug": self.DEBUG,
            "host": self.HOST,
            "port": self.PORT,
            "cors_origins": self.CORS_ORIGINS,
            "upload_dir": self.UPLOAD_DIR,
            "max_file_size_mb": self.MAX_FILE_SIZE_MB,
            "database_path": self.DATABASE_PATH,
            "log_level": self.LOG_LEVEL,
            "log_path": self.LOG_PATH,
            "celery_broker": self.CELERY_BROKER_URL,
        }

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{name}={getattr(self, name)!r}"
            for name in self.__slots__
        )
        return f"Settings({fields})"


# ---------------------------------------------------------------------------
# Singleton instance — import this everywhere
# ---------------------------------------------------------------------------
settings = Settings()
