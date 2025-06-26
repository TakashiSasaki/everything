#!/usr/bin/env python3
"""
everything_subprocess_list.py

This script uses the Everything "es.exe" command-line interface to retrieve a list of files
matching a given search query, or runs a connectivity test via subprocess.

Features:
  - Perform search by invoking es.exe as a subprocess
  - Support --search, --offset, --count options
  - Test mode (--test) verifies es.exe by searching for
    C:\\Windows\\System32\\drivers\\etc\\hosts and checking its size > 1
  - Validates that es.exe is available in PATH or current directory before execution

Requirements:
  - Everything must be installed and accessible in PATH or alongside the script
"""
import argparse
import os
import shutil
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Use es.exe to list files or run a connectivity test"
    )
    parser.add_argument(
        "--search", required=False,
        help="Search pattern (Everything query syntax)"
    )
    parser.add_argument(
        "--offset", type=int, default=0,
        help="Result offset (zero-based)"
    )
    parser.add_argument(
        "--count", type=int, default=100,
        help="Maximum number of results to return"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run connectivity test against es.exe"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Locate es.exe in PATH or current directory
    es_cmd = shutil.which("es.exe")
    if not es_cmd:
        local_path = os.path.join(os.getcwd(), "es.exe")
        if os.path.isfile(local_path) and os.access(local_path, os.X_OK):
            es_cmd = local_path
    if not es_cmd:
        sys.exit("Error: 'es.exe' not found in PATH or current directory.")

    # Test mode: verify es.exe can find the hosts file and report its size
    if args.test:
        test_query = r"C:\Windows\System32\drivers\etc\hosts"
        cmd = [es_cmd, "-size", "-n", "1", test_query]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            sys.exit(f"Test failed: es.exe error: {e.stderr.strip()}")

        output = result.stdout.strip()
        size_token = output.split()[0] if output else "0"
        try:
            size = int(size_token)
        except (ValueError, TypeError):
            sys.exit(f"Test failed: invalid size '{size_token}' from output '{output}'")

        if size > 1:
            print(f"Test passed: hosts file found with size {size}.")
            sys.exit(0)
        else:
            sys.exit(f"Test failed: hosts file size is {size}, expected > 1.")

    # Normal search mode requires --search
    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")

    # Build es.exe command with filename, path, and size columns, offset, and count
    cmd = [
        es_cmd,
        "-filename-column",
        "-path-column",
        "-size",
        "-offset", str(args.offset),
        "-n", str(args.count),
        args.search
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error running es.exe: {e.stderr.strip()}")

    lines = result.stdout.splitlines()
    if not lines:
        print("No results found.")
        return

    # Each line is tab-separated: <name>\t<path>\t<size>
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 2:
            name = parts[0]
            path = parts[1]
        else:
            full = parts[0]
            name = os.path.basename(full)
            path = full
        print(f"{name}\t{path}")


if __name__ == "__main__":
    main()
