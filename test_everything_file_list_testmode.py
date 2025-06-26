# test_everything_file_list_testmode.py
"""
Test script for everything_file_list.py

- Verifies '--test' (plain text) output.
- Verifies '--test --json' output.
- Verifies '--search ... --json' returns expected file entry.
"""

import subprocess
import sys
import json

def run_command(args):
    cmd = [sys.executable, "everything_file_list.py"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        print(f"Failed to run test command: {e}")
        sys.exit(1)

def test_test_option():
    stdout, stderr = run_command(["--test"])
    print("\n--- --test STDOUT ---")
    print(stdout)
    if stderr:
        print("--- --test STDERR ---")
        print(stderr)
    assert "Test passed: hosts file found with size" in stdout, "--test output not as expected"

def test_test_json_option():
    stdout, stderr = run_command(["--test", "--json"])
    print("\n--- --test --json STDOUT ---")
    print(stdout)
    if stderr:
        print("--- --test --json STDERR ---")
        print(stderr)
    try:
        data = json.loads(stdout)
        assert data["passed"] is True, "--test --json: 'passed' is not True"
        assert isinstance(data["size"], int) and data["size"] > 0, "--test --json: invalid or missing 'size'"
    except Exception as e:
        print(f"JSON parse error or assertion failed: {e}")
        sys.exit(1)

def test_search_json_option():
    search_query = r"windows\system32\drivers\etc\hosts.ics"
    stdout, stderr = run_command(["--search", search_query, "--json"])
    print(f"\n--- --search \"{search_query}\" --json STDOUT ---")
    print(stdout)
    if stderr:
        print("--- --search ... --json STDERR ---")
        print(stderr)
    try:
        data = json.loads(stdout)
        assert isinstance(data, list), "--search --json: output is not a list"
        # 少なくとも1件はヒットし、nameとpathが一致するものがあるか
        found = any(
            entry.get("name") == "hosts.ics" and 
            entry.get("path", "").lower().endswith(r"windows\system32\drivers\etc")
            for entry in data
        )
        assert found, "--search --json: expected file not found in results"
    except Exception as e:
        print(f"JSON parse error or assertion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_test_option()
    test_test_json_option()
    test_search_json_option()
    print("✅ All tests (--test, --test --json, --search --json) passed.")
