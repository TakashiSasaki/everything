# everything_test_selftest.py
# Test script to verify --test (with/without --json), --search (with/without --all-fields) of subprocess_list.py

import subprocess
import sys
import re
import json

SCRIPT = "everything-es"

def run_test(args, expected_pattern=None, json_check=None):
    try:
        result = subprocess.run(
            ["poetry", "run", SCRIPT] + args,
            capture_output=True,
            text=True
        )
    except Exception as e:
        print(f"Execution failed: {e}")
        return False

    print(f"\nCOMMAND: python {SCRIPT} {' '.join(args)}")
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    if expected_pattern:
        # For pattern-based checks (like --test)
        return result.returncode == 0 and re.search(expected_pattern, result.stdout)
    elif json_check:
        # For JSON output validation
        try:
            data = json.loads(result.stdout)
            return json_check(data)
        except Exception as e:
            print(f"JSON parse error: {e}")
            return False
    else:
        return False

def check_hosts_ics_json_allfields(data):
    # Checks for --json --all-fields: full record
    if not isinstance(data, list) or len(data) == 0:
        print("JSON output is not a non-empty list.")
        return False
    entry = data[0]
    required_keys = [
        "name", "path", "extension", "size",
        "date_created", "date_modified", "date_accessed",
        "attributes", "run_count", "date_run",
        "date_recently_changed", "file_list_file_name"
    ]
    return all(k in entry for k in required_keys) and entry["name"].lower() == "hosts.ics"

def check_hosts_ics_json_default(data):
    # Checks for --json (no --all-fields): only name, path, size
    if not isinstance(data, list) or len(data) == 0:
        print("JSON output is not a non-empty list.")
        return False
    entry = data[0]
    # Must only have "name", "path", "size"
    required_keys = ["name", "path", "size"]
    extraneous_keys = set(entry.keys()) - set(required_keys)
    return (
        all(k in entry for k in required_keys)
        and entry["name"].lower() == "hosts.ics"
        and not extraneous_keys
    )

def main():
    expected_test = r"Test passed: hosts file found with size \d+\."

    # Test 1: --test only
    test_passed = run_test(["--test"], expected_pattern=expected_test)

    # Test 2: --test and --json
    test_json_passed = run_test(["--test", "--json"], expected_pattern=expected_test)

    # Test 3: --search for hosts.ics in JSON with all fields
    search_query = r"windows\system32\drivers\etc\hosts.ics"
    search_allfields_passed = run_test(
        ["--search", search_query, "--json", "--all-fields"],
        json_check=check_hosts_ics_json_allfields
    )

    # Test 4: --search for hosts.ics in JSON with default fields
    search_default_passed = run_test(
        ["--search", search_query, "--json"],
        json_check=check_hosts_ics_json_default
    )

    if all([test_passed, test_json_passed, search_allfields_passed, search_default_passed]):
        print("✅ All tests PASSED: --test, --search, --all-fields combinations work as expected.")
        sys.exit(0)
    else:
        print("❌ Test FAILED: Some options did not behave as expected.")
        sys.exit(1)

if __name__ == "__main__":
    main()
