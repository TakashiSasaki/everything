# test_everything_file_list_testmode.py
"""
Test script for everything_file_list.py --test option (normal and --json).

- Verifies that '--test' produces expected plain text output.
- Verifies that '--test --json' produces correct JSON output.
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
    # 出力が正しいJSONで、passed: true, size > 0 を含むかチェック
    try:
        data = json.loads(stdout)
        assert data["passed"] is True, "--test --json: 'passed' is not True"
        assert isinstance(data["size"], int) and data["size"] > 0, "--test --json: invalid or missing 'size'"
    except Exception as e:
        print(f"JSON parse error or assertion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_test_option()
    test_test_json_option()
    print("✅ Both --test and --test --json tests passed.")
