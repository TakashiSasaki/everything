import sys
import unittest
from unittest import mock
from io import StringIO
import json

import everything_dll_list

class TestEverythingDllList(unittest.TestCase):
    @mock.patch('everything_dll_list.load_everything_dll')
    @mock.patch('everything_dll_list.init_functions')
    @mock.patch('everything_dll_list.run_search')
    def test_test_option_output_text(self, mock_run_search, mock_init, mock_load):
        # Simulate a search result for the hosts file
        mock_run_search.return_value = [
            {'path': r'C:\Windows\System32\drivers\etc\hosts', 'size': 959}
        ]
        # Prepare argv for --test
        test_args = ['everything_dll_list.py', '--test']
        with mock.patch.object(sys, 'argv', test_args):
            # Capture stdout
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                # main() should exit with code 0
                with self.assertRaises(SystemExit) as cm:
                    everything_dll_list.main()
            # Verify exit code is zero
            self.assertEqual(cm.exception.code, 0)
            # Check output matches the expected format
            output = captured_output.getvalue().strip()
            # Use regex to match number
            self.assertRegex(
                output,
                r'^Test passed: hosts file found, size \d+\.$'
            )

    @mock.patch('everything_dll_list.load_everything_dll')
    @mock.patch('everything_dll_list.init_functions')
    @mock.patch('everything_dll_list.run_search')
    def test_test_option_output_json(self, mock_run_search, mock_init, mock_load):
        # Simulate a search result for the hosts file
        mock_run_search.return_value = [
            {'path': r'C:\Windows\System32\drivers\etc\hosts', 'size': 959}
        ]
        # Prepare argv for --test --json
        test_args = ['everything_dll_list.py', '--test', '--json']
        with mock.patch.object(sys, 'argv', test_args):
            # Capture stdout
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                # main() should exit with code 0
                with self.assertRaises(SystemExit) as cm:
                    everything_dll_list.main()
            # Verify exit code is zero
            self.assertEqual(cm.exception.code, 0)
            # Parse JSON output
            output = captured_output.getvalue().strip()
            data = json.loads(output)
            self.assertTrue(data.get("passed") is True)
            self.assertIsInstance(data.get("size"), int)

if __name__ == '__main__':
    unittest.main()
