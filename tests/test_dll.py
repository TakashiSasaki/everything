import sys
import unittest
from unittest import mock
from io import StringIO
import json
import datetime
from ctypes import wintypes

from everything_cli import dll as dll_list
from everything_cli.dll import filetime_to_dt

class TestDllList(unittest.TestCase):
    @mock.patch('everything_cli.dll.load_everything_dll')
    @mock.patch('everything_cli.dll.init_functions')
    @mock.patch('everything_cli.dll.run_search')
    def test_test_option_output_text(self, mock_run_search, mock_init, mock_load):
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

    @mock.patch('everything_cli.dll.load_everything_dll')
    @mock.patch('everything_cli.dll.init_functions')
    @mock.patch('everything_cli.dll.run_search')
    def test_test_option_output_json(self, mock_run_search, mock_init, mock_load):
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

    @mock.patch('everything_cli.dll.load_everything_dll')
    @mock.patch('everything_cli.dll.init_functions')
    @mock.patch('everything_cli.dll.run_search')
    def test_search_option_output_json(self, mock_run_search, mock_init, mock_load):
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

    @mock.patch('everything_cli.dll.load_everything_dll')
    @mock.patch('everything_cli.dll.init_functions')
    @mock.patch('everything_cli.dll.run_search')
    def test_search_option_output_json_all_fields(self, mock_run_search, mock_init, mock_load):
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

    def test_filetime_to_dt(self):
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
