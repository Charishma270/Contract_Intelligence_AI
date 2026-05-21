"""
Logging Configuration
======================
Day 13: Centralized structured logging for the Contract Intelligence AI backend.

Provides:
  - JSON-structured file output (daily rotating, 30-day retention)
  - Colored human-readable console output
  - Async-safe request-ID context propagation via contextvars
  - One-call setup_logging() initialization

Usage:
    from backend.utils.logging_config import setup_logging
    setup_logging()  # call once at startup
"""

import json
import logging
import logging.handlers
import os
import sys
from contextvars import ContextVar
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Request context — async-safe via contextvars
# ---------------------------------------------------------------------------
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

# ---------------------------------------------------------------------------
# ANSI color codes for console output
# ---------------------------------------------------------------------------
_COLORS = {
    "DEBUG": "\033[36m",     # Cyan
    "INFO": "\033[32m",      # Green
    "WARNING": "\033[33m",   # Yellow
    "ERROR": "\033[31m",     # Red
    "CRITICAL": "\033[1;31m",  # Bold Red
}
_RESET = "\033[0m"
_DIM = "\033[2m"
_BOLD = "\033[1m"


# ---------------------------------------------------------------------------
# Custom filter to inject request_id into every LogRecord
# ---------------------------------------------------------------------------
class RequestIdFilter(logging.Filter):
    """Injects the current request_id from contextvars into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get("-")
        return True


# ---------------------------------------------------------------------------
# JSON Formatter — machine-readable, one JSON object per line
# ---------------------------------------------------------------------------
class JSONFormatter(logging.Formatter):
    """
    Produces JSON Lines output suitable for log aggregation tools
    (ELK, Datadog, CloudWatch, etc.).

    Each line is a self-contained JSON object with fields:
        timestamp, level, logger, message, request_id, module, funcName, lineno
    Exception info is included as 'exception' when present.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }

        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


# ---------------------------------------------------------------------------
# Console Formatter — colored, human-readable
# ---------------------------------------------------------------------------
class ConsoleFormatter(logging.Formatter):
    """
    Colored, human-readable formatter for console/terminal output.

    Format: [timestamp] LEVEL    logger — message
    """

    def format(self, record: logging.LogRecord) -> str:
        color = _COLORS.get(record.levelname, "")
        request_id = getattr(record, "request_id", "-")

        # Pad level name for alignment
        level = record.levelname.ljust(8)

        # Shorten logger name: "contract_ai.pipeline" → "pipeline"
        short_name = record.name
        if short_name.startswith("contract_ai."):
            short_name = short_name[len("contract_ai."):]
        elif short_name == "contract_ai":
            short_name = "app"
        short_name = short_name.ljust(12)

        timestamp = datetime.fromtimestamp(
            record.created, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Build the formatted line
        parts = [
            f"{_DIM}{timestamp}{_RESET}",
            f"{color}{level}{_RESET}",
            f"{_DIM}{short_name}{_RESET}",
        ]

        # Show request_id if not the default placeholder
        if request_id and request_id != "-":
            parts.append(f"{_DIM}[{request_id}]{_RESET}")

        parts.append(f"— {record.getMessage()}")

        line = " ".join(parts)

        # Append exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            line += "\n" + self.formatException(record.exc_info)

        return line


# ---------------------------------------------------------------------------
# Setup function — call once at application startup
# ---------------------------------------------------------------------------
def setup_logging(
    log_level: str | None = None,
    log_dir: str = "logs",
    log_filename: str = "contract_ai.log",
) -> logging.Logger:
    """
    Configure the 'contract_ai' logger hierarchy with console + file handlers.

    Args:
        log_level: Logging level string (DEBUG/INFO/WARNING/ERROR/CRITICAL).
                   Falls back to LOG_LEVEL env var, then defaults to INFO.
        log_dir: Directory for log files (created if missing).
        log_filename: Name of the log file.

    Returns:
        The configured root 'contract_ai' logger.
    """
    # Resolve log level
    level_str = (log_level or os.environ.get("LOG_LEVEL", "INFO")).upper()
    level = getattr(logging, level_str, logging.INFO)

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_filename)

    # Get the root logger for our app hierarchy
    root_logger = logging.getLogger("contract_ai")
    root_logger.setLevel(level)

    # Clear any existing handlers (prevents duplicate handlers on reload)
    root_logger.handlers.clear()

    # Shared filter for request_id injection
    request_filter = RequestIdFilter()

    # --- Console handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ConsoleFormatter())
    console_handler.addFilter(request_filter)
    root_logger.addHandler(console_handler)

    # --- File handler (daily rotation, 30-day retention) ---
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_path,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(JSONFormatter())
    file_handler.addFilter(request_filter)
    file_handler.suffix = "%Y-%m-%d"
    root_logger.addHandler(file_handler)

    # Prevent propagation to root logger (avoids duplicate output)
    root_logger.propagate = False

    # Quiet noisy third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    root_logger.info(
        f"Logging initialized — level={level_str}, "
        f"file={log_path}, rotation=daily, retention=30d"
    )

    return root_logger
