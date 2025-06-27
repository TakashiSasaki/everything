#!/usr/bin/env python3
"""
pyeverything.everything

This module provides the Everything class for interacting with the Everything search engine.
"""
import ctypes
from ctypes import wintypes
import datetime
import os
import sys
from .dll import load_everything_dll, init_functions, filetime_to_dt
from .dll import EVERYTHING_REQUEST_FILE_NAME, EVERYTHING_REQUEST_PATH, EVERYTHING_REQUEST_SIZE, EVERYTHING_REQUEST_ALL

class Everything:
    """A class to interact with the Everything search engine."""

    def __init__(self):
        """Initializes the Everything class and loads the DLL."""
        self.dll = load_everything_dll()
        init_functions(self.dll)

    def search(self, query, offset=0, count=100, all_fields=False):
        """
        Performs a search using the Everything search engine.

        Args:
            query (str): The search query.
            offset (int): The offset of the results.
            count (int): The maximum number of results to return.
            all_fields (bool): Whether to request all available fields.

        Returns:
            list: A list of dictionaries representing the search results.
        """
        self.dll.Everything_SetSearchW(query)
        self.dll.Everything_SetMatchPath(True)
        flags = EVERYTHING_REQUEST_ALL if all_fields else (
            EVERYTHING_REQUEST_FILE_NAME |
            EVERYTHING_REQUEST_PATH |
            EVERYTHING_REQUEST_SIZE
        )
        self.dll.Everything_SetRequestFlags(flags)
        self.dll.Everything_SetOffset(offset)
        self.dll.Everything_SetMax(count)
        if not self.dll.Everything_QueryW(True):
            sys.exit("Error: Everything query failed.")
        total = self.dll.Everything_GetNumResults()
        results = []
        buf = ctypes.create_unicode_buffer(260)

        start_index = offset
        end_index = total

        if count != 0:
            end_index = min(offset + count, total)

        for i in range(start_index, end_index):
            self.dll.Everything_GetResultFullPathNameW(i, buf, 260)
            path = buf.value
            size_var = ctypes.c_ulonglong()
            self.dll.Everything_GetResultSize(i, ctypes.byref(size_var))
            size = size_var.value
            name = os.path.basename(path)
            if all_fields:
                ext_buf = ctypes.create_unicode_buffer(50)
                self.dll.Everything_GetResultExtensionW(i, ext_buf, 50)
                ext = ext_buf.value
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
                flfn_buf = ctypes.create_unicode_buffer(260)
                self.dll.Everything_GetResultFileListFileNameW(i, flfn_buf, 260)
                flfn = flfn_buf.value
                rc = self.dll.Everything_GetResultRunCount(i)
                ft_run = wintypes.FILETIME()
                self.dll.Everything_GetResultDateRun(i, ctypes.byref(ft_run))
                dr = filetime_to_dt(ft_run)
                ft_recent = wintypes.FILETIME()
                self.dll.Everything_GetResultDateRecentlyChanged(i, ctypes.byref(ft_recent))
                drc = filetime_to_dt(ft_recent)
                hfn_buf = ctypes.create_unicode_buffer(260)
                self.dll.Everything_GetResultHighlightedFileNameW(i, hfn_buf, 260)
                hfn = hfn_buf.value
                hp_buf = ctypes.create_unicode_buffer(260)
                self.dll.Everything_GetResultHighlightedPathW(i, hp_buf, 260)
                hp = hp_buf.value
                hfp_buf = ctypes.create_unicode_buffer(260)
                self.dll.Everything_GetResultHighlightedFullPathAndFileNameW(i, hfp_buf, 260)
                hfp = hfp_buf.value
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
        self.dll.Everything_CleanUp()
        self.dll.Everything_Reset()
        return results

    def set_match_case(self, enable: bool):
        """Enables or disables case-sensitive searching.

        Args:
            enable (bool): True for case-sensitive, False for case-insensitive.
        """
        self.dll.Everything_SetMatchCase(enable)

    def set_match_whole_word(self, enable: bool):
        """Enables or disables whole word matching.

        Args:
            enable (bool): True for whole word matching, False otherwise.
        """
        self.dll.Everything_SetMatchWholeWord(enable)

    def set_request_flags(self, flags: int):
        """Sets the request flags for the next search.

        Args:
            flags (int): The flags to set.
        """
        self.dll.Everything_SetRequestFlags(flags)

    def set_regex(self, enable: bool):
        """Enables or disables regex matching.

        Args:
            enable (bool): True for regex matching, False otherwise.
        """
        self.dll.Everything_SetRegex(enable)

    def set_max(self, max_results: int):
        """Sets the maximum number of results to return.

        Args:
            max_results (int): The maximum number of results.
        """
        self.dll.Everything_SetMax(max_results)

    def set_offset(self, offset: int):
        """Sets the offset for the next search.

        Args:
            offset (int): The offset of the results.
        """
        self.dll.Everything_SetOffset(offset)

    def sort_results_by_path(self):
        """Sorts the current search results by path, then by file name."""
        self.dll.Everything_SortResultsByPath()

    def set_sort_order(self, sort_type: int):
        """Sets the sort order for the next search.

        Args:
            sort_type (int): The type of sort to apply (e.g., EVERYTHING_SORT_DATE_MODIFIED_DESCENDING).
        """
        self.dll.Everything_SetSort(sort_type)

