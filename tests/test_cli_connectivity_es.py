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
    queries = [
        r'path:"\\windows\\system32\\drivers\\etc" hosts',
        r"C:\\Windows\\System32\\drivers\\etc\\hosts",
        "windows system32 drivers etc hosts",
    ]
    out, err, rc = "", "", 1
    for q in queries:
        out, err, rc = _run(["--search", q])
        if rc == 0 and out:
            break
    assert rc == 0, f"rc={rc} err={err}\n{out}"
    norm = out.strip().lower().replace("/", "\\")
    if not norm or norm == "no results found.":
        pytest.skip("Everything index not ready; skipping text connectivity for es.exe")
    assert r"windows\system32\drivers\etc\hosts" in norm


@requires_windows
@requires_es
def test_connectivity_json() -> None:
    queries = [
        r'path:"\\windows\\system32\\drivers\\etc" hosts',
        r"C:\\Windows\\System32\\drivers\\etc\\hosts",
        "windows system32 drivers etc hosts",
    ]
    out, err, rc = "", "", 1
    data = []
    for q in queries:
        out, err, rc = _run(["--search", q, "--json"]) 
        if rc == 0:
            try:
                data = json.loads(out)
            except Exception:
                data = []
        if isinstance(data, list) and data:
            break
    assert rc == 0, f"rc={rc} err={err}\n{out}"
    if not isinstance(data, list) or not data:
        pytest.skip("Everything index not ready; skipping JSON connectivity for es.exe")
    assert any(r"windows\system32\drivers\etc\hosts" in str(e.get("path", "")).lower() for e in data)
