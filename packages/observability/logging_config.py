"""Structured logging configuration — JSON output on Cloud Run,
human-readable locally.

Detects Cloud Run environment via the K_SERVICE env var (auto-set by
Cloud Run on every container). On Cloud Run, formats stdlib logging
records as JSON with a `severity` field that Cloud Logging
auto-extracts into its severity levels. Locally (no K_SERVICE), the
formatter falls back to a standard human-readable one-liner.

Logging convention going forward:
    logger.info("...", extra={"prospect_id": ..., "status": ...})
Custom fields land in jsonPayload.extra.* in Cloud Logging, enabling
per-prospect log queries and aggregation by status.
"""
import json
import logging
import os
import sys
from typing import Any


IS_CLOUD_RUN = bool(os.environ.get("K_SERVICE"))


class CloudLoggingFormatter(logging.Formatter):
    """JSON formatter compatible with Cloud Logging's structured-log
    auto-extraction. Cloud Logging maps the top-level `severity` field
    to its severity levels automatically."""

    SEVERITY_MAP = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL",
    }

    STANDARD_FIELDS = {
        "name", "msg", "args", "levelname", "levelno", "pathname",
        "filename", "module", "exc_info", "exc_text", "stack_info",
        "lineno", "funcName", "created", "msecs", "relativeCreated",
        "thread", "threadName", "processName", "process", "message",
        "taskName",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "severity": self.SEVERITY_MAP.get(record.levelno, "DEFAULT"),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        extra = {
            k: v for k, v in record.__dict__.items()
            if k not in self.STANDARD_FIELDS
        }
        if extra:
            payload["extra"] = extra

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_logging(service_name: str = "matta-refinery", level: int = logging.INFO) -> None:
    """Configure root logger. Called once at service startup."""
    root = logging.getLogger()
    root.setLevel(level)

    for handler in root.handlers[:]:
        root.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)

    if IS_CLOUD_RUN:
        handler.setFormatter(CloudLoggingFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))

    root.addHandler(handler)

    class _ServiceNameFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record.service = service_name
            return True

    handler.addFilter(_ServiceNameFilter())

    # Tame noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("celery.utils.functional").setLevel(logging.WARNING)
    logging.getLogger("kombu.connection").setLevel(logging.WARNING)
