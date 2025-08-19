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
def test_connectivity_text_via_search() -> None:
    # Validate connectivity using a robust tokenized search in text mode
    query = "windows system32 drivers etc hosts"
    stdout, stderr, rc = run_command(["--search", query]) 
    assert rc == 0, f"--search failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    assert r"windows\system32\drivers\etc\hosts" in stdout.lower().replace("/", "\\")


@requires_windows
@requires_dll
def test_search_json_option() -> None:
    # Use a universal Windows system file and a robust tokenized query
    query = "windows system32 drivers etc hosts"
    stdout, stderr, rc = run_command(["--search", query, "--json"]) 
    assert rc == 0, f"--search --json failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert isinstance(data, list)
    found = any(
        str(entry.get("name", "")).lower() == "hosts" and
        r"windows\system32\drivers\etc\hosts" in str(entry.get("path", "")).lower()
        for entry in data
    )
    assert found, "Expected hosts entry not found in search results"


@requires_windows
@requires_dll
def test_search_allfields_json_option() -> None:
    query = "windows system32 drivers etc hosts"
    stdout, stderr, rc = run_command(["--search", query, "--json", "--all-fields"]) 
    assert rc == 0, f"--search --json --all-fields failed rc={rc}, stderr={stderr}\nstdout={stdout}"
    data = json.loads(stdout)
    assert isinstance(data, list) and len(data) > 0
    found = False
    for entry in data:
        if (
            str(entry.get("name", "")).lower() == "hosts" and
            r"windows\system32\drivers\etc\hosts" in str(entry.get("path", "")).lower()
        ):
            # A representative all-fields key
            assert "date_modified" in entry
            found = True
    assert found, "Expected hosts entry with extended fields not found"
