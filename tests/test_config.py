"""Tests for JSON configuration parsing and validation."""

import pytest

from copilot_for_python.config import (
    RuntimeConfig,
    load_runtime_config,
    parse_runtime_config,
)
from copilot_for_python.errors import ConfigError


def test_runtime_config_has_documented_defaults() -> None:
    config = parse_runtime_config({})

    assert config.host == "127.0.0.1"
    assert config.port == 8000
    assert config.enable_logging is True


def test_parse_runtime_config_validates_port_and_types() -> None:
    assert parse_runtime_config({"host": "localhost", "port": 8080}).port == 8080

    with pytest.raises(ConfigError, match="port"):
        parse_runtime_config({"port": 65536})

    with pytest.raises(ConfigError, match="enable_logging"):
        parse_runtime_config({"enable_logging": "false"})


@pytest.mark.parametrize(
    "data",
    [
        {"host": ""},
        {"host": "invalid\nhost"},
        {"port": 0},
        {"port": True},
        {"unknown": "value"},
        [],
    ],
)
def test_parse_runtime_config_rejects_invalid_values(data) -> None:
    with pytest.raises(ConfigError):
        parse_runtime_config(data)


def test_load_runtime_config_parses_runtime_settings(tmp_path) -> None:
    config_path = tmp_path / "runtime.json"
    config_path.write_text(
        '{"host": "127.0.0.1", "port": 9000, "enable_logging": false}',
        encoding="utf-8",
    )

    config = load_runtime_config(config_path)

    assert isinstance(config, RuntimeConfig)
    assert config.port == 9000
    assert config.enable_logging is False


def test_load_config_reports_missing_and_malformed_files(tmp_path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        load_runtime_config(tmp_path / "missing.json")

    malformed_path = tmp_path / "malformed.json"
    malformed_path.write_text("{invalid", encoding="utf-8")
    with pytest.raises(ConfigError, match="Invalid JSON.*line 1"):
        load_runtime_config(malformed_path)
