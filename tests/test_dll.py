import sys
import unittest
from unittest import mock
from io import StringIO
import json
import datetime
from typing import Any, Dict, List, Optional
from ctypes import wintypes  # Need to ensure wintypes is available or mocked

# Mock ctypes and wintypes if not on Windows
if sys.platform != 'win32':
    class MockWintypes:
        class FILETIME:
            dwLowDateTime: int = 0
            dwHighDateTime: int = 0

        LPCWSTR: Optional[str] = None
        BOOL: Optional[bool] = None
        DWORD: Optional[int] = None
        LPWSTR: Optional[str] = None
        POINTER: Any = None

    wintypes = MockWintypes()

    class MockCtypes:
        def WinDLL(self, *args: Any, **kwargs: Any) -> "MockDll":
            return MockDll()
        def create_unicode_buffer(self, size: int) -> Any:
            m: Any = mock.Mock()
            m.value = ""
            return m
        def c_ulonglong(self) -> Any:
            m: Any = mock.Mock()
            m.value = 0
            return m
        def byref(self, obj: Any) -> Any:  # Simplified for mocking
            return obj

    ctypes = MockCtypes()

# Mock DLL class
class MockDll:
    def __init__(self) -> None:
        self.Everything_SetSearchW: mock.Mock = mock.Mock()
        self.Everything_SetMatchPath: mock.Mock = mock.Mock()
        self.Everything_SetRequestFlags: mock.Mock = mock.Mock()
        self.Everything_SetOffset: mock.Mock = mock.Mock()
        self.Everything_SetMax: mock.Mock = mock.Mock()
        self.Everything_QueryW: mock.Mock = mock.Mock(return_value=True)
        self.Everything_GetNumResults: mock.Mock = mock.Mock()
        self.Everything_GetResultFullPathNameW: mock.Mock = mock.Mock()
        self.Everything_GetResultSize: mock.Mock = mock.Mock()
        self.Everything_GetResultExtensionW: mock.Mock = mock.Mock()
        self.Everything_GetResultDateCreated: mock.Mock = mock.Mock()
        self.Everything_GetResultDateModified: mock.Mock = mock.Mock()
        self.Everything_GetResultDateAccessed: mock.Mock = mock.Mock()
        self.Everything_GetResultAttributes: mock.Mock = mock.Mock(return_value=32)
        self.Everything_GetResultFileListFileNameW: mock.Mock = mock.Mock()
        self.Everything_GetResultRunCount: mock.Mock = mock.Mock()
        self.Everything_GetResultDateRun: mock.Mock = mock.Mock()
        self.Everything_GetResultDateRecentlyChanged: mock.Mock = mock.Mock()
        self.Everything_GetResultHighlightedFileNameW: mock.Mock = mock.Mock()
        self.Everything_GetResultHighlightedPathW: mock.Mock = mock.Mock()
        self.Everything_GetResultHighlightedFullPathAndFileNameW: mock.Mock = mock.Mock()
        self.Everything_CleanUp: mock.Mock = mock.Mock()

from pyeverything import dll as dll_list
from pyeverything.dll import filetime_to_dt

