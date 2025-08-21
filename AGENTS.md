# AGENTS

This document records working agreements and decisions made during the current session to guide future automation and contributions.

## Operating Mode

- Prefer running Codex CLI in `--full-auto` mode for maximum autonomy.
- For this repository, proceed autonomously in the current sandbox when a restart is not requested.

## Platform and DLL Policy

- Use only the 64‑bit Everything SDK DLL: `Everything64.dll`.
- DLL load order: package `pyeverything/bin/Everything64.dll` → current working directory → system `PATH`.
- Do not attempt to load or fallback to 32‑bit DLLs.

## es.exe Discovery Policy

- Primary resolution: `PATH` (via `shutil.which`).
- Fallbacks (in order):
  - Package bin: `pyeverything/bin/es.exe`
  - Current working directory: `./es.exe`
  - Repository local bin: `./bin/es.exe`
  - Common Windows installs: `C:\bin\es.exe`, `%ProgramFiles%\Everything\es.exe`, `%ProgramFiles(x86)%\Everything\es.exe`
- Error message reflects all checked locations so tests can assert precisely.

## Test Strategy

- Keep both unit and integration tests; they serve complementary purposes.
  - Unit tests: deterministic, mock‑driven, fast feedback for Python wrapper logic.
  - Integration tests: Windows‑only verification against the real Everything SDK (IPC, sorting, flags, indexing).
- Integration test environment requirements:
  - Run on Windows (`sys.platform == 'win32'`).
  - Ensure `pyeverything/bin/Everything64.dll` is present.
  - Everything service/index should be available; some tests may briefly wait or trigger index updates.
- Conventions validated by tests:
  - `pyeverything.everything.Everything.search()` returns items with separate `name` (basename) and `path` (directory path).
  - The DLL CLI (`python -m pyeverything.dll`) returns JSON entries where `path` contains the full path; tests match against a full‑path substring.
  - DLL can be loaded and queried for version info when IPC is available; otherwise tests skip with a clear message.
  - All documented DLL exports are bound in `init_functions` and verifiable via `verify_dll_bindings`.

## Integration Suites Added

- DLL CLI: `tests/test_integration_dll.py`
  - Windows‑only; requires `pyeverything/bin/Everything64.dll`.
  - Uses robust token queries (e.g., `windows system32 drivers etc hosts`) and relaxed full‑path substring checks.
- DLL load/version/bindings (step‑by‑step): `tests/test_integration_dll_steps.py`
  - `test_dll_file_exists_in_package_bin`: asserts `pyeverything/bin/Everything64.dll` exists.
  - `test_dll_loads_and_bindings_ok`: loads DLL, initializes ctypes signatures, and verifies all expected exports via `verify_dll_bindings`.
  - `test_ipc_available_or_skip`: detects IPC availability and skips with guidance if Everything is not running.
  - `test_version_info_when_ipc_available`: asserts non‑zero version components when IPC is available.
- DLL load/version (simple): `tests/test_integration_dll_load.py`
  - Loads DLL, initializes signatures, retrieves version and target machine; skips on IPC error.
- es CLI: `tests/test_integration_es.py`
  - Windows‑only when `es.exe` is available; recognizes PATH, package bin, CWD, repo `./bin`, and common install paths.
  - Uses multi‑query fallback (path: filter → absolute path → plain tokens) to avoid false negatives.
- HTTP CLI: `tests/test_integration_http.py`
  - Portable; patches `requests.get` to emulate the Everything HTTP API and asserts URL/params and JSON output shape.

## Linting & Style

- Use `flake8` with `max-line-length = 120`.
- Exclude `.venv`, `Everything-SDK`, and `docs` from linting.
- Per‑file ignores for `pyeverything/dll.py`: `E221`, `E501` (aligned constants and long docstrings).

## Commits & Changes

- Prefer atomic commits grouped by logical change.
- When specifically requested, commit certain changes separately (e.g., integration tests added in a dedicated commit).
- `.gitignore` includes local logs used during debugging: `logs/es_test.json`, `logs/es_search_hosts.json`.

## Sandbox & Execution

- The agent runs in a Linux sandbox with the repo mounted from a Windows NTFS drive.
- Capabilities: read/write files in the workspace; run shell reads; stage/commit with approval.
- Limitations: cannot execute Windows binaries (e.g., `.venv\Scripts\pytest.exe`), cannot access outside the workspace, network typically restricted.
- Workflow: Windows‑only tests run on the user’s machine; the agent can add CI to run them on `windows-latest` if desired.

## Local Run Cheatsheet (Windows)

- Unit tests: `.\.venv\Scripts\pytest -q`
- DLL integration tests: `.\.venv\Scripts\pytest -q tests\test_integration_dll.py`
- DLL step tests: `.\.venv\Scripts\pytest -q tests\test_integration_dll_steps.py`
- DLL quick load/version: `.\.venv\Scripts\pytest -q tests\test_integration_dll_load.py`
- Full suite: `.\.venv\Scripts\pytest -q`
- Lint: `.\.venv\Scripts\flake8`

Verbose options for diagnostics:
- `-vv` to list each test; `-s` to show prints/logs; `-ra` to show skip reasons; `-l` to show locals; `--tb=long` for full tracebacks.
Example: `.\.venv\Scripts\pytest -vv -s -ra tests\test_integration_dll_steps.py`

IPC guidance:
- If tests skip with "Everything IPC not available", start the Everything app/service, then rerun tests.

DLL bindings check from Python REPL or script:
- `from pyeverything.dll import load_everything_dll, init_functions, verify_dll_bindings`
- `dll = load_everything_dll(); init_functions(dll); ok, missing = verify_dll_bindings(dll)`
- `print(ok, missing)`

## Sharing Diagnostics

- Multi‑line output: prefer saving to files under `logs/` and referencing paths (e.g., `logs/es_test.json`).
- PowerShell helpers:
  - `mkdir logs -Force`
  - `... --json | Out-File -Encoding utf8 logs\es_search_hosts.json`
  - `"$LASTEXITCODE" | Out-File -Encoding ascii logs\exit.txt`

## Notes

- Integration tests auto‑skip on non‑Windows or when `Everything64.dll` is missing.
- If the Everything index is cold, launching the app or waiting briefly may be necessary before search assertions.
