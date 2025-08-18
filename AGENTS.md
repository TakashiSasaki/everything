# AGENTS

This document records working agreements and decisions made during the current session to guide future automation and contributions.

## Operating Mode

- Prefer running Codex CLI in `--full-auto` mode for maximum autonomy.
- For this repository, proceed autonomously in the current sandbox when a restart is not requested.

## Platform and DLL Policy

- Use only the 64‑bit Everything SDK DLL: `Everything64.dll`.
- DLL load order: package `pyeverything/bin/Everything64.dll` → current working directory → system `PATH`.
- Do not attempt to load or fallback to 32‑bit DLLs.

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
  - The DLL CLI (`python -m pyeverything.dll`) returns JSON entries where `path` contains the full path; tests match against the full path suffix.

## Linting & Style

- Use `flake8` with `max-line-length = 120`.
- Exclude `.venv`, `Everything-SDK`, and `docs` from linting.
- Per‑file ignores for `pyeverything/dll.py`: `E221`, `E501` (aligned constants and long docstrings).

## Commits & Changes

- Prefer atomic commits grouped by logical change.
- When specifically requested, commit certain changes separately (e.g., integration tests added in a dedicated commit).

## Local Run Cheatsheet (Windows)

- Unit tests: `.\.venv\Scripts\pytest -q`
- DLL integration tests: `.\.venv\Scripts\pytest -q tests\test_integration_dll.py`
- Full suite: `.\.venv\Scripts\pytest -q`
- Lint: `.\.venv\Scripts\flake8`

## Notes

- Integration tests auto‑skip on non‑Windows or when `Everything64.dll` is missing.
- If the Everything index is cold, launching the app or waiting briefly may be necessary before search assertions.

