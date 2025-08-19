"""
Standalone connectivity tests for the es CLI.

Replaces the deprecated `--test` option with pytest checks that run
`python -m pyeverything.es --search ...` in both text and JSON modes.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import pytest


def _es_present() -> bool:
    if shutil.which("es.exe"):
        return True
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bin_es = os.path.join(repo_root, "pyeverything", "bin", "es.exe")
    if os.path.isfile(bin_es) and os.access(bin_es, os.X_OK):
        return True
    cwd_es = os.path.join(os.getcwd(), "es.exe")
    if os.path.isfile(cwd_es) and os.access(cwd_es, os.X_OK):
        return True
    repo_bin_es = os.path.join(os.getcwd(), "bin", "es.exe")
    if os.path.isfile(repo_bin_es) and os.access(repo_bin_es, os.X_OK):
        return True
    common_paths = [
        r"C:\\bin\\es.exe",
        os.path.join(os.environ.get("ProgramFiles", r"C:\\Program Files"), "Everything", "es.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\\Program Files (x86)"), "Everything", "es.exe"),
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return True
    return False


requires_windows = pytest.mark.skipif(sys.platform != "win32", reason="Requires Windows")
requires_es = pytest.mark.skipif(not _es_present(), reason="es.exe not found (PATH/bin/CWD)")


def _run(args: list[str]) -> tuple[str, str, int]:
    cmd = [sys.executable, "-m", "pyeverything.es", *args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode


@requires_windows
@requires_es
def test_connectivity_text() -> None:
    q = "windows system32 drivers etc hosts"
    out, err, rc = _run(["--search", q])
    assert rc == 0, f"rc={rc} err={err}\n{out}"
    assert r"windows\system32\drivers\etc\hosts" in out.lower().replace("/", "\\")


@requires_windows
@requires_es
def test_connectivity_json() -> None:
    q = "windows system32 drivers etc hosts"
    out, err, rc = _run(["--search", q, "--json"]) 
    assert rc == 0, f"rc={rc} err={err}\n{out}"
    data = json.loads(out)
    assert isinstance(data, list)
    assert any(r"windows\system32\drivers\etc\hosts" in str(e.get("path", "")).lower() for e in data)

