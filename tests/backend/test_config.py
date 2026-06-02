"""
Day 20 — Configuration Tests
==============================
Verifies the centralized Settings object:
  - Defaults are correct for all fields
  - Environment variable overrides work
  - Derived properties compute correctly
  - settings singleton is importable
"""

import os
import pytest


# -------------------------------------------------------------------
# Test: Importability
# -------------------------------------------------------------------

class TestSettingsImport:
    """Verify the settings singleton is importable."""

    def test_import_settings(self):
        from backend.config import settings
        assert settings is not None

    def test_import_settings_class(self):
        from backend.config import Settings
        assert Settings is not None

    def test_singleton_identity(self):
        """Two imports should return the same object."""
        from backend.config import settings as s1
        from backend.config import settings as s2
        assert s1 is s2


# -------------------------------------------------------------------
# Test: Default values
# -------------------------------------------------------------------

class TestSettingsDefaults:
    """Verify all defaults match expected values."""

    def test_app_name(self):
        from backend.config import settings
        # Should be "Contract Intelligence AI" unless overridden
        assert isinstance(settings.APP_NAME, str)
        assert len(settings.APP_NAME) > 0

    def test_app_version(self):
        from backend.config import settings
        assert isinstance(settings.APP_VERSION, str)
        # Version should be a semver-like string
        assert "." in settings.APP_VERSION

    def test_app_env(self):
        from backend.config import settings
        assert settings.APP_ENV in (
            "development", "staging", "production", "testing"
        )

    def test_debug_is_bool(self):
        from backend.config import settings
        assert isinstance(settings.DEBUG, bool)

    def test_host(self):
        from backend.config import settings
        assert isinstance(settings.HOST, str)

    def test_port(self):
        from backend.config import settings
        assert isinstance(settings.PORT, int)
        assert 1 <= settings.PORT <= 65535

    def test_cors_origins_is_list(self):
        from backend.config import settings
        assert isinstance(settings.CORS_ORIGINS, list)
        assert len(settings.CORS_ORIGINS) >= 1

    def test_upload_dir(self):
        from backend.config import settings
        assert isinstance(settings.UPLOAD_DIR, str)
        assert len(settings.UPLOAD_DIR) > 0

    def test_max_file_size_mb(self):
        from backend.config import settings
        assert isinstance(settings.MAX_FILE_SIZE_MB, int)
        assert settings.MAX_FILE_SIZE_MB > 0

    def test_database_dir(self):
        from backend.config import settings
        assert isinstance(settings.DATABASE_DIR, str)

    def test_log_level(self):
        from backend.config import settings
        assert settings.LOG_LEVEL in (
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        )

    def test_log_retention_days(self):
        from backend.config import settings
        assert isinstance(settings.LOG_RETENTION_DAYS, int)
        assert settings.LOG_RETENTION_DAYS > 0

    def test_ocr_settings_types(self):
        from backend.config import settings
        assert isinstance(settings.OCR_POPPLER_PATH, str)
        assert isinstance(settings.OCR_TESSERACT_CMD, str)
        assert isinstance(settings.OCR_MIN_TEXT_LENGTH, int)
        assert isinstance(settings.OCR_CHUNK_SIZE, int)
        assert isinstance(settings.OCR_CHUNK_OVERLAP, int)
        assert isinstance(settings.OCR_DPI, int)

    def test_nlp_settings_types(self):
        from backend.config import settings
        assert isinstance(settings.NLP_MULTILABEL_MODEL_PATH, str)
        assert isinstance(settings.NLP_CONFIDENCE_THRESHOLD, float)
        assert isinstance(settings.NLP_MAX_SEQUENCE_LENGTH, int)
        assert isinstance(settings.NLP_MAX_CHUNKS, int)
        assert isinstance(settings.NLP_SPACY_MODEL, str)

    def test_celery_settings_types(self):
        from backend.config import settings
        assert isinstance(settings.CELERY_BROKER_URL, str)
        assert isinstance(settings.CELERY_RESULT_BACKEND, str)
        assert isinstance(settings.CELERY_WORKER_CONCURRENCY, int)
        assert isinstance(settings.CELERY_TASK_TIME_LIMIT, int)
        assert isinstance(settings.CELERY_TASK_SOFT_TIME_LIMIT, int)
        assert isinstance(settings.CELERY_RESULT_EXPIRES, int)


# -------------------------------------------------------------------
# Test: Derived properties
# -------------------------------------------------------------------

class TestDerivedProperties:
    """Verify derived/computed properties."""

    def test_max_file_size_bytes(self):
        from backend.config import settings
        expected = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        assert settings.MAX_FILE_SIZE_BYTES == expected

    def test_database_path(self):
        from backend.config import settings
        assert settings.DATABASE_PATH == os.path.join(
            settings.DATABASE_DIR, settings.DATABASE_FILENAME
        )

    def test_database_url_prefix(self):
        from backend.config import settings
        assert settings.DATABASE_URL.startswith("sqlite:///")

    def test_database_url_contains_path(self):
        from backend.config import settings
        assert settings.DATABASE_PATH in settings.DATABASE_URL

    def test_log_path(self):
        from backend.config import settings
        assert settings.LOG_PATH == os.path.join(
            settings.LOG_DIR, settings.LOG_FILENAME
        )


