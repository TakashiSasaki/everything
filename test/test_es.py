import os
import os
import os
import subprocess
import sys
import re
import json
import unittest
from unittest import mock

SCRIPT_MODULE = "everything_cli.es"

def run_command(args):
    cmd = [sys.executable, "-m", SCRIPT_MODULE] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout, result.stderr
    except Exception as e:
        # This block should ideally not be reached if check=False
        # but keeping it for robustness, returning empty strings for output
        print(f"Failed to run test command: {e}")
        return "", str(e)

def test_test_option():
    stdout, stderr = run_command(["--test"])
    expected_pattern = r"Test passed: hosts file found with size \d+."
    assert re.search(expected_pattern, stdout), "--test output not as expected"

def test_test_json_option():
    stdout, stderr = run_command(["--test", "--json"])
    try:
        data = json.loads(stdout)
        assert data["passed"] is True, "--test --json: 'passed' is not True"
        assert isinstance(data["size"], int) and data["size"] > 0, "--test --json: invalid or missing 'size'"
    except Exception as e:
        raise AssertionError(f"JSON parse error or assertion failed: {e}\nSTDOUT: {stdout}\nSTDERR: {stderr}") from e

@mock.patch('everything_cli.es.subprocess.run')
def test_search_json_option(mock_run):
    mock_run.return_value = mock.Mock(
        stdout=json.dumps([
            {
                "name": "hosts.ics",
                "path": "C:\\Windows\\System32\\drivers\\etc\\hosts.ics",
                "size": 438
            }
        ], indent=2),
        stderr="",
        returncode=0
    )

    search_query = r"windows\\system32\\drivers\\etc\\hosts.ics"
    stdout, stderr = run_command(["--search", search_query, "--json"])
    try:
        data = json.loads(stdout)
        assert isinstance(data, list), "--search --json: output is not a list"
        found = any(
            entry.get("name") == "hosts.ics" and             os.path.normcase(r"C:\Windows\System32\drivers\etc") == os.path.normcase(os.path.dirname(entry.get("path", "")))
            for entry in data
        )
        assert found, "--search --json: expected file not found in results"
    except Exception as e:
        raise AssertionError(f"JSON parse error or assertion failed: {e}\nSTDOUT: {stdout}\nSTDERR: {stderr}") from e

@mock.patch('everything_cli.es.subprocess.run')
def test_search_allfields_json_option(mock_run):
    mock_run.return_value = mock.Mock(
        stdout=json.dumps([
            {
                "name": "hosts.ics",
                "path": "C:\\Windows\\System32\\drivers\\etc\\hosts.ics",
                "size": 438,
                "extension": "ics",
                "date_created": "2022-07-27T12:37:01.620755",
                "date_modified": "2024-06-13T10:28:57.492615",
                "date_accessed": "2025-06-23T00:15:11.843185",
                "attributes": 8224,
                "file_list_file_name": "",
                "run_count": 0,
                "date_run": None,
                "date_recently_changed": None
            }
        ], indent=2) + '\n',
        stderr="",
        returncode=0
    )

    search_query = r"windows\\system32\\drivers\\etc\\hosts.ics"
    stdout, stderr = run_command(["--search", search_query, "--json", "--all-fields"])
    try:
        data = json.loads(stdout)
        assert isinstance(data, list) and len(data) > 0, "--search --json --all-fields: output not a list or empty"
        found = False
        for entry in data:
            if (
                entry.get("name") == "hosts.ics" and                os.path.normcase(r"C:\Windows\System32\drivers\etc") == os.path.normcase(os.path.dirname(entry.get("path", "")))
            ):
                assert "date_modified" in entry, "--search --json --all-fields: 'date_modified' missing"
                found = True
        assert found, "--search --json --all-fields: expected file not found in results"
    except Exception as e:
        raise AssertionError(f"JSON parse error or assertion failed: {e}\nSTDOUT: {stdout}\nSTDERR: {stderr}") from e
