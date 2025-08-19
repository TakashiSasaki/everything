#!/usr/bin/env python3
"""
pyeverything.dll_class

Self-contained Everything DLL client that does not depend on pyeverything.dll.

Policy:
- 64-bit only (Everything64.dll).
- Load order: package bin (pyeverything/bin/Everything64.dll) → CWD → PATH.
- Windows-only; raises a clear error on non-Windows platforms.

Output conventions (kept consistent with current DLL CLI):
- search() returns dicts with name (basename), path (full path), size, and
  optional metadata when all_fields=True.
"""
import ctypes
import argparse
import json
import datetime
import os
import sys
from ctypes import wintypes
from typing import List, Dict, Optional

# Everything SDK request flags (per Everything.h)
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
EVERYTHING_REQUEST_DATE_RUN = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000

# Everything SDK sort constants (match Everything.h)
EVERYTHING_SORT_NAME_ASCENDING = 1
EVERYTHING_SORT_NAME_DESCENDING = 2
EVERYTHING_SORT_PATH_ASCENDING = 3
EVERYTHING_SORT_PATH_DESCENDING = 4
EVERYTHING_SORT_SIZE_ASCENDING = 5
EVERYTHING_SORT_SIZE_DESCENDING = 6
EVERYTHING_SORT_EXTENSION_ASCENDING = 7
EVERYTHING_SORT_EXTENSION_DESCENDING = 8
EVERYTHING_SORT_TYPE_NAME_ASCENDING = 9
EVERYTHING_SORT_TYPE_NAME_DESCENDING = 10
EVERYTHING_SORT_DATE_CREATED_ASCENDING = 11
EVERYTHING_SORT_DATE_CREATED_DESCENDING = 12
EVERYTHING_SORT_DATE_MODIFIED_ASCENDING = 13
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING = 14
EVERYTHING_SORT_ATTRIBUTES_ASCENDING = 15
EVERYTHING_SORT_ATTRIBUTES_DESCENDING = 16
EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING = 17
EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING = 18
EVERYTHING_SORT_RUN_COUNT_ASCENDING = 19
EVERYTHING_SORT_RUN_COUNT_DESCENDING = 20
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING = 21
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING = 22
EVERYTHING_SORT_DATE_ACCESSED_ASCENDING = 23
EVERYTHING_SORT_DATE_ACCESSED_DESCENDING = 24
EVERYTHING_SORT_DATE_RUN_ASCENDING = 25
EVERYTHING_SORT_DATE_RUN_DESCENDING = 26

# Combined flag for all fields
EVERYTHING_REQUEST_ALL = (
    EVERYTHING_REQUEST_FILE_NAME
    | EVERYTHING_REQUEST_PATH
    | EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME
    | EVERYTHING_REQUEST_EXTENSION
    | EVERYTHING_REQUEST_SIZE
    | EVERYTHING_REQUEST_DATE_CREATED
    | EVERYTHING_REQUEST_DATE_MODIFIED
    | EVERYTHING_REQUEST_DATE_ACCESSED
    | EVERYTHING_REQUEST_ATTRIBUTES
    | EVERYTHING_REQUEST_FILE_LIST_FILE_NAME
    | EVERYTHING_REQUEST_RUN_COUNT
    | EVERYTHING_REQUEST_DATE_RUN
    | EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED
    | EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME
    | EVERYTHING_REQUEST_HIGHLIGHTED_PATH
    | EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME
)

_DLL_NAME = "Everything64.dll"
_BUF_CHARS = 260  # Keep parity with current CLI


def filetime_to_dt(ft: wintypes.FILETIME) -> Optional[datetime.datetime]:
    """Convert Windows FILETIME to datetime or None.

    FILETIME is 100-nanosecond intervals since January 1, 1601 (UTC).
    """
    ticks = (ft.dwHighDateTime << 32) | ft.dwLowDateTime
    if ticks == 0:
        return None
    try:
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ticks // 10)
    except OverflowError:
        return None


