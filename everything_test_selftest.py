# everything_test_selftest.py
# Test script to verify that --test option of everything_subprocess_list.py works correctly

import subprocess
import sys
import re

SCRIPT = "everything_subprocess_list.py"

def main():
    try:
        # Run the script with --test and capture output
        result = subprocess.run(
            [sys.executable, SCRIPT, "--test"],
            capture_output=True,
            text=True
        )
    except Exception as e:
        print(f"Execution failed: {e}")
        sys.exit(1)

    # The script should exit with code 0 and print the expected message
    passed = result.returncode == 0 and re.search(r"Test passed: hosts file found with size \d+\.", result.stdout)

    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    if passed:
        print("✅ Test PASSED: --test works as expected.")
        sys.exit(0)
    else:
        print("❌ Test FAILED: Unexpected result from --test option.")
        sys.exit(1)

if __name__ == "__main__":
    main()
