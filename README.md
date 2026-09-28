# copilot-for-python

A small CLI for parsing and validating JSON runtime configuration.

## Requirements

- Python 3.10 or newer
- pip

## Set up

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Validate a config

Create a JSON file such as `config.json`:

```json
{
	"host": "127.0.0.1",
	"port": 8000,
	"enable_logging": true
}
```

Supported fields and defaults:

- `host`: non-empty string, default `127.0.0.1`.
- `port`: integer from 1 to 65535, default `8000`.
- `enable_logging`: boolean, default `true`.

All fields are optional. Unknown fields and values of the wrong type are rejected.

Then validate it with:

```powershell
copilot-for-python validate --config config.json
# Or use the module entry point:
python -m copilot_for_python validate --config config.json
```

Expected configuration errors are logged to stderr and return exit status 2. The
`enable_logging` setting controls application log output; `--verbose` enables debug
logging when logging is enabled. This CLI validates settings; it does not start a
network server.

## Test and lint

```powershell
pytest
ruff check .
```