class EverythingDLL:
    """Core DLL client to interact with the Everything SDK.

    This class is Windows-only and enforces loading the 64-bit Everything DLL.
    """

    def __init__(self, dll_path: Optional[str] = None):
        if sys.platform != "win32":
            raise RuntimeError("EverythingDLL is only supported on Windows (win32).")
        self.dll = self._load_dll(dll_path)
        self._bind_functions()

    # Loader
    def _load_dll(self, dll_path: Optional[str]) -> ctypes.WinDLL:
        checks = []

        if dll_path:
            checks.append(dll_path)
            try:
                return ctypes.WinDLL(dll_path)
            except OSError as e:
                raise RuntimeError(f"Error loading {_DLL_NAME} from explicit path {dll_path}: {e}")

        # 1) package bin: pyeverything/bin/Everything64.dll
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bin_dir = os.path.join(script_dir, "bin")
        pkg_bin = os.path.join(bin_dir, _DLL_NAME)
        checks.append(pkg_bin)
        if os.path.isfile(pkg_bin):
            try:
                return ctypes.WinDLL(pkg_bin)
            except OSError:
                pass

        # 2) current working directory
        cwd = os.getcwd()
        cwd_path = os.path.join(cwd, _DLL_NAME)
        checks.append(cwd_path)
        if os.path.isfile(cwd_path):
            try:
                return ctypes.WinDLL(cwd_path)
            except OSError:
                pass

        # 3) PATH
        checks.append("PATH")
        try:
            return ctypes.WinDLL(_DLL_NAME)
        except OSError:
            msg = (
                "Error: Could not load Everything64.dll. Checked locations: "
                + ", ".join(checks)
            )
            raise RuntimeError(msg)

    # Binder
    def _bind_functions(self) -> None:
        dll = self.dll

        # Setters
        dll.Everything_SetSearchW.argtypes = [wintypes.LPCWSTR]
        dll.Everything_SetSearchA.argtypes = [wintypes.LPCSTR]
        dll.Everything_SetMatchPath.argtypes = [wintypes.BOOL]
        dll.Everything_SetMatchCase.argtypes = [wintypes.BOOL]
        dll.Everything_SetMatchWholeWord.argtypes = [wintypes.BOOL]
        dll.Everything_SetRegex.argtypes = [wintypes.BOOL]
        dll.Everything_SetMax.argtypes = [wintypes.DWORD]
        dll.Everything_SetOffset.argtypes = [wintypes.DWORD]
        dll.Everything_SetRequestFlags.argtypes = [wintypes.DWORD]
        dll.Everything_SetSort.argtypes = [wintypes.DWORD]
        dll.Everything_SetReplyWindow.argtypes = [wintypes.HWND]

        # Getters
        dll.Everything_GetMatchPath.restype = wintypes.BOOL
        dll.Everything_GetMatchCase.restype = wintypes.BOOL
        dll.Everything_GetMatchWholeWord.restype = wintypes.BOOL
        dll.Everything_GetRegex.restype = wintypes.BOOL
        dll.Everything_GetMax.restype = wintypes.DWORD
        dll.Everything_GetOffset.restype = wintypes.DWORD
        dll.Everything_GetSort.restype = wintypes.DWORD
        dll.Everything_GetRequestFlags.restype = wintypes.DWORD
        dll.Everything_GetSearchW.restype = wintypes.LPCWSTR
        dll.Everything_GetSearchA.restype = wintypes.LPCSTR
        dll.Everything_GetNumResults.restype = wintypes.DWORD
        dll.Everything_GetLastError.restype = wintypes.DWORD
        dll.Everything_GetReplyWindow.restype = wintypes.HWND
        dll.Everything_GetTargetMachine.restype = wintypes.DWORD

        # Query
        dll.Everything_QueryW.argtypes = [wintypes.BOOL]
        dll.Everything_QueryW.restype = wintypes.BOOL
        dll.Everything_QueryA.argtypes = [wintypes.BOOL]
        dll.Everything_QueryA.restype = wintypes.BOOL
        dll.Everything_IsQueryReply.argtypes = [
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
            wintypes.DWORD,
        ]
        dll.Everything_IsQueryReply.restype = wintypes.BOOL

        # Results
        dll.Everything_SortResultsByPath.argtypes = []
        dll.Everything_GetResultFullPathNameW.argtypes = [
            wintypes.DWORD,
            wintypes.LPWSTR,
            wintypes.DWORD,
        ]
        dll.Everything_GetResultFullPathNameW.restype = wintypes.DWORD
        dll.Everything_GetResultFullPathNameA.argtypes = [
            wintypes.DWORD,
            wintypes.LPSTR,
            wintypes.DWORD,
        ]
        dll.Everything_GetResultFullPathNameA.restype = wintypes.DWORD
        dll.Everything_GetResultFileNameW.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultFileNameW.restype = wintypes.LPCWSTR
        dll.Everything_GetResultFileNameA.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultFileNameA.restype = wintypes.LPCSTR
        dll.Everything_GetResultSize.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        dll.Everything_GetResultSize.restype = wintypes.BOOL
        dll.Everything_GetResultExtensionW.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultExtensionW.restype = wintypes.LPCWSTR
        dll.Everything_GetResultDateCreated.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(wintypes.FILETIME),
        ]
        dll.Everything_GetResultDateCreated.restype = wintypes.BOOL
        dll.Everything_GetResultDateModified.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(wintypes.FILETIME),
        ]
        dll.Everything_GetResultDateModified.restype = wintypes.BOOL
        dll.Everything_GetResultDateAccessed.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(wintypes.FILETIME),
        ]
        dll.Everything_GetResultDateAccessed.restype = wintypes.BOOL
        dll.Everything_GetResultAttributes.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultAttributes.restype = wintypes.DWORD
        dll.Everything_GetResultFileListFileNameW.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultFileListFileNameW.restype = wintypes.LPCWSTR
        dll.Everything_GetResultFileListFileNameA.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultFileListFileNameA.restype = wintypes.LPCSTR
        dll.Everything_GetResultRunCount.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultRunCount.restype = wintypes.DWORD
        dll.Everything_GetResultDateRun.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(wintypes.FILETIME),
        ]
        dll.Everything_GetResultDateRun.restype = wintypes.BOOL
        dll.Everything_GetResultDateRecentlyChanged.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(wintypes.FILETIME),
        ]
        dll.Everything_GetResultDateRecentlyChanged.restype = wintypes.BOOL
        dll.Everything_GetResultHighlightedFileNameW.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultHighlightedFileNameW.restype = wintypes.LPCWSTR
        dll.Everything_GetResultHighlightedPathW.argtypes = [wintypes.DWORD]
        dll.Everything_GetResultHighlightedPathW.restype = wintypes.LPCWSTR
        dll.Everything_GetResultHighlightedFullPathAndFileNameW.argtypes = [
            wintypes.DWORD,
        ]
        dll.Everything_GetResultHighlightedFullPathAndFileNameW.restype = (
            wintypes.LPCWSTR
        )

        # Version
        dll.Everything_GetMajorVersion.restype = wintypes.DWORD
        dll.Everything_GetMinorVersion.restype = wintypes.DWORD
        dll.Everything_GetRevision.restype = wintypes.DWORD
        dll.Everything_GetBuildNumber.restype = wintypes.DWORD

        # Status
        dll.Everything_IsDBLoaded.restype = wintypes.BOOL
        dll.Everything_IsAdmin.restype = wintypes.BOOL
        dll.Everything_IsAppData.restype = wintypes.BOOL

        # Control
        dll.Everything_CleanUp.argtypes = []
        dll.Everything_Reset.argtypes = []
        dll.Everything_Exit.argtypes = []

    # Helpers
    def _get_wstring_field(self, func_name: str, index: int) -> str:
        """Compatibility getter: try buffer API (if available) then pointer API."""
        func = getattr(self.dll, func_name)
        try:
            buf = ctypes.create_unicode_buffer(_BUF_CHARS)
            func(index, buf, _BUF_CHARS)
            return buf.value
        except Exception:
            try:
                ptr = func(index)
                return ptr if ptr else ""
            except Exception:
                return ""

    # Public surface
    def search(
        self,
        query: str,
        offset: int = 0,
        count: int = 100,
        all_fields: bool = False,
    ) -> List[Dict[str, object]]:
        """Execute a search through the Everything SDK.

        Returns a list of dicts with keys:
        - name: basename
        - path: full path
        - size: integer bytes
        - plus optional fields when all_fields is True
        """
        self.dll.Everything_SetSearchW(query)
        self.dll.Everything_SetMatchPath(True)
        flags = (
            EVERYTHING_REQUEST_ALL
            if all_fields
            else (
                EVERYTHING_REQUEST_FILE_NAME
                | EVERYTHING_REQUEST_PATH
                | EVERYTHING_REQUEST_SIZE
            )
        )
        self.dll.Everything_SetRequestFlags(flags)
        self.dll.Everything_SetOffset(offset)
        self.dll.Everything_SetMax(count)
        if not self.dll.Everything_QueryW(True):
            raise RuntimeError("Error: Everything query failed.")

        total = self.dll.Everything_GetNumResults()
        results: List[Dict[str, object]] = []
        buf = ctypes.create_unicode_buffer(_BUF_CHARS)

        for i in range(total):
            self.dll.Everything_GetResultFullPathNameW(i, buf, _BUF_CHARS)
            full_path = buf.value
            size_var = ctypes.c_ulonglong()
            self.dll.Everything_GetResultSize(i, ctypes.byref(size_var))
            size = size_var.value
            name = os.path.basename(full_path)
            if all_fields:
                ext = self._get_wstring_field("Everything_GetResultExtensionW", i)
                ft_created = wintypes.FILETIME()
                self.dll.Everything_GetResultDateCreated(i, ctypes.byref(ft_created))
                dc = filetime_to_dt(ft_created)
                ft_modified = wintypes.FILETIME()
                self.dll.Everything_GetResultDateModified(i, ctypes.byref(ft_modified))
                dm = filetime_to_dt(ft_modified)
                ft_accessed = wintypes.FILETIME()
                self.dll.Everything_GetResultDateAccessed(i, ctypes.byref(ft_accessed))
                da = filetime_to_dt(ft_accessed)
                attr = self.dll.Everything_GetResultAttributes(i)
                flfn = self._get_wstring_field("Everything_GetResultFileListFileNameW", i)
                rc = self.dll.Everything_GetResultRunCount(i)
                ft_run = wintypes.FILETIME()
                self.dll.Everything_GetResultDateRun(i, ctypes.byref(ft_run))
                dr = filetime_to_dt(ft_run)
                ft_recent = wintypes.FILETIME()
                self.dll.Everything_GetResultDateRecentlyChanged(
                    i, ctypes.byref(ft_recent)
                )
                drc = filetime_to_dt(ft_recent)
                hfn = self._get_wstring_field(
                    "Everything_GetResultHighlightedFileNameW", i
                )
                hp = self._get_wstring_field("Everything_GetResultHighlightedPathW", i)
                hfp = self._get_wstring_field(
                    "Everything_GetResultHighlightedFullPathAndFileNameW", i
                )
                results.append(
                    {
                        "name": name,
                        "path": full_path,
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
                        "highlighted_full_path": hfp,
                    }
                )
            else:
                results.append({"name": name, "path": full_path, "size": size})

        self.dll.Everything_CleanUp()
        return results

    # Thin pass-throughs / utilities
    def set_match_path(self, enable: bool) -> None:
        self.dll.Everything_SetMatchPath(bool(enable))

    def set_match_case(self, enable: bool) -> None:
        self.dll.Everything_SetMatchCase(bool(enable))

    def set_match_whole_word(self, enable: bool) -> None:
        self.dll.Everything_SetMatchWholeWord(bool(enable))

    def set_regex(self, enable: bool) -> None:
        self.dll.Everything_SetRegex(bool(enable))

    def set_max(self, max_results: int) -> None:
        self.dll.Everything_SetMax(int(max_results))

    def set_offset(self, offset: int) -> None:
        self.dll.Everything_SetOffset(int(offset))

    def set_sort(self, sort_type: int) -> None:
        self.dll.Everything_SetSort(int(sort_type))

    def sort_results_by_path(self) -> None:
        self.dll.Everything_SortResultsByPath()

    def cleanup(self) -> None:
        self.dll.Everything_CleanUp()

    def reset(self) -> None:
        self.dll.Everything_Reset()

    # Optional context manager
    def __enter__(self) -> "EverythingDLL":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.cleanup()
        finally:
            self.reset()


