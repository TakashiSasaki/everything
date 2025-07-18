#!/usr/bin/env python3
""" 
subprocess_list.py

This script uses the Everything "es.exe" command-line interface to retrieve a list of files
matching a given search query, runs a connectivity test, and supports various output formats.

Features:
  - Perform search by invoking es.exe as a subprocess
  - Support --search, --offset, --count options
  - Support --all-fields option to display all available fields
  - Support --json option to output results in JSON format (uses CSV export internally for accurate parsing)
  - Support --csv option to export CSV from Everything and parse it
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
import json
import csv
import io


def parse_args():
    parser = argparse.ArgumentParser(
        description="Use es.exe to list files, run a connectivity test, or output in various formats"
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
        "--all-fields", action="store_true",
        help="Include all available fields in output"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results in JSON format (uses CSV export internally)"
    )
    parser.add_argument(
        "--csv", action="store_true",
        help="Export results via -csv and parse CSV"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run connectivity test against es.exe"
    )
    return parser.parse_args()


def locate_es():
    es_cmd = shutil.which("es.exe")
    if not es_cmd:
        # Check in the package's bin directory
        script_dir = os.path.dirname(__file__)
        bin_path = os.path.join(script_dir, "bin", "es.exe")
        if os.path.isfile(bin_path) and os.access(bin_path, os.X_OK):
            es_cmd = bin_path
    if not es_cmd:
        # Check in the current working directory
        local_path = os.path.join(os.getcwd(), "es.exe")
        if os.path.isfile(local_path) and os.access(local_path, os.X_OK):
            es_cmd = local_path
    if not es_cmd:
        sys.exit("Error: 'es.exe' not found in PATH, package bin directory, or current directory.")
    return es_cmd


def run_test(es_cmd):
    test_query = "C:\\Windows\\System32\\drivers\\etc\\hosts"
    cmd = [es_cmd, "-size", "-n", "1", test_query]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"Test failed: es.exe error: {e.stderr.strip()}")

    output = result.stdout.strip()
    size_token = output.split()[0] if output else "0"
    try:
        size = int(size_token)
    except (ValueError, TypeError):
        sys.exit(f"Test failed: invalid size '{size_token}' from output '{output}'")

    if size > 1:
        return {"passed": True, "size": size, "message": f"Test passed: hosts file found with size {size}."}
    else:
        return {"passed": False, "size": size, "message": f"Test failed: hosts file size is {size}, expected > 1."}


def build_field_config(all_fields):
    if all_fields:
        flags = [
            "-name",
            "-path-column",
            "-extension",
            "-size",
            "-date-created",
            "-date-modified",
            "-date-accessed",
            "-attributes",
            "-file-list-file-name",
            "-run-count",
            "-date-run",
            "-date-recently-changed",
            "-csv"
        ]
        names = [
            "name",
            "path",
            "extension",
            "size",
            "date_created",
            "date_modified",
            "date_accessed",
            "attributes",
            "file_list_file_name",
            "run_count",
            "date_run",
            "date_recently_changed"
        ]
    else:
        flags = ["-name", "-path-column", "-size", "-csv"]
        names = ["name", "path", "size"]
    return flags, names


def parse_csv_text(csv_text, field_names):
    records = []
    f = io.StringIO(csv_text)
    reader = csv.DictReader(f)
    # Map CSV headers (with spaces) to internal field names
    header_mapping = {
        'Name': 'name',
        'Filename': 'name',
        'Path': 'path',
        'Extension': 'extension',
        'Size': 'size',
        'Date Created': 'date_created',
        'Date Modified': 'date_modified',
        'Date Accessed': 'date_accessed',
        'Attributes': 'attributes',
        'File List File Name': 'file_list_file_name',
        'Run Count': 'run_count',
        'Date Run': 'date_run',
        'Date Recently Changed': 'date_recently_changed'
    }
    for row in reader:
        rec = {}
        for orig, val in row.items():
            key = header_mapping.get(orig)
            if key:
                rec[key] = val
        # Ensure all requested fields exist
        for name in field_names:
            rec.setdefault(name, None)
        records.append(rec)
    return records


def main():
    args = parse_args()
    es_cmd = locate_es()

    if args.test:
        test_result = run_test(es_cmd)
        if args.json:
            json.dump(test_result, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write('\n')
            sys.exit(0)
        else:
            print(test_result["message"])
            sys.exit(0)
        

    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")

    use_csv = args.csv or args.json
    field_flags, field_names = build_field_config(args.all_fields)

    records = []
    if use_csv:
        cmd = [es_cmd, *field_flags, args.search]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(f"Error exporting CSV: {e.stderr.strip()}")
        records = parse_csv_text(result.stdout, field_names)
    else:
        # Fallback to default text output
        text_flags, text_names = build_field_config(False)
        cmd = [es_cmd, *text_flags, args.search]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(f"Error running es.exe: {e.stderr.strip()}")
        for line in result.stdout.splitlines():
            parts = line.split()
            rec = {text_names[i]: parts[i] if i < len(parts) else None for i in range(len(text_names))}
            records.append(rec)

    if args.json:
        json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write('\n')
        sys.exit(0)
    elif not records:
        print("No results found.")
    else:
        for rec in records:
            if args.all_fields:
                print("\t".join(str(rec.get(n, '')) for n in field_names))
            else:
                print(rec.get('name', ''))

if __name__ == "__main__":
    main()