class TestDllList(unittest.TestCase):
    @mock.patch('pyeverything.dll.load_everything_dll')
    @mock.patch('pyeverything.dll.init_functions')
    @mock.patch('pyeverything.dll.run_search')
    def test_test_option_output_text(self, mock_run_search: mock.Mock, mock_init: mock.Mock, mock_load: mock.Mock) -> None:
        # Simulate a search result for the hosts file
        mock_run_search.return_value = [
            {'path': r'C:\Windows\System32\drivers\etc\hosts', 'size': 959}
        ]
        # Prepare argv for --test
        test_args = ['dll_list.py', '--test']
        with mock.patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                with self.assertRaises(SystemExit) as cm:
                    dll_list.main()
            self.assertEqual(cm.exception.code, 0)
            output = captured_output.getvalue().strip()
            self.assertRegex(
                output,
                r'^Test passed: hosts file found, size \d+\.$'
            )

    @mock.patch('pyeverything.dll.load_everything_dll')
    @mock.patch('pyeverything.dll.init_functions')
    @mock.patch('pyeverything.dll.run_search')
    def test_test_option_output_json(self, mock_run_search: mock.Mock, mock_init: mock.Mock, mock_load: mock.Mock) -> None:
        mock_run_search.return_value = [
            {'path': r'C:\Windows\System32\drivers\etc\hosts', 'size': 959}
        ]
        test_args = ['dll_list.py', '--test', '--json']
        with mock.patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                with self.assertRaises(SystemExit) as cm:
                    dll_list.main()
            self.assertEqual(cm.exception.code, 0)
            data = json.loads(captured_output.getvalue().strip())
            self.assertTrue(data.get("passed") is True)
            self.assertIsInstance(data.get("size"), int)

    @mock.patch('pyeverything.dll.load_everything_dll')
    @mock.patch('pyeverything.dll.init_functions')
    @mock.patch('pyeverything.dll.run_search')
    def test_search_option_output_json(self, mock_run_search: mock.Mock, mock_init: mock.Mock, mock_load: mock.Mock) -> None:
        # Simulate a search result for a hosts.ics file
        mock_run_search.return_value = [
            {
                'name': 'hosts.ics',
                'path': r'C:\Windows\System32\drivers\etc\hosts.ics',
                'size': 438
            }
        ]
        test_args = [
            'dll_list.py',
            '--search',
            'windows system32 drivers etc hosts ics',
            '--json'
        ]
        with mock.patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                # main() should not raise SystemExit for normal search
                dll_list.main()
            output = captured_output.getvalue().strip()
            data = json.loads(output)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            entry = data[0]
            self.assertEqual(entry.get('name'), 'hosts.ics')
            self.assertEqual(entry.get('path'), r'C:\Windows\System32\drivers\etc\hosts.ics')
            self.assertIsInstance(entry.get('size'), int)

    @mock.patch('pyeverything.dll.load_everything_dll')
    @mock.patch('pyeverything.dll.init_functions')
    @mock.patch('pyeverything.dll.run_search')
    def test_search_option_output_json_all_fields(self, mock_run_search: mock.Mock, mock_init: mock.Mock, mock_load: mock.Mock) -> None:
        # Simulate a search result with all fields
        mock_run_search.return_value = [
            {
                "name": "hosts.ics",
                "path": r"C:\Windows\System32\drivers\etc\hosts.ics",
                "size": 438,
                "extension": "",
                "date_created": "2022-07-27T12:37:01.620755",
                "date_modified": "2024-06-13T10:28:57.492615",
                "date_accessed": "2025-06-23T00:15:11.843185",
                "attributes": 8224,
                "list_file_name": "",
                "run_count": 0,
                "date_run": None,
                "date_recently_changed": None,
                "highlighted_file_name": "",
                "highlighted_path": "",
                "highlighted_full_path": ""
            }
        ]
        test_args = [
            'dll_list.py',
            '--search',
            'windows system32 drivers etc hosts ics',
            '--json',
            '--all-fields'
        ]
        with mock.patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                dll_list.main()
            output = captured_output.getvalue().strip()
            data = json.loads(output)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            entry = data[0]
            # Check required fields and types
            self.assertEqual(entry.get('name'), 'hosts.ics')
            self.assertEqual(entry.get('path'), r'C:\Windows\System32\drivers\etc\hosts.ics')
            self.assertIsInstance(entry.get('size'), int)
            self.assertIn('extension', entry)
            self.assertIn('date_created', entry)
            self.assertIn('date_modified', entry)
            self.assertIn('date_accessed', entry)
            self.assertIn('attributes', entry)
            self.assertIn('list_file_name', entry)
            self.assertIn('run_count', entry)
            self.assertIn('date_run', entry)
            self.assertIn('date_recently_changed', entry)
            self.assertIn('highlighted_file_name', entry)
            self.assertIn('highlighted_path', entry)
            self.assertIn('highlighted_full_path', entry)

    @mock.patch('pyeverything.dll.ctypes.create_unicode_buffer')
    @mock.patch('pyeverything.dll.ctypes.c_ulonglong')
    @mock.patch('pyeverything.dll.ctypes.byref')
    @mock.patch('pyeverything.dll.wintypes.FILETIME')
    def test_run_search(self, mock_filetime: mock.Mock, mock_byref: mock.Mock, mock_c_ulonglong: mock.Mock, mock_create_unicode_buffer: mock.Mock) -> None:
        import os
        debug_path_for_basename = r'C:\test\path\file.txt'
        print(f"DEBUG_TEST: os.path.basename in test_run_search: {os.path.basename(debug_path_for_basename)}", flush=True)
        print(f"DEBUG_TEST: id(os) in test_run_search: {id(os)}", flush=True)
        mock_dll = MockDll()
        mock_dll.Everything_QueryW.return_value = True
        mock_dll.Everything_GetNumResults.return_value = 1

        # Mock for path and name
        mock_path_buffer = mock.Mock()
        mock_path_buffer.value = r"C:\test\path\file.txt"
        mock_create_unicode_buffer.return_value = mock_path_buffer

        # Mock for size
        mock_size_var = mock.Mock()
        mock_size_var.value = 12345
        mock_c_ulonglong.return_value = mock_size_var

        # Mock for all_fields
        mock_dll.Everything_GetResultExtensionW.return_value = 0 # Success
        mock_ext_buffer = mock.Mock()
        mock_ext_buffer.value = "txt"
        mock_create_unicode_buffer.side_effect = [mock_path_buffer, mock_ext_buffer, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()] # Reset side_effect
        mock_create_unicode_buffer.return_value = mock_path_buffer # Reset for path buffer

        # Test with all_fields=True

        # Mock FILETIME conversions
        mock_filetime_instance = mock.Mock()
        mock_filetime.return_value = mock_filetime_instance
        # Simulate a valid datetime for date_created, modified, accessed, run, recently_changed
        with mock.patch('pyeverything.dll.filetime_to_dt', side_effect=[
            datetime.datetime(2023, 1, 1), # created
            datetime.datetime(2023, 1, 2), # modified
            datetime.datetime(2023, 1, 3), # accessed
            datetime.datetime(2023, 1, 4), # run
            datetime.datetime(2023, 1, 5)  # recently_changed
        ]):
            # Test with all_fields=False
            results_basic = dll_list.run_search(mock_dll, "query", 0, 10, all_fields=False)
            self.assertEqual(len(results_basic), 1)
            self.assertIn("name", results_basic[0])
            self.assertIn("path", results_basic[0])
            self.assertIn("size", results_basic[0])
            self.assertEqual(results_basic[0]["name"], "file.txt")
            self.assertEqual(results_basic[0]["path"], r"C:\test\path\file.txt")
            self.assertEqual(results_basic[0]["size"], 12345)
            self.assertNotIn("extension", results_basic[0]) # Should not be present in basic

            mock_dll.Everything_CleanUp.reset_mock()
            mock_create_unicode_buffer.reset_mock()
            mock_create_unicode_buffer.side_effect = [mock_path_buffer, mock_ext_buffer, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()] # Re-assign side_effect

            # Test with all_fields=True
            results_all = dll_list.run_search(mock_dll, "query", 0, 10, all_fields=True)
            self.assertEqual(len(results_all), 1)
            self.assertIn("extension", results_all[0])
            self.assertEqual(results_all[0]["extension"], "txt")
            self.assertIn("date_created", results_all[0])
            self.assertEqual(results_all[0]["date_created"], "2023-01-01T00:00:00")
            self.assertIn("date_modified", results_all[0])
            self.assertEqual(results_all[0]["date_modified"], "2023-01-02T00:00:00")
            self.assertIn("date_accessed", results_all[0])
            self.assertEqual(results_all[0]["date_accessed"], "2023-01-03T00:00:00")
            self.assertIn("attributes", results_all[0])
            self.assertEqual(results_all[0]["attributes"], 32)
            self.assertIn("date_run", results_all[0])
            self.assertEqual(results_all[0]["date_run"], "2023-01-04T00:00:00")
            self.assertIn("date_recently_changed", results_all[0])
            self.assertEqual(results_all[0]["date_recently_changed"], "2023-01-05T00:00:00")

            mock_dll.Everything_SetSearchW.assert_called_with("query")
            mock_dll.Everything_SetMatchPath.assert_called_with(True)
            mock_dll.Everything_SetOffset.assert_called_with(0)
            mock_dll.Everything_SetMax.assert_called_with(10)
            mock_dll.Everything_QueryW.assert_called_with(True)
            self.assertEqual(mock_dll.Everything_GetNumResults.call_count, 2)
            mock_dll.Everything_CleanUp.assert_called_once()

    def test_filetime_to_dt(self) -> None:
        # Test case 1: Known valid FILETIME
        # Corresponds to 2024-01-01 00:00:00 UTC
        ft = wintypes.FILETIME()
        ft.dwLowDateTime = 2880360960
        ft.dwHighDateTime = 30538200
        expected_dt = datetime.datetime(2016, 8, 19, 5, 15, 15, 906816)
        self.assertEqual(filetime_to_dt(ft), expected_dt)

        # Test case 2: Zero FILETIME (should return None)
        ft_zero = wintypes.FILETIME()
        ft_zero.dwLowDateTime = 0
        ft_zero.dwHighDateTime = 0
        self.assertIsNone(filetime_to_dt(ft_zero))

        # Test case 3: FILETIME causing OverflowError (should return None)
        # A very large value that would cause overflow
        ft_overflow = wintypes.FILETIME()
        ft_overflow.dwLowDateTime = 0xFFFFFFFF
        ft_overflow.dwHighDateTime = 0x7FFFFFFF # Max positive high part
        self.assertIsNone(filetime_to_dt(ft_overflow))

if __name__ == '__main__':
    unittest.main()
