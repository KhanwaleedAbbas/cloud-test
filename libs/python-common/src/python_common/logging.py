from __future__ import annotations

import logging
import os


def configure_logging(level: str | None = None) -> None:
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