__all__ = [
    "EverythingDLL",
    # Flags
    "EVERYTHING_REQUEST_FILE_NAME",
    "EVERYTHING_REQUEST_PATH",
    "EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME",
    "EVERYTHING_REQUEST_EXTENSION",
    "EVERYTHING_REQUEST_SIZE",
    "EVERYTHING_REQUEST_DATE_CREATED",
    "EVERYTHING_REQUEST_DATE_MODIFIED",
    "EVERYTHING_REQUEST_DATE_ACCESSED",
    "EVERYTHING_REQUEST_ATTRIBUTES",
    "EVERYTHING_REQUEST_FILE_LIST_FILE_NAME",
    "EVERYTHING_REQUEST_RUN_COUNT",
    "EVERYTHING_REQUEST_DATE_RUN",
    "EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED",
    "EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME",
    "EVERYTHING_REQUEST_HIGHLIGHTED_PATH",
    "EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME",
    "EVERYTHING_REQUEST_ALL",
    # Sorts
    "EVERYTHING_SORT_NAME_ASCENDING",
    "EVERYTHING_SORT_NAME_DESCENDING",
    "EVERYTHING_SORT_PATH_ASCENDING",
    "EVERYTHING_SORT_PATH_DESCENDING",
    "EVERYTHING_SORT_SIZE_ASCENDING",
    "EVERYTHING_SORT_SIZE_DESCENDING",
    "EVERYTHING_SORT_EXTENSION_ASCENDING",
    "EVERYTHING_SORT_EXTENSION_DESCENDING",
    "EVERYTHING_SORT_TYPE_NAME_ASCENDING",
    "EVERYTHING_SORT_TYPE_NAME_DESCENDING",
    "EVERYTHING_SORT_DATE_CREATED_ASCENDING",
    "EVERYTHING_SORT_DATE_CREATED_DESCENDING",
    "EVERYTHING_SORT_DATE_MODIFIED_ASCENDING",
    "EVERYTHING_SORT_DATE_MODIFIED_DESCENDING",
    "EVERYTHING_SORT_ATTRIBUTES_ASCENDING",
    "EVERYTHING_SORT_ATTRIBUTES_DESCENDING",
    "EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING",
    "EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING",
    "EVERYTHING_SORT_RUN_COUNT_ASCENDING",
    "EVERYTHING_SORT_RUN_COUNT_DESCENDING",
    "EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING",
    "EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING",
    "EVERYTHING_SORT_DATE_ACCESSED_ASCENDING",
    "EVERYTHING_SORT_DATE_ACCESSED_DESCENDING",
    "EVERYTHING_SORT_DATE_RUN_ASCENDING",
    "EVERYTHING_SORT_DATE_RUN_DESCENDING",
    # Utils
    "filetime_to_dt",
    # CLI
    "main",
]


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Use Everything DLL to list files or run a connectivity test",
    )
    parser.add_argument(
        "--search",
        required=False,
        help="Search pattern (Everything query syntax)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Result offset (zero-based)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Maximum number of results to return",
    )
    parser.add_argument(
        "--all-fields",
        action="store_true",
        help="Request all available fields from the Everything SDK",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run connectivity test against hosts file",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    try:
        client = EverythingDLL()
    except Exception as e:
        sys.exit(str(e))

    # Test mode
    if args.test:
        hostfile = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
        # Try a few robust queries to avoid false negatives on cold indexes
        queries = [
            hostfile,
            r'path:"\\\\windows\\\\system32\\\\drivers\\\\etc" hosts',
            "windows system32 drivers etc hosts",
        ]
        results = []
        try:
            for q in queries:
                results = client.search(q, 0, 50, all_fields=args.all_fields)
                if results:
                    break
        except Exception as e:
            sys.exit(str(e))
        if not results:
            sys.exit("Test failed: no search results returned for hosts file.")
        # Prefer exact match, otherwise relax to substring on normalized path
        match = next(
            (e for e in results if str(e.get("path", "")).lower() == hostfile.lower()),
            None,
        )
        if not match:
            canon = hostfile.lower().replace("/", "\\")
            for e in results:
                p = str(e.get("path", "")).lower().replace("/", "\\")
                if canon in p:
                    match = e
                    break
        if not match:
            sys.exit("Test failed: hosts file not found among search results.")
        size = match.get("size", 0)
        if size == 0:
            actual = os.path.getsize(hostfile) if os.path.isfile(hostfile) else 0
            if actual > 1:
                msg = {"warning": f"indexed size 0, actual size {actual}."}
                if args.json:
                    print(json.dumps(msg, ensure_ascii=False, indent=2))
                else:
                    print(f"Warning: indexed size 0, actual size {actual}.")
                sys.exit(0)
            sys.exit("Test failed: hosts file size is zero both in index and on disk.")
        if args.json:
            print(json.dumps({"passed": True, "size": size}, ensure_ascii=False, indent=2))
        else:
            print(f"Test passed: hosts file found, size {size}.")
        sys.exit(0)

    # Normal mode
    if not args.search:
        sys.exit("Error: --search is required unless --test is specified.")
    try:
        results = client.search(
            args.search, args.offset, args.count, all_fields=args.all_fields
        )
    except Exception as e:
        sys.exit(str(e))
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for entry in results:
            print("\t".join(str(v) for v in entry.values()))


if __name__ == "__main__":
    main()
