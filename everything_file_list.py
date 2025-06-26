#!/usr/bin/env python3
"""
everything_file_list.py

This script connects to the Everything HTTP API and retrieves a list of files
matching a given search query, or runs a connectivity test.

Features:
  - Load EVERYTHING_HOST and EVERYTHING_PORT from .env (current directory)
  - Override host and port via --host and --port options
  - Perform normal search with --search, --offset, --count
  - Test mode (--test) verifies the API by searching for
    C:\\Windows\\System32\\drivers\\etc\\hosts and checking its size > 1

Requirements:
  pip install requests python-dotenv
"""
import argparse
import os
import sys

from dotenv import load_dotenv
import requests


def parse_args():
    parser = argparse.ArgumentParser(
        description="Retrieve file list from Everything HTTP API or run connectivity test"
    )
    parser.add_argument(
        "--host", default=None,
        help="Hostname or IP for Everything HTTP server (overrides EVERYTHING_HOST if set)"
    )
    parser.add_argument(
        "--port", type=int, default=None,
        help="Port for Everything HTTP server (overrides EVERYTHING_PORT if set)"
    )
    parser.add_argument(
        "--search", required=False,
        help="Search pattern (Everything query syntax)"
    )
    parser.add_argument(
        "--offset", type=int, default=0,
        help="Result offset (default: %(default)s)"
    )
    parser.add_argument(
        "--count", type=int, default=100,
        help="Maximum number of results to return (default: %(default)s)"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run connectivity test against Everything HTTP API"
    )
    return parser.parse_args()


def main():
    # Load environment variables from .env
    load_dotenv()

    args = parse_args()

    # Determine host: CLI > ENV > default
    host = args.host or os.getenv("EVERYTHING_HOST") or "127.0.0.1"

    # Determine port: CLI > ENV > default
    try:
        port = args.port or int(os.getenv("EVERYTHING_PORT", "")) or 80
    except ValueError:
        sys.exit("Invalid port number in EVERYTHING_PORT environment variable.")

    base_url = f"http://{host}:{port}/"

    # If test mode, verify API is responding and returns hosts file with size > 1
    if args.test:
        test_query = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        test_params = {
            "search": test_query,
            "offset": 0,
            "count": 1,
            "json": 1,
            "size_column": 1,
        }
        try:
            resp = requests.get(base_url, params=test_params)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            sys.exit(f"Test failed: could not connect to Everything HTTP API: {e}")

        results = data.get("results", [])
        if not results:
            sys.exit(
                "Test failed: no results for hosts file."
                " Check that Everything HTTP server has indexing enabled for system files."
            )

        size_str = results[0].get("size", "0")
        try:
            size = int(size_str)
        except (ValueError, TypeError):
            sys.exit(f"Test failed: invalid size value '{size_str}'.")

        if size > 1:
            print(f"Test passed: hosts file found with size {size}.")
            sys.exit(0)
        else:
            sys.exit(f"Test failed: hosts file size is {size}, expected > 1.")

    # Ensure --search is provided when not in test mode
    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")

    # Perform normal search
    params = {
        "search": args.search,
        "offset": args.offset,
        "count": args.count,
        "json": 1,
        # Include path and size in JSON response
        "path_column": 1,
        "size_column": 1,
        # "date_modified_column": 1,  # Uncomment to include
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        sys.exit(f"Error connecting to Everything HTTP API: {e}")

    data = response.json()
    results = data.get("results", [])
    if not results:
        print("No results found.")
        return

    for item in results:
        name = item.get("name", "<unknown>")
        path = item.get("path", "")
        print(f"{name}\t{path}")


if __name__ == "__main__":
    main()
