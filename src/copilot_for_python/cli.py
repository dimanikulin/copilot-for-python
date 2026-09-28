"""Command-line interface for copilot-for-python."""

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from copilot_for_python.config import load_runtime_config
from copilot_for_python.errors import CopilotForPythonError
from copilot_for_python.logging_config import configure_logging

_LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Validate JSON runtime configuration for a Python application."
    )
    parser.add_argument("--verbose", action="store_true", help="enable debug logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate a JSON runtime config"
    )
    validate_parser.add_argument(
        "--config", required=True, type=Path, help="path to the JSON config file"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run a CLI command and return its process exit status."""
    args = build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)

    try:
        config = load_runtime_config(args.config)
        configure_logging(enabled=config.enable_logging, verbose=args.verbose)
        logging_state = "enabled" if config.enable_logging else "disabled"
        print(
            f"Configuration valid: host={config.host}, port={config.port}, "
            f"logging={logging_state}"
        )
        return 0
    except CopilotForPythonError as error:
        _LOGGER.error("%s", error)
        return 2
