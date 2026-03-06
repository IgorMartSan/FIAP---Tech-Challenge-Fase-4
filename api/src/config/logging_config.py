import json
import logging
import os
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": os.getenv("SERVICE_NAME", "defasagem_api"),
        }

        for key in ("event", "model_version", "latency_ms", "risk_class", "risk_probability", "features"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        return json.dumps(payload, ensure_ascii=False)


class LogConfig:
    def __init__(self, level: str | None = None) -> None:
        self.level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()

    def configure(self) -> None:
        root = logging.getLogger()
        root.setLevel(self.level)

        if root.handlers:
            root.handlers.clear()

        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        root.addHandler(handler)
