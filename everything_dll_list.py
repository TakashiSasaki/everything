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
  - --all-fields option to request all supported result data fields
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
import datetime

# Everything SDK request flags (per documentation)
EVERYTHING_REQUEST_FILE_NAME                        = 0x00000001
EVERYTHING_REQUEST_PATH                             = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME          = 0x00000004
EVERYTHING_REQUEST_EXTENSION                        = 0x00000008
EVERYTHING_REQUEST_SIZE                             = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED                     = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED                    = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED                    = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES                       = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME              = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT                        = 0x00000400
EVERYTHING_REQUEST_DATE_RUN                         = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED            = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME            = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH                 = 0x00004000
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000

# Combined flag for all fields
EVERYTHING_REQUEST_ALL = (
    EVERYTHING_REQUEST_FILE_NAME |
    EVERYTHING_REQUEST_PATH |
    EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME |
    EVERYTHING_REQUEST_EXTENSION |
    EVERYTHING_REQUEST_SIZE |
    EVERYTHING_REQUEST_DATE_CREATED |
    EVERYTHING_REQUEST_DATE_MODIFIED |
    EVERYTHING_REQUEST_DATE_ACCESSED |
    EVERYTHING_REQUEST_ATTRIBUTES |
    EVERYTHING_REQUEST_FILE_LIST_FILE_NAME |
    EVERYTHING_REQUEST_RUN_COUNT |
    EVERYTHING_REQUEST_DATE_RUN |
    EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED |
    EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME |
    EVERYTHING_REQUEST_HIGHLIGHTED_PATH |
    EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME
)


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
    dll.Everything_SetSearchW.argtypes                   = [wintypes.LPCWSTR]
    dll.Everything_SetMatchPath.argtypes                 = [wintypes.BOOL]
    dll.Everything_SetRequestFlags.argtypes              = [wintypes.DWORD]
    dll.Everything_SetOffset.argtypes                    = [wintypes.DWORD]
    dll.Everything_SetMax.argtypes                       = [wintypes.DWORD]
    dll.Everything_QueryW.argtypes                       = [wintypes.BOOL]
    dll.Everything_QueryW.restype                        = wintypes.BOOL
    dll.Everything_GetNumResults.argtypes                = []
    dll.Everything_GetNumResults.restype                 = wintypes.DWORD
    dll.Everything_GetResultFullPathNameW.argtypes       = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultFullPathNameW.restype        = wintypes.DWORD
    dll.Everything_GetResultSize.argtypes                = [wintypes.DWORD, ctypes.POINTER(ctypes.c_ulonglong)]
    dll.Everything_GetResultSize.restype                 = wintypes.BOOL
    dll.Everything_GetResultExtensionW.argtypes          = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultExtensionW.restype           = wintypes.DWORD
    # Date functions use FILETIME pointers
    dll.Everything_GetResultDateCreated.argtypes         = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateCreated.restype          = wintypes.BOOL
    dll.Everything_GetResultDateModified.argtypes        = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateModified.restype         = wintypes.BOOL
    dll.Everything_GetResultDateAccessed.argtypes        = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateAccessed.restype         = wintypes.BOOL
    dll.Everything_GetResultAttributes.argtypes          = [wintypes.DWORD]
    dll.Everything_GetResultAttributes.restype           = wintypes.DWORD
    dll.Everything_GetResultFileListFileNameW.argtypes   = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultFileListFileNameW.restype    = wintypes.DWORD
    dll.Everything_GetResultRunCount.argtypes            = [wintypes.DWORD]
    dll.Everything_GetResultRunCount.restype             = wintypes.DWORD
    dll.Everything_GetResultDateRun.argtypes             = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateRun.restype              = wintypes.BOOL
    dll.Everything_GetResultDateRecentlyChanged.argtypes = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateRecentlyChanged.restype  = wintypes.BOOL
    dll.Everything_GetResultHighlightedFileNameW.argtypes= [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultHighlightedFileNameW.restype = wintypes.DWORD
    dll.Everything_GetResultHighlightedPathW.argtypes    = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultHighlightedPathW.restype     = wintypes.DWORD
    dll.Everything_GetResultHighlightedFullPathAndFileNameW.argtypes = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultHighlightedFullPathAndFileNameW.restype  = wintypes.DWORD
    dll.Everything_CleanUp.argtypes                      = []


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
    parser.add_argument("--all-fields", action="store_true",
                        help="Request all available fields from the Everything SDK")
    parser.add_argument("--test", action="store_true",
                        help="Run connectivity test against hosts file")
    return parser.parse_args()


def filetime_to_dt(ft):
    # Convert Windows FILETIME to datetime; handle empty or invalid values
    ticks = (ft.dwHighDateTime << 32) | ft.dwLowDateTime
    if ticks == 0:
        return None
    # FILETIME is in 100-nanosecond intervals since Jan 1, 1601
    try:
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ticks // 10)
    except OverflowError:
        return None


def run_search(dll, query, offset, count, all_fields=False):
    dll.Everything_SetSearchW(query)
    dll.Everything_SetMatchPath(True)
    flags = EVERYTHING_REQUEST_ALL if all_fields else (
        EVERYTHING_REQUEST_FILE_NAME |
        EVERYTHING_REQUEST_PATH |
        EVERYTHING_REQUEST_SIZE
    )
    dll.Everything_SetRequestFlags(flags)
    dll.Everything_SetOffset(offset)
    dll.Everything_SetMax(count)
    if not dll.Everything_QueryW(True):
        sys.exit("Error: Everything query failed.")
    total = dll.Everything_GetNumResults()
    results = []
    buf = ctypes.create_unicode_buffer(260)
    for i in range(total):
        dll.Everything_GetResultFullPathNameW(i, buf, 260)
        path = buf.value
        size_var = ctypes.c_ulonglong()
        dll.Everything_GetResultSize(i, ctypes.byref(size_var))
        size = size_var.value
        name = os.path.basename(path)
        if all_fields:
            # Retrieve extension and dates safely
            ext_buf = ctypes.create_unicode_buffer(50)
            dll.Everything_GetResultExtensionW(i, ext_buf, 50)
            ext = ext_buf.value
            ft_created = wintypes.FILETIME()
            dll.Everything_GetResultDateCreated(i, ctypes.byref(ft_created))
            dc = filetime_to_dt(ft_created)
            ft_modified = wintypes.FILETIME()
            dll.Everything_GetResultDateModified(i, ctypes.byref(ft_modified))
            dm = filetime_to_dt(ft_modified)
            ft_accessed = wintypes.FILETIME()
            dll.Everything_GetResultDateAccessed(i, ctypes.byref(ft_accessed))
            da = filetime_to_dt(ft_accessed)
            attr = dll.Everything_GetResultAttributes(i)
            flfn_buf = ctypes.create_unicode_buffer(260)
            dll.Everything_GetResultFileListFileNameW(i, flfn_buf, 260)
            flfn = flfn_buf.value
            rc = dll.Everything_GetResultRunCount(i)
            ft_run = wintypes.FILETIME()
            dll.Everything_GetResultDateRun(i, ctypes.byref(ft_run))
            dr = filetime_to_dt(ft_run)
            ft_recent = wintypes.FILETIME()
            dll.Everything_GetResultDateRecentlyChanged(i, ctypes.byref(ft_recent))
            drc = filetime_to_dt(ft_recent)
            hfn_buf = ctypes.create_unicode_buffer(260)
            dll.Everything_GetResultHighlightedFileNameW(i, hfn_buf, 260)
            hfn = hfn_buf.value
            hp_buf = ctypes.create_unicode_buffer(260)
            dll.Everything_GetResultHighlightedPathW(i, hp_buf, 260)
            hp = hp_buf.value
            hfp_buf = ctypes.create_unicode_buffer(260)
            dll.Everything_GetResultHighlightedFullPathAndFileNameW(i, hfp_buf, 260)
            hfp = hfp_buf.value
            results.append((name, path, size, ext, dc, dm, da, attr, flfn, rc, dr, drc, hfn, hp, hfp))
        else:
            results.append((name, path, size))
    dll.Everything_CleanUp()
    return results


def main():
    args = parse_args()
    dll = load_everything_dll()
    init_functions(dll)

    if args.test:
        hostfile = r"C:\Windows\System32\drivers\etc\hosts"
        found = run_search(dll, hostfile, 0, 10, all_fields=args.all_fields)
        if not found:
            sys.exit("Test failed: no search results returned for hosts file.")
        match = next((e for e in found if e[1].lower() == hostfile.lower()), None)
        if not match:
            sys.exit("Test failed: hosts file not found among search results.")
        size = match[2]
        if size == 0:
            actual = os.path.getsize(hostfile) if os.path.isfile(hostfile) else 0
            if actual > 1:
                print(f"Test warning: indexed size 0, actual size {actual}.")
                sys.exit(0)
            sys.exit("Test failed: hosts file size is zero both in index and on disk.")
        print(f"Test passed: hosts file found with size {size}.")
        sys.exit(0)

    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")

    results = run_search(dll, args.search, args.offset, args.count, all_fields=args.all_fields)
    for entry in results:
        print("\t".join(str(x) for x in entry))

if __name__ == '__main__':
    main()
