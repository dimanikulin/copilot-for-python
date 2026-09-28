# Plan: Production-Ready Python Configuration Validator

> Scope update: project generation, its template files, and the `generate` command were removed. The remaining service validates runtime JSON settings.

Maintain a local CLI that parses and validates JSON runtime configuration, reports errors clearly, and supports logging controls. Project skeleton generation is out of scope.

## Steps

1. **Configuration and errors — implemented**
   - Parse JSON and validate runtime settings together with Pydantic.
   - Validate host, port, and logging settings, rejecting unknown fields and coercion.
   - Provide actionable errors and standard-library logging without logging config contents.

2. **Project generation — removed from scope**
   - The project generator, template assets, and `generate` command were deleted.
   - The CLI retains only runtime JSON validation.

3. **Tests and documentation — implemented for runtime validation**
   - Test valid and invalid config parsing, CLI behavior, and error reporting.
   - Document runtime configuration and validation usage in the README.

4. **CI and verification — completed**
   - Retain the current Python support floor and CI matrix.
   - CI runs lint, tests, source/wheel builds, and CLI entry-point smoke checks.
   - Local verification passed on Python 3.14; distribution contents exclude removed generator/template files.

## Relevant Existing Files

- `src/copilot_for_python/config.py` — Pydantic runtime settings and JSON loading.
- `src/copilot_for_python/cli.py` — `validate` command.
- `tests/test_config.py` and `tests/test_cli.py` — config and CLI tests.
- `pyproject.toml` — package and tool configuration.
- `.github/workflows/ci.yml` — CI checks.
- `README.md` — runtime config and CLI instructions.

## Decisions

- JSON config with Pydantic validation.
- Runtime config covers `host`, `port`, and `enable_logging`; no HTTP server is started.
- Project skeleton generation and template assets are out of scope.
- Preserve the existing LICENSE and Python support claims.
