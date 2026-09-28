"""Tests for the command-line interface."""

import json

from copilot_for_python.cli import main


def test_validate_command_reports_valid_config(tmp_path, capsys) -> None:
    config_path = tmp_path / "runtime.json"
    config_path.write_text(
        json.dumps({"host": "localhost", "port": 8080, "enable_logging": True}),
        encoding="utf-8",
    )

    assert main(["validate", "--config", str(config_path)]) == 0
    assert "Configuration valid: host=localhost, port=8080" in capsys.readouterr().out


def test_command_returns_nonzero_for_invalid_configuration(tmp_path, caplog) -> None:
    config_path = tmp_path / "runtime.json"
    config_path.write_text('{"port": 70000}', encoding="utf-8")

    assert main(["validate", "--config", str(config_path)]) == 2
    assert "Invalid runtime configuration" in caplog.text


def test_command_returns_nonzero_for_missing_configuration(tmp_path, caplog) -> None:
    assert main(["validate", "--config", str(tmp_path / "missing.json")]) == 2
    assert "Configuration file not found" in caplog.text
