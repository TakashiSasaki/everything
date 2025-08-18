"""
Integration tests for the pyeverything.dll CLI adapter.

These tests invoke the module as a script (python -m pyeverything.dll)
to exercise the real Everything SDK DLL and IPC path. They are guarded
to only run on Windows and when the 64-bit DLL is present in the
package's bin directory.
"""
from __future__ import annotations

import json
import os
import sys
import subprocess
import pytest


def _dll_present() -> bool:
    """Return True if Everything64.dll exists in the package bin dir."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dll_path = os.path.join(repo_root, "pyeverything", "bin", "Everything64.dll")
    return os.path.isfile(dll_path)


requires_windows = pytest.mark.skipif(sys.platform != "win32", reason="Requires Windows")
requires_dll = pytest.mark.skipif(not _dll_present(), reason="Everything64.dll missing in pyeverything/bin")


def run_command(args: list[str]) -> tuple[str, str, int]:
    """Run `python -m pyeverything.dll` with args; return (stdout, stderr, rc)."""
    cmd = [sys.executable, "-m", "pyeverything.dll", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


@requires_windows
@requires_dll
def test_test_option_text() -> None:
    stdout, stderr, rc = run_command(["--test"]) 
    assert rc == 0, f"--test failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    assert stdout.startswith("Test passed: hosts file found, size "), "Unexpected --test text output"


@requires_windows
@requires_dll
def test_test_option_json() -> None:
    stdout, stderr, rc = run_command(["--test", "--json"]) 
    assert rc == 0, f"--test --json failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert data.get("passed") is True
    assert isinstance(data.get("size"), int) and data["size"] > 0


@requires_windows
@requires_dll
def test_search_json_option() -> None:
    # Use a known Windows system file that typically exists
    query = r"windows\\system32\\drivers\\etc\\hosts.ics"
    stdout, stderr, rc = run_command(["--search", query, "--json"]) 
    assert rc == 0, f"--search --json failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert isinstance(data, list) and len(data) >= 0
    found = any(
        entry.get("name") == "hosts.ics" and
        entry.get("path", "").lower().endswith(r"windows\system32\drivers\etc")
        for entry in data
    )
    assert found, "Expected hosts.ics entry not found in search results"


@requires_windows
@requires_dll
def test_search_allfields_json_option() -> None:
    query = r"windows\\system32\\drivers\\etc\\hosts.ics"
    stdout, stderr, rc = run_command(["--search", query, "--json", "--all-fields"]) 
    assert rc == 0, f"--search --json --all-fields failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert isinstance(data, list) and len(data) > 0
    found = False
    for entry in data:
        if (
            entry.get("name") == "hosts.ics" and
            entry.get("path", "").lower().endswith(r"windows\system32\drivers\etc")
        ):
            # A representative all-fields key
            assert "date_modified" in entry
            found = True
    assert found, "Expected hosts.ics entry with extended fields not found"

