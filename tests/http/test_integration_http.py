"""
Integration-like tests for the pyeverything.http CLI adapter.

These tests exercise the module entrypoint in-process, patching
`requests.get` to emulate Everything's HTTP server. They verify
both `--test` behavior and `--search` output with and without the
`--all-fields` flag, and ensure host/port resolution works.
"""
from __future__ import annotations

import json
import os
import sys
import types
from io import StringIO
from typing import Any, Dict
from unittest import mock
import unittest


SCRIPT_MODULE = "pyeverything.http"


class MockResponse:
    def __init__(self, payload: Dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code}")

    def json(self) -> Dict[str, Any]:
        return self._payload


class TestHttpCli(unittest.TestCase):
    """Integration-like tests for the HTTP CLI entrypoint."""

    def setUp(self) -> None:
        self._stdout = sys.stdout
        sys.stdout = StringIO()
        # Ensure env vars do not leak between tests
        self._env_backup = dict(os.environ)

    def tearDown(self) -> None:
        sys.stdout = self._stdout
        os.environ.clear()
        os.environ.update(self._env_backup)

    @mock.patch("requests.get")
    @mock.patch("sys.argv", ["http.py", "--test"])  # text mode
    def test_test_option_text(self, mock_get: mock.Mock) -> None:
        payload = {"results": [{"size": 959}]}
        mock_get.return_value = MockResponse(payload)

        # Import and run main
        mod = __import__(SCRIPT_MODULE, fromlist=["main"])
        with self.assertRaises(SystemExit) as cm:
            mod.main()
        self.assertEqual(cm.exception.code, 0)

        out = sys.stdout.getvalue().strip()
        self.assertRegex(out, r"^Test passed: hosts file found with size \d+\.")

        # Ensure correct base URL used (defaults)
        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith("http://"))

    @mock.patch("requests.get")
    @mock.patch("sys.argv", ["http.py", "--test", "--json"])  # JSON mode
    def test_test_option_json(self, mock_get: mock.Mock) -> None:
        payload = {"results": [{"size": 1234}]}
        mock_get.return_value = MockResponse(payload)

        mod = __import__(SCRIPT_MODULE, fromlist=["main"])
        with self.assertRaises(SystemExit) as cm:
            mod.main()
        self.assertEqual(cm.exception.code, 0)

        data = json.loads(sys.stdout.getvalue().strip())
        self.assertTrue(data.get("passed"))
        self.assertEqual(data.get("size"), 1234)

    @mock.patch("requests.get")
    def test_search_json_basic(self, mock_get: mock.Mock) -> None:
        # Provide environment host/port and validate URL formation
        os.environ["EVERYTHING_HOST"] = "localhost"
        os.environ["EVERYTHING_PORT"] = "8888"

        # Simulate a single basic result
        payload = {
            "results": [
                {
                    "file_name_column": "hosts",
                    "path_column": r"C:\\Windows\\System32\\drivers\\etc",
                    "size_column": 959,
                }
            ]
        }
        mock_get.return_value = MockResponse(payload)

        sys.argv = ["http.py", "--search", "hosts", "--json"]
        mod = __import__(SCRIPT_MODULE, fromlist=["main"])
        mod.main()  # should not exit

        # Assert output is the results array as JSON
        out = sys.stdout.getvalue().strip()
        data = json.loads(out)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["file_name_column"], "hosts")
        self.assertIn("path_column", data[0])
        # Validate base URL and params used
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "http://localhost:8888/")
        self.assertIn("params", kwargs)
        self.assertEqual(kwargs["params"]["search"], "hosts")

    @mock.patch("requests.get")
    def test_search_json_all_fields(self, mock_get: mock.Mock) -> None:
        # Simulate an extended result row with common columns
        row = {
            "file_name_column": "hosts",
            "path_column": r"C:\\Windows\\System32\\drivers\\etc",
            "full_path_column": r"C:\\Windows\\System32\\drivers\\etc\\hosts",
            "size_column": 959,
            "extension_column": "",
            "date_modified_column": "2024-01-01T00:00:00",
            "date_created_column": "2023-01-01T00:00:00",
            "date_accessed_column": "2025-01-01T00:00:00",
            "attributes_column": 32,
            "file_list_file_name_column": "",
            "run_count_column": 0,
            "date_run_column": None,
            "date_recently_changed_column": None,
            "highlighted_file_name_column": "",
            "highlighted_path_column": "",
            "highlighted_full_path_column": "",
        }
        payload = {"results": [row]}
        mock_get.return_value = MockResponse(payload)

        sys.argv = ["http.py", "--search", "hosts", "--json", "--all-fields"]
        mod = __import__(SCRIPT_MODULE, fromlist=["main"])
        mod.main()

        out = sys.stdout.getvalue().strip()
        data = json.loads(out)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        e0 = data[0]
        # Spot-check a few extended fields
        self.assertIn("full_path_column", e0)
        self.assertIn("date_modified_column", e0)
        self.assertIn("attributes_column", e0)


if __name__ == "__main__":
    unittest.main()

