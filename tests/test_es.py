import os
import subprocess
import sys
import re
import json
import unittest
from unittest import mock
from io import StringIO
from typing import Any

SCRIPT_MODULE: str = "pyeverything.es"

class TestEsSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.original_stdout: Any = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self) -> None:
        sys.stdout = self.original_stdout

    @mock.patch('pyeverything.es.parse_csv_text')
    @mock.patch('pyeverything.es.subprocess.run')
    @mock.patch('pyeverything.es.locate_es', return_value='/mock/es.exe')
    @mock.patch('sys.argv', ['es.py', '--search', 'windows system32 drivers etc hosts.ics', '--json'])
    def test_search_json_option(self, mock_locate_es: mock.Mock, mock_run: mock.Mock, mock_parse_csv_text: mock.Mock) -> None:
        mock_run.return_value = mock.Mock(
            stdout="mocked csv content",
            stderr="",
            returncode=0
        )
        mock_parse_csv_text.return_value = [
            {
                "name": "hosts.ics",
                "path": "C:\\Windows\\System32\\drivers\\etc\\hosts.ics",
                "size": 438
            }
        ]

        from pyeverything.es import main
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        stdout = sys.stdout.getvalue()
        data = json.loads(stdout)
        self.assertEqual(data, mock_parse_csv_text.return_value)

    @mock.patch('pyeverything.es.parse_csv_text')
    @mock.patch('pyeverything.es.subprocess.run')
    @mock.patch('pyeverything.es.locate_es', return_value='/mock/es.exe')
    @mock.patch('sys.argv', ['es.py', '--search', 'windows system32 drivers etc hosts.ics', '--json', '--all-fields'])
    def test_search_allfields_json_option(self, mock_locate_es: mock.Mock, mock_run: mock.Mock, mock_parse_csv_text: mock.Mock) -> None:
        mock_run.return_value = mock.Mock(
            stdout="mocked csv content",
            stderr="",
            returncode=0
        )
        mock_parse_csv_text.return_value = [
            {
                "name": "hosts.ics",
                "path": "C:\\Windows\\System32\\drivers\\etc\\hosts.ics",
                "size": 438,
                "extension": "ics",
                "date_created": "2022-07-27T12:37:01.620755",
                "date_modified": "2024-06-13T10:28:57.492615",
                "date_accessed": "2025-06-23T00:15:11.843185",
                "attributes": 8224,
                "file_list_file_name": "",
                "run_count": 0,
                "date_run": None,
                "date_recently_changed": None
            }
        ]

        from pyeverything.es import main
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        stdout = sys.stdout.getvalue()
        data = json.loads(stdout)
        self.assertEqual(data, mock_parse_csv_text.return_value)

class TestEsLocateEs(unittest.TestCase):
    @mock.patch('shutil.which')
    @mock.patch('os.path.isfile')
    @mock.patch('os.access')
    @mock.patch('os.path.dirname', return_value='/mock/script/dir')
    @mock.patch('os.path.join')
    def test_locate_es_in_path(self, mock_join: mock.Mock, mock_dirname: mock.Mock, mock_access: mock.Mock, mock_isfile: mock.Mock, mock_which: mock.Mock) -> None:
        mock_which.return_value = '/path/to/es.exe'
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_join.side_effect = lambda *args: '/'.join(args) # Simulate os.path.join behavior

        from pyeverything.es import locate_es
        result = locate_es()
        self.assertEqual(result, '/path/to/es.exe')
        mock_which.assert_called_once_with('es.exe')
        mock_isfile.assert_not_called() # Should not be called if found in PATH
        mock_access.assert_not_called() # Should not be called if found in PATH

    @mock.patch('shutil.which', return_value=None)
    @mock.patch('os.path.isfile')
    @mock.patch('os.access')
    @mock.patch('os.path.dirname', return_value='/mock/script/dir')
    @mock.patch('os.path.join')
    def test_locate_es_in_package_bin(self, mock_join: mock.Mock, mock_dirname: mock.Mock, mock_access: mock.Mock, mock_isfile: mock.Mock, mock_which: mock.Mock) -> None:
        # Simulate es.exe not in PATH, but in package bin
        mock_which.return_value = None
        mock_join.side_effect = lambda *args: '/'.join(args) # Simulate os.path.join behavior

        # Set side_effect for isfile and access to simulate finding in package bin
        mock_isfile.side_effect = [True, False] # True for bin_path, False for local_path
        mock_access.side_effect = [True, False] # True for bin_path, False for local_path

        from pyeverything.es import locate_es
        result = locate_es()
        self.assertEqual(result, '/mock/script/dir/bin/es.exe')
        mock_which.assert_called_once_with('es.exe')
        mock_isfile.assert_any_call('/mock/script/dir/bin/es.exe')
        mock_access.assert_any_call('/mock/script/dir/bin/es.exe', os.X_OK)

    @mock.patch('shutil.which', return_value=None)
    @mock.patch('os.path.isfile')
    @mock.patch('os.access')
    @mock.patch('os.path.dirname', return_value='/mock/script/dir')
    @mock.patch('os.path.join')
    @mock.patch('os.getcwd', return_value='/mock/current/dir')
    def test_locate_es_in_cwd(self, mock_getcwd: mock.Mock, mock_join: mock.Mock, mock_dirname: mock.Mock, mock_access: mock.Mock, mock_isfile: mock.Mock, mock_which: mock.Mock) -> None:
        # Simulate es.exe not in PATH or package bin, but in CWD
        mock_which.return_value = None
        mock_join.side_effect = lambda *args: '/'.join(args) # Simulate os.path.join behavior

        # Set side_effect for isfile and access to simulate finding in CWD
        mock_isfile.side_effect = [False, True] # False for bin_path, True for local_path
        mock_access.side_effect = [True] # Only one call to access is expected

        from pyeverything.es import locate_es
        result = locate_es()
        self.assertEqual(result, '/mock/current/dir/es.exe')
        mock_which.assert_called_once_with('es.exe')
        mock_isfile.assert_any_call('/mock/script/dir/bin/es.exe')
        mock_isfile.assert_any_call('/mock/current/dir/es.exe')
        mock_access.assert_called_once_with('/mock/current/dir/es.exe', os.X_OK)

    @mock.patch('shutil.which', return_value=None)
    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('os.access', return_value=False)
    @mock.patch('os.path.dirname', return_value='/mock/script/dir')
    @mock.patch('os.path.join')
    @mock.patch('os.getcwd', return_value='/mock/current/dir')
    def test_locate_es_not_found(self, mock_getcwd: mock.Mock, mock_join: mock.Mock, mock_dirname: mock.Mock, mock_access: mock.Mock, mock_isfile: mock.Mock, mock_which: mock.Mock) -> None:
        mock_join.side_effect = lambda *args: '/'.join(args) # Simulate os.path.join behavior
        from pyeverything.es import locate_es
        with self.assertRaisesRegex(SystemExit, "Error: 'es.exe' not found in PATH, package bin directory, or current directory."):
            locate_es()
        mock_which.assert_called_once_with('es.exe')
        mock_isfile.assert_any_call('/mock/script/dir/bin/es.exe')
        mock_isfile.assert_any_call('/mock/current/dir/es.exe')
        mock_access.assert_not_called()
