#!/usr/bin/env python3
r"""
pyeverything.dll

This script uses the Everything DLL (Everything64.dll or Everything32.dll) to retrieve a list
of files matching a given search query, or runs a connectivity test by searching for
C:\Windows\System32\drivers\etc\hosts.

It auto-detects Python architecture (32-bit vs 64-bit) and loads the matching DLL from the
current directory or PATH, then uses the Everything SDK functions via ctypes.

Features:
  - Auto-detect Python bitness and load corresponding Everything DLL
  - Search with --search, --offset, --count options
  - --all-fields option to request all supported result data fields
  - --json option to output results in JSON format
  - Test mode (--test) verifies hosts file indexing and size > 1 by exact matching
  - Enables full-path matching so searches on complete paths work
  - Fallback: compares indexed size vs actual filesystem size for clearer behavior

Requirements:
  - Place Everything64.dll (64-bit) or Everything32.dll (32-bit) in PATH or current directory
"""
import argparse
import os as pydll_os  # Use an alias for os module
import sys
import json
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

# Everything SDK sort constants (match Everything.h)
EVERYTHING_SORT_NAME_ASCENDING                     = 1
EVERYTHING_SORT_NAME_DESCENDING                    = 2
EVERYTHING_SORT_PATH_ASCENDING                     = 3
EVERYTHING_SORT_PATH_DESCENDING                    = 4
EVERYTHING_SORT_SIZE_ASCENDING                     = 5
EVERYTHING_SORT_SIZE_DESCENDING                    = 6
EVERYTHING_SORT_EXTENSION_ASCENDING                = 7
EVERYTHING_SORT_EXTENSION_DESCENDING               = 8
EVERYTHING_SORT_TYPE_NAME_ASCENDING                = 9
EVERYTHING_SORT_TYPE_NAME_DESCENDING               = 10
EVERYTHING_SORT_DATE_CREATED_ASCENDING             = 11
EVERYTHING_SORT_DATE_CREATED_DESCENDING            = 12
EVERYTHING_SORT_DATE_MODIFIED_ASCENDING            = 13
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING           = 14
EVERYTHING_SORT_ATTRIBUTES_ASCENDING               = 15
EVERYTHING_SORT_ATTRIBUTES_DESCENDING              = 16
EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING       = 17
EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING      = 18
EVERYTHING_SORT_RUN_COUNT_ASCENDING                = 19
EVERYTHING_SORT_RUN_COUNT_DESCENDING               = 20
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING    = 21
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING   = 22
EVERYTHING_SORT_DATE_ACCESSED_ASCENDING            = 23
EVERYTHING_SORT_DATE_ACCESSED_DESCENDING           = 24
EVERYTHING_SORT_DATE_RUN_ASCENDING                 = 25
EVERYTHING_SORT_DATE_RUN_DESCENDING                = 26

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
    """Load the 64-bit Everything DLL only (Everything64.dll).

    Searches the package's `bin` directory, current working directory,
    then the system PATH. Exits with an error if not found.
    """
    dll_name = "Everything64.dll"

    # Search in the 'bin' directory relative to the script's location
    script_dir = pydll_os.path.dirname(pydll_os.path.abspath(__file__))
    bin_dir = pydll_os.path.join(script_dir, "bin")
    path = pydll_os.path.join(bin_dir, dll_name)
    if pydll_os.path.isfile(path):
        try:
            return ctypes.WinDLL(path)
        except OSError:
            pass

    # Search in the current working directory
    cwd = pydll_os.getcwd()
    path = pydll_os.path.join(cwd, dll_name)
    if pydll_os.path.isfile(path):
        try:
            return ctypes.WinDLL(path)
        except OSError:
            pass

    # Search in PATH
    try:
        return ctypes.WinDLL(dll_name)
    except OSError:
        sys.exit(
            "Error: Could not load Everything64.dll.\n"
            "Please ensure Everything64.dll is in PATH, the package's bin directory, or the current directory."
        )

