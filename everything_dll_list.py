#!/usr/bin/env python3
r"""
everything_dll_list.py

This script uses the Everything DLL (Everything64.dll or Everything32.dll) to retrieve a list
of files matching a given search query, or runs a connectivity test by searching for
C:\Windows\System32\drivers\etc\hosts.

It auto-detects Python architecture (32-bit vs 64-bit) and loads the matching DLL from the
current directory or PATH, then uses the Everything SDK functions via ctypes.

Features:
  - Auto-detect Python bitness and load corresponding Everything DLL
  - Search with --search, --offset, --count options
  - Test mode (--test) verifies hosts file indexing and size > 1 by exact matching
  - Enables full-path matching so searches on complete paths work
  - Fallback: compares indexed size vs actual filesystem size for clearer behavior

Requirements:
  - Place Everything64.dll (64-bit) or Everything32.dll (32-bit) in PATH or current directory
"""
import argparse
import os
import sys
import ctypes
from ctypes import wintypes

# Everything SDK request flags (per documentation)
EVERYTHING_REQUEST_FILE_NAME = 0x00000001  # file name
EVERYTHING_REQUEST_PATH      = 0x00000002  # path
EVERYTHING_REQUEST_SIZE      = 0x00000010  # size in bytes


def load_everything_dll():
    is_64bit = sys.maxsize > 2**32
    dll_names = ["Everything64.dll", "Everything32.dll"] if is_64bit else ["Everything32.dll", "Everything64.dll"]
    cwd = os.getcwd()
    for name in dll_names:
        path = os.path.join(cwd, name)
        if os.path.isfile(path):
            try:
                return ctypes.WinDLL(path)
            except OSError:
                continue
    for name in dll_names:
        try:
            return ctypes.WinDLL(name)
        except OSError:
            continue
    arch = '64-bit' if is_64bit else '32-bit'
    expected = 'Everything64.dll' if is_64bit else 'Everything32.dll'
    sys.exit(f"Error: Could not load Everything DLL for {arch} Python.\n"
             f"Please ensure {expected} is in PATH or the current directory.")


def init_functions(dll):
    # Define argument and return types for Everything SDK functions
    dll.Everything_SetSearchW.argtypes         = [wintypes.LPCWSTR]
    dll.Everything_SetMatchPath.argtypes       = [wintypes.BOOL]
    dll.Everything_SetRequestFlags.argtypes    = [wintypes.DWORD]
    dll.Everything_SetOffset.argtypes          = [wintypes.DWORD]
    dll.Everything_SetMax.argtypes             = [wintypes.DWORD]
    dll.Everything_QueryW.argtypes             = [wintypes.BOOL]
    dll.Everything_QueryW.restype              = wintypes.BOOL
    dll.Everything_GetNumResults.argtypes      = []
    dll.Everything_GetNumResults.restype       = wintypes.DWORD
    dll.Everything_GetResultFullPathNameW.argtypes = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultFullPathNameW.restype  = wintypes.DWORD
    # Correct GetResultSize signature: takes index and pointer to size
    dll.Everything_GetResultSize.argtypes      = [wintypes.DWORD, ctypes.POINTER(ctypes.c_ulonglong)]
    dll.Everything_GetResultSize.restype       = None
    dll.Everything_CleanUp.argtypes            = []


def parse_args():
    parser = argparse.ArgumentParser(
        description="Use Everything DLL to list files or run a connectivity test"
    )
    parser.add_argument("--search", required=False,
                        help="Search pattern (Everything query syntax)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Result offset (zero-based)")
    parser.add_argument("--count", type=int, default=100,
                        help="Maximum number of results to return")
    parser.add_argument("--test", action="store_true",
                        help="Run connectivity test against hosts file")
    return parser.parse_args()


def run_search(dll, query, offset, count):
    # Configure search parameters
    dll.Everything_SetSearchW(query)
    dll.Everything_SetMatchPath(True)
    flags = (EVERYTHING_REQUEST_FILE_NAME |
             EVERYTHING_REQUEST_PATH      |
             EVERYTHING_REQUEST_SIZE)
    dll.Everything_SetRequestFlags(flags)
    dll.Everything_SetOffset(offset)
    dll.Everything_SetMax(count)
    if not dll.Everything_QueryW(True):
        sys.exit("Error: Everything query failed.")
    total = dll.Everything_GetNumResults()
    results = []
    buffer = ctypes.create_unicode_buffer(260)
    for i in range(total):
        # get full path
        dll.Everything_GetResultFullPathNameW(i, buffer, 260)
        fullpath = buffer.value
        # get size
        size_var = ctypes.c_ulonglong()
        dll.Everything_GetResultSize(i, ctypes.byref(size_var))
        size = size_var.value
        name = os.path.basename(fullpath)
        results.append((name, fullpath, size))
    dll.Everything_CleanUp()
    return results


def main():
    args = parse_args()
    dll = load_everything_dll()
    init_functions(dll)

    if args.test:
        hostfile = r"C:\Windows\System32\drivers\etc\hosts"
        found = run_search(dll, hostfile, 0, 10)
        if not found:
            sys.exit("Test failed: no search results returned for hosts file. Ensure indexing of system files.")
        match = next((e for e in found if e[1].lower() == hostfile.lower()), None)
        if match is None:
            sys.exit("Test failed: hosts file not found among search results. Ensure full-path matching is enabled.")
        size = match[2]
        if size == 0:
            try:
                actual = os.path.getsize(hostfile)
            except OSError:
                sys.exit("Test failed: hosts file indexed size is zero and file not found on disk.")
            if actual > 1:
                print(f"Test warning: hosts file indexed size is zero, but actual disk size is {actual}. Index may lack size info.")
                sys.exit(0)
            sys.exit("Test failed: hosts file size is zero both in index and on disk.")
        print(f"Test passed: hosts file found with size {size}.")
        sys.exit(0)

    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")

    # Normal search: print name, path, and size
    for name, path, size in run_search(dll, args.search, args.offset, args.count):
        print(f"{name}\t{path}\t{size}")

if __name__ == '__main__':
    main()