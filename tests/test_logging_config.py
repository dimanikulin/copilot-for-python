"""Tests for application logging setup."""

import logging

import pytest

from copilot_for_python.logging_config import configure_logging


@pytest.fixture
def restore_root_logger():
    root_logger = logging.getLogger()
    previous_level = root_logger.level
    previous_handlers = root_logger.handlers[:]
    try:
        yield root_logger
    finally:
        root_logger.setLevel(previous_level)
        root_logger.handlers[:] = previous_handlers


def test_configure_logging_uses_debug_level_when_verbose(restore_root_logger) -> None:
    configure_logging(verbose=True)

    assert restore_root_logger.level == logging.DEBUG


def test_configure_logging_can_disable_output(restore_root_logger) -> None:
    configure_logging(enabled=False)

    assert restore_root_logger.level > logging.CRITICAL