def init_functions(dll):
    # Setters
    dll.Everything_SetSearchW.argtypes                   = [wintypes.LPCWSTR]
    dll.Everything_SetSearchA.argtypes                   = [wintypes.LPCSTR]
    dll.Everything_SetMatchPath.argtypes                 = [wintypes.BOOL]
    dll.Everything_SetMatchCase.argtypes                 = [wintypes.BOOL]
    dll.Everything_SetMatchWholeWord.argtypes            = [wintypes.BOOL]
    dll.Everything_SetRegex.argtypes                     = [wintypes.BOOL]
    dll.Everything_SetMax.argtypes                       = [wintypes.DWORD]
    dll.Everything_SetOffset.argtypes                    = [wintypes.DWORD]
    dll.Everything_SetRequestFlags.argtypes              = [wintypes.DWORD]
    dll.Everything_SetSort.argtypes                      = [wintypes.DWORD]
    dll.Everything_SetReplyWindow.argtypes               = [wintypes.HWND]

    # Getters
    dll.Everything_GetMatchPath.restype                  = wintypes.BOOL
    dll.Everything_GetMatchCase.restype                  = wintypes.BOOL
    dll.Everything_GetMatchWholeWord.restype             = wintypes.BOOL
    dll.Everything_GetRegex.restype                      = wintypes.BOOL
    dll.Everything_GetMax.restype                        = wintypes.DWORD
    dll.Everything_GetOffset.restype                     = wintypes.DWORD
    dll.Everything_GetSort.restype                       = wintypes.DWORD
    dll.Everything_GetRequestFlags.restype               = wintypes.DWORD
    dll.Everything_GetSearchW.restype                    = wintypes.LPCWSTR
    dll.Everything_GetSearchA.restype                    = wintypes.LPCSTR
    dll.Everything_GetNumResults.restype                 = wintypes.DWORD
    dll.Everything_GetLastError.restype                  = wintypes.DWORD
    dll.Everything_GetReplyWindow.restype                = wintypes.HWND
    dll.Everything_GetTargetMachine.restype              = wintypes.DWORD

    # Query
    dll.Everything_QueryW.argtypes                       = [wintypes.BOOL]
    dll.Everything_QueryW.restype                        = wintypes.BOOL
    dll.Everything_QueryA.argtypes                       = [wintypes.BOOL]
    dll.Everything_QueryA.restype                        = wintypes.BOOL
    dll.Everything_IsQueryReply.argtypes                 = [wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM, wintypes.DWORD]
    dll.Everything_IsQueryReply.restype                  = wintypes.BOOL

    # Results
    dll.Everything_SortResultsByPath.argtypes            = []
    dll.Everything_GetResultFullPathNameW.argtypes       = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
    dll.Everything_GetResultFullPathNameW.restype        = wintypes.DWORD
    dll.Everything_GetResultFullPathNameA.argtypes       = [wintypes.DWORD, wintypes.LPSTR, wintypes.DWORD]
    dll.Everything_GetResultFullPathNameA.restype        = wintypes.DWORD
    dll.Everything_GetResultFileNameW.argtypes           = [wintypes.DWORD]
    dll.Everything_GetResultFileNameW.restype            = wintypes.LPCWSTR
    dll.Everything_GetResultFileNameA.argtypes           = [wintypes.DWORD]
    dll.Everything_GetResultFileNameA.restype            = wintypes.LPCSTR
    dll.Everything_GetResultSize.argtypes                = [wintypes.DWORD, ctypes.POINTER(ctypes.c_ulonglong)]
    dll.Everything_GetResultSize.restype                 = wintypes.BOOL
    dll.Everything_GetResultExtensionW.argtypes          = [wintypes.DWORD]
    dll.Everything_GetResultExtensionW.restype           = wintypes.LPCWSTR
    dll.Everything_GetResultDateCreated.argtypes         = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateCreated.restype          = wintypes.BOOL
    dll.Everything_GetResultDateModified.argtypes        = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateModified.restype         = wintypes.BOOL
    dll.Everything_GetResultDateAccessed.argtypes        = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateAccessed.restype         = wintypes.BOOL
    dll.Everything_GetResultAttributes.argtypes          = [wintypes.DWORD]
    dll.Everything_GetResultAttributes.restype           = wintypes.DWORD
    dll.Everything_GetResultFileListFileNameW.argtypes   = [wintypes.DWORD]
    dll.Everything_GetResultFileListFileNameW.restype    = wintypes.LPCWSTR
    dll.Everything_GetResultFileListFileNameA.argtypes   = [wintypes.DWORD]
    dll.Everything_GetResultFileListFileNameA.restype    = wintypes.LPCSTR
    dll.Everything_GetResultRunCount.argtypes            = [wintypes.DWORD]
    dll.Everything_GetResultRunCount.restype             = wintypes.DWORD
    dll.Everything_GetResultDateRun.argtypes             = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateRun.restype              = wintypes.BOOL
    dll.Everything_GetResultDateRecentlyChanged.argtypes = [wintypes.DWORD, ctypes.POINTER(wintypes.FILETIME)]
    dll.Everything_GetResultDateRecentlyChanged.restype  = wintypes.BOOL
    dll.Everything_GetResultHighlightedFileNameW.argtypes= [wintypes.DWORD]
    dll.Everything_GetResultHighlightedFileNameW.restype = wintypes.LPCWSTR
    dll.Everything_GetResultHighlightedPathW.argtypes    = [wintypes.DWORD]
    dll.Everything_GetResultHighlightedPathW.restype     = wintypes.LPCWSTR
    dll.Everything_GetResultHighlightedFullPathAndFileNameW.argtypes = [wintypes.DWORD]
    dll.Everything_GetResultHighlightedFullPathAndFileNameW.restype  = wintypes.LPCWSTR

    # Version
    dll.Everything_GetMajorVersion.restype               = wintypes.DWORD
    dll.Everything_GetMinorVersion.restype               = wintypes.DWORD
    dll.Everything_GetRevision.restype                   = wintypes.DWORD
    dll.Everything_GetBuildNumber.restype                = wintypes.DWORD

    # Status
    dll.Everything_IsDBLoaded.restype                    = wintypes.BOOL
    dll.Everything_IsAdmin.restype                       = wintypes.BOOL
    dll.Everything_IsAppData.restype                     = wintypes.BOOL

    # Control
    dll.Everything_CleanUp.argtypes                      = []
    dll.Everything_Reset.argtypes                        = []
    dll.Everything_Exit.argtypes                         = []

