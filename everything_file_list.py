#!/usr/bin/env python3
"""
everything_file_list.py

This script connects to the Everything HTTP API and retrieves a list of files
matching a given search query, or runs a connectivity test.

Features:
  - Load EVERYTHING_HOST and EVERYTHING_PORT from .env (current directory)
  - Override host and port via --host and --port options
  - Perform normal search with --search, --offset, --count
  - --all-fields option to request all available fields
  - --json option to output results in JSON format
  - Test mode (--test) verifies the API by searching for
    C:\\Windows\\System32\\drivers\\etc\\hosts and checking its size > 1

Requirements:
  pip install requests python-dotenv
"""
import argparse
import os
import sys
import json
from dotenv import load_dotenv
import requests

# Fields supported by the HTTP API
BASIC_COLUMNS = {"file_name_column":1, "path_column":1, "size_column":1}
ALL_COLUMNS = {
    "file_name_column":1,
    "path_column":1,
    "full_path_column":1,
    "size_column":1,
    "extension_column":1,
    "date_created_column":1,
    "date_modified_column":1,
    "date_accessed_column":1,
    "attributes_column":1,
    "file_list_file_name_column":1,
    "run_count_column":1,
    "date_run_column":1,
    "date_recently_changed_column":1,
    "highlighted_file_name_column":1,
    "highlighted_path_column":1,
    "highlighted_full_path_column":1
}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Retrieve file list from Everything HTTP API or run connectivity test"
    )
    parser.add_argument(
        "--host", default=None,
        help="Hostname or IP for Everything HTTP server (overrides EVERYTHING_HOST)"
    )
    parser.add_argument(
        "--port", type=int, default=None,
        help="Port for Everything HTTP server (overrides EVERYTHING_PORT)"
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
        "--all-fields", action="store_true",
        help="Request all available fields from the Everything HTTP API"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run connectivity test against Everything HTTP API"
    )
    return parser.parse_args()

def main():
    load_dotenv()
    args = parse_args()

    host = args.host or os.getenv("EVERYTHING_HOST") or "127.0.0.1"
    try:
        port = args.port or int(os.getenv("EVERYTHING_PORT", "")) or 80
    except ValueError:
        sys.exit("Invalid port number in EVERYTHING_PORT environment variable.")

    base_url = f"http://{host}:{port}/"

    # Build parameter set: basic JSON + columns
    params = {"search": args.search or "", "offset": args.offset, "count": args.count, "json": 1}
    columns = ALL_COLUMNS if args.all_fields else BASIC_COLUMNS
    params.update(columns)

    # Test mode
    if args.test:
        test_query = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        params.update({"search": test_query, "offset": 0, "count": 1})
        try:
            resp = requests.get(base_url, params=params)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            sys.exit(f"Test failed: could not connect: {e}")
        results = data.get("results", [])
        if not results:
            sys.exit("Test failed: no results for hosts file.")
        size = int(results[0].get("size", 0))
        if size > 1:
            output = {"passed": True, "size": size}
            if args.json:
                print(json.dumps(output))
            else:
                print(f"Test passed: hosts file found with size {size}.")
            sys.exit(0)
        sys.exit(f"Test failed: hosts file size is {size}, expected > 1.")

    # Normal search
    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        sys.exit(f"Error: could not connect: {e}")

    data = response.json()
    results = data.get("results", [])
    if not results:
        print("No results found.")
        return

    # Output
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        # Tab-separated values per entry
        keys = list(columns.keys())
        for item in results:
            values = [str(item.get(k, "")) for k in keys]
            print("\t".join(values))

if __name__ == "__main__":
    main()
