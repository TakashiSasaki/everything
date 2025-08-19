"""
Connectivity tests that replace the deprecated `--test` CLI option.

These tests exercise the DLL-backed CLIs using robust search queries
to verify that Everything is reachable and indexed (finds the hosts file).

They are Windows-only and require `pyeverything/bin/Everything64.dll`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import pytest


def _dll_present() -> bool:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dll_path = os.path.join(repo_root, "pyeverything", "bin", "Everything64.dll")
    return os.path.isfile(dll_path)


requires_windows = pytest.mark.skipif(sys.platform != "win32", reason="Requires Windows")
requires_dll = pytest.mark.skipif(not _dll_present(), reason="Everything64.dll missing in pyeverything/bin")


@pytest.mark.parametrize("module", ["pyeverything.dll", "pyeverything.dll_class"])  # both CLIs
@requires_windows
@requires_dll
def test_connectivity_text(module: str) -> None:
    query = "windows system32 drivers etc hosts"
    cmd = [sys.executable, "-m", module, "--search", query]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, f"text {module} rc={r.returncode} stderr={r.stderr}\nstdout={r.stdout}"
    out = (r.stdout or "").lower().replace("/", "\\")
    assert r"windows\system32\drivers\etc\hosts" in out


@pytest.mark.parametrize("module", ["pyeverything.dll", "pyeverything.dll_class"])  # both CLIs
@requires_windows
@requires_dll
def test_connectivity_json(module: str) -> None:
    query = "windows system32 drivers etc hosts"
    cmd = [sys.executable, "-m", module, "--search", query, "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, f"json {module} rc={r.returncode} stderr={r.stderr}\nstdout={r.stdout}"
    data = json.loads(r.stdout or "[]")
    assert isinstance(data, list) and len(data) >= 0
    found = any(
        r"windows\system32\drivers\etc\hosts" in str(e.get("path", "")).lower()
        for e in data
    )
    assert found, f"Expected hosts entry not found in {module} results"