def parse_args():
    parser = argparse.ArgumentParser(
        description="Use Everything DLL to list files via the Everything SDK"
    )
    parser.add_argument("--search", required=False,
                        help="Search pattern (Everything query syntax)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Result offset (zero-based)")
    parser.add_argument("--count", type=int, default=100,
                        help="Maximum number of results to return")
    parser.add_argument("--all-fields", action="store_true",
                        help="Request all available fields from the Everything SDK")
    parser.add_argument("--json", action="store_true",
                        help="Output results in JSON format")
    # Note: connectivity checks moved to tests; CLI focuses on search only.
    return parser.parse_args()

def filetime_to_dt(ft):
    ticks = (ft.dwHighDateTime << 32) | ft.dwLowDateTime
    if ticks == 0:
        return None
    try:
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ticks // 10)
    except OverflowError:
        return None

def _get_wstring_field(dll, func_name, index):
    """Compatibility getter: try buffer API then pointer API."""
    func = getattr(dll, func_name)
    try:
        buf = ctypes.create_unicode_buffer(260)
        func(index, buf, 260)
        return buf.value
    except Exception:
        try:
            ptr = func(index)
            return ptr if ptr else ""
        except Exception:
            return ""

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
        name = pydll_os.path.basename(path)
        if all_fields:
            ext = _get_wstring_field(dll, 'Everything_GetResultExtensionW', i)
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
            flfn = _get_wstring_field(dll, 'Everything_GetResultFileListFileNameW', i)
            rc = dll.Everything_GetResultRunCount(i)
            ft_run = wintypes.FILETIME()
            dll.Everything_GetResultDateRun(i, ctypes.byref(ft_run))
            dr = filetime_to_dt(ft_run)
            ft_recent = wintypes.FILETIME()
            dll.Everything_GetResultDateRecentlyChanged(i, ctypes.byref(ft_recent))
            drc = filetime_to_dt(ft_recent)
            hfn = _get_wstring_field(dll, 'Everything_GetResultHighlightedFileNameW', i)
            hp = _get_wstring_field(dll, 'Everything_GetResultHighlightedPathW', i)
            hfp = _get_wstring_field(dll, 'Everything_GetResultHighlightedFullPathAndFileNameW', i)
            results.append({
                "name": name,
                "path": path,
                "size": size,
                "extension": ext,
                "date_created": dc.isoformat() if dc else None,
                "date_modified": dm.isoformat() if dm else None,
                "date_accessed": da.isoformat() if da else None,
                "attributes": attr,
                "list_file_name": flfn,
                "run_count": rc,
                "date_run": dr.isoformat() if dr else None,
                "date_recently_changed": drc.isoformat() if drc else None,
                "highlighted_file_name": hfn,
                "highlighted_path": hp,
                "highlighted_full_path": hfp
            })
        else:
            results.append({"name": name, "path": path, "size": size})
    dll.Everything_CleanUp()
    return results

def main():
    args = parse_args()
    dll = load_everything_dll()
    init_functions(dll)

    # 通常モード: --json フラグで JSON、それ以外はタブ区切りテキスト
    if not args.search:
        sys.exit("Error: --search is required.")
    results = run_search(dll, args.search, args.offset, args.count, all_fields=args.all_fields)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for entry in results:
            print("\t".join(str(v) for v in entry.values()))

if __name__ == '__main__':
    main()
