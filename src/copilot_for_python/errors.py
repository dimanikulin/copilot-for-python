"""Domain exceptions exposed by the configuration validator."""


class CopilotForPythonError(Exception):
    """Base exception for expected application errors."""


class ConfigError(CopilotForPythonError):
    """Raised when configuration cannot be read or fails validation."""
