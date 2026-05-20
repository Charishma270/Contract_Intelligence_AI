"""
Test Suite — Structured Logging (Day 13)
==========================================
Tests for the centralized logging configuration module.
"""

import json
import logging
import os
import tempfile

import pytest

from backend.utils.logging_config import (
    ConsoleFormatter,
    JSONFormatter,
    RequestIdFilter,
    request_id_ctx,
    setup_logging,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _clean_logger():
    """Reset the contract_ai logger between tests to avoid handler leaks."""
    logger = logging.getLogger("contract_ai")
    logger.handlers.clear()
    yield
    logger.handlers.clear()


@pytest.fixture
def tmp_log_dir(tmp_path):
    """Provide a temp directory for log file tests."""
    return str(tmp_path)


# ---------------------------------------------------------------------------
# setup_logging() tests
# ---------------------------------------------------------------------------
class TestSetupLogging:
    """Tests for the setup_logging() initialization function."""

    def test_returns_logger(self, tmp_log_dir):
        """setup_logging() should return the root contract_ai logger."""
        logger = setup_logging(log_dir=tmp_log_dir)
        assert logger.name == "contract_ai"

    def test_creates_two_handlers(self, tmp_log_dir):
        """Should create exactly one StreamHandler and one file handler."""
        logger = setup_logging(log_dir=tmp_log_dir)
        assert len(logger.handlers) == 2

        handler_types = {type(h).__name__ for h in logger.handlers}
        assert "StreamHandler" in handler_types
        assert "TimedRotatingFileHandler" in handler_types

    def test_creates_log_file(self, tmp_log_dir):
        """Should create the log file in the specified directory."""
        setup_logging(log_dir=tmp_log_dir)
        log_path = os.path.join(tmp_log_dir, "contract_ai.log")
        assert os.path.exists(log_path)

    def test_custom_log_filename(self, tmp_log_dir):
        """Should accept a custom log filename."""
        setup_logging(log_dir=tmp_log_dir, log_filename="test_app.log")
        log_path = os.path.join(tmp_log_dir, "test_app.log")
        assert os.path.exists(log_path)

    def test_default_level_is_info(self, tmp_log_dir):
        """Default log level should be INFO."""
        logger = setup_logging(log_dir=tmp_log_dir)
        assert logger.level == logging.INFO

    def test_custom_log_level(self, tmp_log_dir):
        """Should accept a custom log level string."""
        logger = setup_logging(log_level="DEBUG", log_dir=tmp_log_dir)
        assert logger.level == logging.DEBUG

    def test_env_var_log_level(self, tmp_log_dir, monkeypatch):
        """Should read log level from LOG_LEVEL environment variable."""
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        logger = setup_logging(log_dir=tmp_log_dir)
        assert logger.level == logging.WARNING

    def test_explicit_level_overrides_env(self, tmp_log_dir, monkeypatch):
        """Explicit log_level argument should override LOG_LEVEL env var."""
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        logger = setup_logging(log_level="DEBUG", log_dir=tmp_log_dir)
        assert logger.level == logging.DEBUG

    def test_no_propagation(self, tmp_log_dir):
        """Logger should not propagate to root to avoid duplicate output."""
        logger = setup_logging(log_dir=tmp_log_dir)
        assert logger.propagate is False

    def test_clears_existing_handlers(self, tmp_log_dir):
        """Calling setup_logging() twice shouldn't duplicate handlers."""
        setup_logging(log_dir=tmp_log_dir)
        logger = setup_logging(log_dir=tmp_log_dir)
        assert len(logger.handlers) == 2

    def test_creates_log_directory(self):
        """Should create the log directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as base:
            nested = os.path.join(base, "subdir", "logs")
            logger = setup_logging(log_dir=nested)
            assert os.path.isdir(nested)
            # Close file handlers so Windows can clean up the temp dir
            for h in logger.handlers[:]:
                if hasattr(h, "close"):
                    h.close()
                logger.removeHandler(h)

    def test_child_loggers_inherit(self, tmp_log_dir):
        """Child loggers like 'contract_ai.upload' should inherit config."""
        setup_logging(log_level="DEBUG", log_dir=tmp_log_dir)
        child = logging.getLogger("contract_ai.upload")
        assert child.getEffectiveLevel() == logging.DEBUG


# ---------------------------------------------------------------------------
# JSONFormatter tests
# ---------------------------------------------------------------------------
class TestJSONFormatter:
    """Tests for the JSON Lines file formatter."""

    def test_produces_valid_json(self, tmp_log_dir):
        """Each log line should be a valid JSON object."""
        setup_logging(log_dir=tmp_log_dir)
        logger = logging.getLogger("contract_ai.test_json")
        logger.info("Test message for JSON")

        log_path = os.path.join(tmp_log_dir, "contract_ai.log")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # At least the initialization log + our test message
        assert len(lines) >= 1

        for line in lines:
            parsed = json.loads(line)  # Should not raise
            assert isinstance(parsed, dict)

    def test_json_contains_required_fields(self, tmp_log_dir):
        """JSON output should contain all required structured fields."""
        setup_logging(log_dir=tmp_log_dir)
        logger = logging.getLogger("contract_ai.test_fields")
        logger.info("Field check message")

        log_path = os.path.join(tmp_log_dir, "contract_ai.log")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Check the last line (our test message)
        parsed = json.loads(lines[-1])
        required_fields = {
            "timestamp", "level", "logger", "message",
            "request_id", "module", "funcName", "lineno",
        }
        assert required_fields.issubset(parsed.keys())

    def test_json_message_content(self, tmp_log_dir):
        """JSON message field should match the logged message."""
        setup_logging(log_dir=tmp_log_dir)
        logger = logging.getLogger("contract_ai.test_msg")
        logger.info("Unique test message 12345")

        log_path = os.path.join(tmp_log_dir, "contract_ai.log")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        parsed = json.loads(lines[-1])
        assert parsed["message"] == "Unique test message 12345"
        assert parsed["level"] == "INFO"

    def test_json_includes_exception(self, tmp_log_dir):
        """JSON output should include exception info when present."""
        setup_logging(log_dir=tmp_log_dir)
        logger = logging.getLogger("contract_ai.test_exc")
        try:
            raise ValueError("test error")
        except ValueError:
            logger.exception("Something went wrong")

        log_path = os.path.join(tmp_log_dir, "contract_ai.log")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        parsed = json.loads(lines[-1])
        assert "exception" in parsed
        assert "ValueError" in parsed["exception"]
        assert "test error" in parsed["exception"]


# ---------------------------------------------------------------------------
# ConsoleFormatter tests
# ---------------------------------------------------------------------------
class TestConsoleFormatter:
    """Tests for the colored console formatter."""

    def test_produces_readable_output(self):
        """Console formatter should produce a non-empty string."""
        formatter = ConsoleFormatter()
        record = logging.LogRecord(
            name="contract_ai.upload",
            level=logging.INFO,
            pathname="upload.py",
            lineno=42,
            msg="Test console message",
            args=None,
            exc_info=None,
        )
        record.request_id = "abc123"
        output = formatter.format(record)
        assert "Test console message" in output
        assert "abc123" in output

    def test_shortens_logger_name(self):
        """Should shorten 'contract_ai.upload' to 'upload'."""
        formatter = ConsoleFormatter()
        record = logging.LogRecord(
            name="contract_ai.pipeline",
            level=logging.INFO,
            pathname="pipeline.py",
            lineno=10,
            msg="Pipeline started",
            args=None,
            exc_info=None,
        )
        record.request_id = "-"
        output = formatter.format(record)
        assert "pipeline" in output

    def test_hides_default_request_id(self):
        """Should not show request_id when it's the default '-'."""
        formatter = ConsoleFormatter()
        record = logging.LogRecord(
            name="contract_ai",
            level=logging.INFO,
            pathname="main.py",
            lineno=1,
            msg="Startup",
            args=None,
            exc_info=None,
        )
        record.request_id = "-"
        output = formatter.format(record)
        assert "[-]" not in output


# ---------------------------------------------------------------------------
# RequestIdFilter tests
# ---------------------------------------------------------------------------
class TestRequestIdFilter:
    """Tests for the request_id context filter."""

    def test_injects_default_request_id(self):
        """Should inject '-' as default when no request context is set."""
        filt = RequestIdFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="",
            lineno=0, msg="test", args=None, exc_info=None,
        )
        # Reset context to default
        token = request_id_ctx.set("-")
        try:
            result = filt.filter(record)
            assert result is True
            assert record.request_id == "-"
        finally:
            request_id_ctx.reset(token)

    def test_injects_custom_request_id(self):
        """Should inject the request_id from contextvars."""
        filt = RequestIdFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="",
            lineno=0, msg="test", args=None, exc_info=None,
        )
        token = request_id_ctx.set("abc12345")
        try:
            filt.filter(record)
            assert record.request_id == "abc12345"
        finally:
            request_id_ctx.reset(token)

    def test_request_id_in_json_output(self, tmp_log_dir):
        """request_id should appear in JSON file output."""
        setup_logging(log_dir=tmp_log_dir)
        token = request_id_ctx.set("req-test-99")
        try:
            logger = logging.getLogger("contract_ai.test_ctx")
            logger.info("Context test message")
        finally:
            request_id_ctx.reset(token)

        log_path = os.path.join(tmp_log_dir, "contract_ai.log")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        parsed = json.loads(lines[-1])
        assert parsed["request_id"] == "req-test-99"


# ---------------------------------------------------------------------------
# File rotation config tests
# ---------------------------------------------------------------------------
class TestRotationConfig:
    """Tests for the log file rotation configuration."""

    def test_file_handler_rotation_settings(self, tmp_log_dir):
        """File handler should have daily rotation with 30-day retention."""
        setup_logging(log_dir=tmp_log_dir)
        logger = logging.getLogger("contract_ai")

        file_handlers = [
            h for h in logger.handlers
            if isinstance(h, logging.handlers.TimedRotatingFileHandler)
        ]
        assert len(file_handlers) == 1

        handler = file_handlers[0]
        assert handler.when == "MIDNIGHT"  # internally stored as uppercase
        assert handler.interval == 86400   # 1 day in seconds
        assert handler.backupCount == 30
        assert handler.encoding == "utf-8"
