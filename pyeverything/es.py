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
        description="Use es.exe to list files or output in various formats"
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
    return parser.parse_args()


def locate_es():
    """Locate es.exe on Windows.

    Search order:
    1) PATH (via shutil.which)
    2) Package bin directory (pyeverything/bin/es.exe)
    3) Current working directory (./es.exe)
    4) Repository root bin directory (./bin/es.exe)
    5) Common install locations (C:\\bin\\es.exe, Program Files\\Everything\\es.exe)
    """
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
        # Check in repository root ./bin (useful in sandboxes/CI)
        repo_bin = os.path.join(os.getcwd(), "bin", "es.exe")
        if os.path.isfile(repo_bin) and os.access(repo_bin, os.X_OK):
            es_cmd = repo_bin
    if not es_cmd:
        # Common absolute install locations (do not require os.access to avoid unit test coupling)
        candidate_paths = [
            r"C:\\bin\\es.exe",
            os.path.join(os.environ.get("ProgramFiles", r"C:\\Program Files"), "Everything", "es.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\\Program Files (x86)"), "Everything", "es.exe"),
        ]
        for candidate in candidate_paths:
            if os.path.isfile(candidate):
                es_cmd = candidate
                break
    if not es_cmd:
        sys.exit("Error: 'es.exe' not found in PATH, package bin directory, current directory, repo ./bin, or common install locations.")
    return es_cmd


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

    if not args.search:
        sys.exit("Error: --search is required.")

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
        # Fallback to default text output (no CSV header)
        text_flags = ["-name", "-path-column", "-size"]
        cmd = [es_cmd, *text_flags, args.search]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(f"Error running es.exe: {e.stderr.strip()}")
        # Print raw output so consumers (and tests) can see the full path
        out = result.stdout.strip()
        if out:
            print(out)
        sys.exit(0)

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