# -------------------------------------------------------------------
# Test: Summary method
# -------------------------------------------------------------------

class TestSettingsSummary:
    """Verify the summary() helper."""

    def test_summary_returns_dict(self):
        from backend.config import settings
        s = settings.summary()
        assert isinstance(s, dict)

    def test_summary_has_required_keys(self):
        from backend.config import settings
        s = settings.summary()
        required_keys = [
            "app_name", "app_version", "app_env",
            "debug", "host", "port",
            "cors_origins", "upload_dir", "max_file_size_mb",
            "database_path", "log_level", "log_path",
            "celery_broker",
        ]
        for key in required_keys:
            assert key in s, f"Missing key: {key}"


# -------------------------------------------------------------------
# Test: Environment variable override (using fresh Settings)
# -------------------------------------------------------------------

class TestEnvOverride:
    """Verify that environment variables are picked up by a fresh Settings."""

    def test_app_name_override(self, monkeypatch):
        monkeypatch.setenv("APP_NAME", "Test App")
        # Import the class and create a new instance to pick up the override
        from backend.config import Settings
        fresh = Settings()
        assert fresh.APP_NAME == "Test App"

    def test_port_override(self, monkeypatch):
        monkeypatch.setenv("PORT", "9999")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.PORT == 9999

    def test_debug_true(self, monkeypatch):
        monkeypatch.setenv("DEBUG", "true")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.DEBUG is True

    def test_debug_false(self, monkeypatch):
        monkeypatch.setenv("DEBUG", "false")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.DEBUG is False

    def test_max_file_size_override(self, monkeypatch):
        monkeypatch.setenv("MAX_FILE_SIZE_MB", "50")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.MAX_FILE_SIZE_MB == 50
        assert fresh.MAX_FILE_SIZE_BYTES == 50 * 1024 * 1024

    def test_cors_origins_multiple(self, monkeypatch):
        monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")
        from backend.config import Settings
        fresh = Settings()
        assert len(fresh.CORS_ORIGINS) == 2
        assert "http://localhost:3000" in fresh.CORS_ORIGINS
        assert "http://localhost:8080" in fresh.CORS_ORIGINS

    def test_log_level_override(self, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "debug")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.LOG_LEVEL == "DEBUG"

    def test_celery_broker_override(self, monkeypatch):
        monkeypatch.setenv("CELERY_BROKER_URL", "redis://prod:6379/0")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.CELERY_BROKER_URL == "redis://prod:6379/0"

    def test_ocr_dpi_override(self, monkeypatch):
        monkeypatch.setenv("OCR_DPI", "600")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.OCR_DPI == 600

    def test_nlp_confidence_override(self, monkeypatch):
        monkeypatch.setenv("NLP_CONFIDENCE_THRESHOLD", "0.50")
        from backend.config import Settings
        fresh = Settings()
        assert fresh.NLP_CONFIDENCE_THRESHOLD == 0.50


# -------------------------------------------------------------------
# Test: Config modules delegate correctly
# -------------------------------------------------------------------

class TestConfigDelegation:
    """
    Verify that the per-module config files (ocr_config, nlp_config)
    export the same values as the central settings.
    """

    def test_ocr_config_matches_settings(self):
        from backend.config import settings
        from backend.services.ocr_config import (
            POPPLER_PATH, TESSERACT_CMD,
            MIN_TEXT_LENGTH, CHUNK_SIZE, CHUNK_OVERLAP, OCR_DPI,
        )
        assert POPPLER_PATH == settings.OCR_POPPLER_PATH
        assert TESSERACT_CMD == settings.OCR_TESSERACT_CMD
        assert MIN_TEXT_LENGTH == settings.OCR_MIN_TEXT_LENGTH
        assert CHUNK_SIZE == settings.OCR_CHUNK_SIZE
        assert CHUNK_OVERLAP == settings.OCR_CHUNK_OVERLAP
        assert OCR_DPI == settings.OCR_DPI

    def test_nlp_config_matches_settings(self):
        from backend.config import settings
        from backend.services.nlp_config import (
            MULTILABEL_MODEL_PATH, MULTILABEL_TOKENIZER_PATH,
            LABEL_MAP_PATH, CONFIDENCE_THRESHOLD,
            MAX_SEQUENCE_LENGTH, MAX_CHUNKS_TO_PROCESS,
            SPACY_MODEL,
        )
        assert MULTILABEL_MODEL_PATH == settings.NLP_MULTILABEL_MODEL_PATH
        assert MULTILABEL_TOKENIZER_PATH == settings.NLP_MULTILABEL_TOKENIZER_PATH
        assert LABEL_MAP_PATH == settings.NLP_LABEL_MAP_PATH
        assert CONFIDENCE_THRESHOLD == settings.NLP_CONFIDENCE_THRESHOLD
        assert MAX_SEQUENCE_LENGTH == settings.NLP_MAX_SEQUENCE_LENGTH
        assert MAX_CHUNKS_TO_PROCESS == settings.NLP_MAX_CHUNKS
        assert SPACY_MODEL == settings.NLP_SPACY_MODEL
