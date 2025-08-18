"""
Integration tests for the pyeverything.es CLI adapter.

These tests invoke the module as a script (python -m pyeverything.es)
to exercise the real Everything es.exe CLI. They are guarded to only
run on Windows and when an es.exe binary is available in PATH, the
package bin directory, or the current working directory.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import pytest


def _es_present() -> bool:
    """Return True if es.exe is available via PATH, package bin, or CWD."""
    if shutil.which("es.exe"):
        return True
    # package bin
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bin_es = os.path.join(repo_root, "pyeverything", "bin", "es.exe")
    if os.path.isfile(bin_es) and os.access(bin_es, os.X_OK):
        return True
    # current working directory
    cwd_es = os.path.join(os.getcwd(), "es.exe")
    if os.path.isfile(cwd_es) and os.access(cwd_es, os.X_OK):
        return True
    # common absolute install locations
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


def run_es(args: list[str]) -> tuple[str, str, int]:
    """Run `python -m pyeverything.es` with args; return (stdout, stderr, rc)."""
    cmd = [sys.executable, "-m", "pyeverything.es", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


@requires_windows
@requires_es
def test_test_option_text() -> None:
    stdout, stderr, rc = run_es(["--test"]) 
    assert rc == 0, f"--test failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    assert "Test passed: hosts file found with size" in stdout


@requires_windows
@requires_es
def test_test_option_json() -> None:
    stdout, stderr, rc = run_es(["--test", "--json"]) 
    assert rc == 0, f"--test --json failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert data.get("passed") is True
    assert isinstance(data.get("size"), int)


@requires_windows
@requires_es
def test_search_json_option() -> None:
    # Use a known Windows system file that exists on all systems
    query = r"windows\\system32\\drivers\\etc\\hosts"
    stdout, stderr, rc = run_es(["--search", query, "--json"]) 
    assert rc == 0, f"--search --json failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert isinstance(data, list)
    found = any(
        entry.get("name") == "hosts" and
        entry.get("path", "").lower().endswith(r"windows\system32\drivers\etc")
        for entry in data
    )
    assert found, "Expected hosts.ics entry not found in search results"


@requires_windows
@requires_es
def test_search_allfields_json_option() -> None:
    query = r"windows\\system32\\drivers\\etc\\hosts"
    stdout, stderr, rc = run_es(["--search", query, "--json", "--all-fields"]) 
    assert rc == 0, f"--search --json --all-fields failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert isinstance(data, list) and len(data) > 0
    found = False
    for entry in data:
        if (
            entry.get("name") == "hosts" and
            entry.get("path", "").lower().endswith(r"windows\system32\drivers\etc")
        ):
            # Representative all-fields presence
            assert "date_modified" in entry
            found = True
    assert found, "Expected hosts.ics entry with extended fields not found"
