"""JSON configuration models and parse-plus-validation helpers."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from copilot_for_python.errors import ConfigError


class _StrictConfigModel(BaseModel):
    """Base configuration model that rejects unknown fields and coercion."""

    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)


class RuntimeConfig(_StrictConfigModel):
    """Validated runtime settings loaded from JSON."""

    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    enable_logging: bool = True

    @field_validator("host")
    @classmethod
    def host_must_not_be_empty(cls, value: str) -> str:
        if not value or any(ord(character) < 32 for character in value):
            raise ValueError(
                "host must be a non-empty string without control characters"
            )
        return value


def _validation_message(error: ValidationError) -> str:
    details = "; ".join(
        f"{'.'.join(str(part) for part in issue['loc']) or 'config'}: {issue['msg']}"
        for issue in error.errors(include_url=False)
    )
    return details or "configuration is invalid"


def parse_runtime_config(data: Any) -> RuntimeConfig:
    """Parse a decoded JSON value and validate runtime settings."""
    try:
        return RuntimeConfig.model_validate(data)
    except ValidationError as error:
        message = _validation_message(error)
        raise ConfigError(f"Invalid runtime configuration: {message}") from error


def _load_json(path: str | Path) -> Any:
    config_path = Path(path)
    try:
        with config_path.open(encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError as error:
        raise ConfigError(f"Configuration file not found: {config_path}") from error
    except (OSError, UnicodeDecodeError) as error:
        message = f"Cannot read configuration file {config_path}: {error}"
        raise ConfigError(message) from error
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"Invalid JSON in {config_path} at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error


def load_runtime_config(path: str | Path) -> RuntimeConfig:
    """Read and validate a runtime JSON config file."""
    return parse_runtime_config(_load_json(path))
