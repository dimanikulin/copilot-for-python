"""Logging configuration for the configuration-validator CLI."""

import logging
import sys


def configure_logging(*, enabled: bool = True, verbose: bool = False) -> None:
    """Configure concise stderr logging without replacing application handlers."""
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        root_logger.addHandler(handler)
    if not enabled:
        root_logger.setLevel(logging.CRITICAL + 1)
    else:
        root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
