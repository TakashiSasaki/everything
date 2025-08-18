# Everything CLI Tools

This project provides command-line interface (CLI) tools to interact with the Everything search engine, leveraging its DLL, `es.exe` (command-line utility), and HTTP API.

## Features

- **`everything-dll`**: Interact with Everything via its DLL for fast, direct searches.
- **`everything-es`**: Utilize the `es.exe` command-line tool for searches.
- **`everything-http`**: Connect to the Everything HTTP server for remote or local searches.
- **Flexible Output**: Get search results in plain text or JSON format.
- **CSV Output (`everything-es`)**: Export and parse CSV via `--csv` (JSON uses CSV internally).
- **Test Mode**: Built-in connectivity tests for each method.

## Requirements

- **Python**: 3.9+ (see `pyproject.toml`).
- **Everything Search Engine**: Installed on Windows.
- **`es.exe`**: For `everything-es`, ensure `es.exe` is available in one of: PATH, `pyeverything/bin`, or the current directory.
- **Everything DLL**: For `everything-dll`, ensure `Everything64.dll` (for 64-bit Python) or `Everything32.dll` (for 32-bit Python) is available in one of: `pyeverything/bin`, the current directory, or PATH. This repo includes `pyeverything/bin/Everything64.dll`.
- **Everything HTTP Server**: For `everything-http`, the Everything HTTP server must be running and accessible (see notes below).

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. If you don't have Poetry installed, follow their official installation guide.

1. **Clone the repository:**
   ```bash
   git clone <your repo URL>
   cd <repo folder>
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```
   If `poetry` is not on PATH, use `python -m poetry install`.

3. **(Optional) Activate the virtual environment:**
   ```bash
   poetry shell
   ```
   You can also run commands directly using `poetry run <command>`. For example, `poetry run everything-dll --help`.

## Usage

Each tool can be run using `poetry run <tool-name>`. Use the `--help` flag for detailed options.

### `everything-dll`

Interacts directly with the Everything DLL.

```bash
poetry run everything-dll --help
poetry run everything-dll --search "your query" --json
poetry run everything-dll --test
```

Notes:
- DLL lookup order: `pyeverything/bin` → current directory → PATH.
- Use `Everything64.dll` with 64‑bit Python and `Everything32.dll` with 32‑bit Python.

### `everything-es`

Uses the `es.exe` command-line utility.

```bash
poetry run everything-es --help
poetry run everything-es --search "your query" --all-fields
poetry run everything-es --search "your query" --csv
poetry run everything-es --search "your query" --json --all-fields
poetry run everything-es --test
```

Notes:
- `--json` uses CSV export under the hood for accurate parsing.
- `es.exe` lookup order: PATH → `pyeverything/bin` → current directory.

### `everything-http`

Connects to the Everything HTTP server.

```bash
poetry run everything-http --help
poetry run everything-http --search "your query" --host 127.0.0.1 --port 8080 --json
poetry run everything-http --test
```

HTTP server notes:
- Enable in Everything via: Tools → Options → HTTP Server.
- Default port is 80 unless changed.
- Configure via flags (`--host`, `--port`) or `.env`.

### Environment Variables (for `everything-http`)

You can configure the HTTP host and port using a `.env` file in the project root:

```
EVERYTHING_HOST=127.0.0.1
EVERYTHING_PORT=80
```

## Python API (optional)

You can use the `Everything` class directly from Python:

```python
from pyeverything.everything import Everything

ev = Everything()
results = ev.search("your query", count=10, all_fields=True)
print(results)
```

## Running Tests

Install dev dependencies and run tests:

```bash
poetry install --with dev
poetry run pytest
```

Notes:
- Tests are in the `tests/` directory.
- Some tests (especially integration) require Windows and a running Everything instance (and, for HTTP, the HTTP server enabled).

### What `poetry run pytest` does

- Executes `pytest` inside Poetry’s virtual environment for this project; it does not install dependencies by itself.
- Uses `pyproject.toml` to identify the project and environment. This repo includes Poetry config sections: `[tool.poetry]`, `[tool.poetry.dependencies]`, `[tool.poetry.group.dev.dependencies]`, `[tool.poetry.scripts]`, and `[build-system]`.
- `pytest` discovers tests using its defaults (here, the `tests/` folder) since there is no pytest-specific config in `pyproject.toml`.

Common outcomes and fixes:
- If `pytest` is missing: run `poetry install --with dev` (or `python -m poetry install --with dev` on Windows if `poetry` isn’t on PATH).
- If integration tests fail: they may require Windows and a running Everything/HTTP server. Run a subset instead, e.g. `poetry run pytest tests/test_*.py`.
- If no venv exists: Poetry will create/select one, but dev dependencies are only installed when you run `poetry install --with dev`.

Quick sequence:
```bash
poetry install --with dev
poetry run pytest
```
