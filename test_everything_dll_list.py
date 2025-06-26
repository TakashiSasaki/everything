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
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                with self.assertRaises(SystemExit) as cm:
                    everything_dll_list.main()
            self.assertEqual(cm.exception.code, 0)
            output = captured_output.getvalue().strip()
            self.assertRegex(
                output,
                r'^Test passed: hosts file found, size \d+\.$'
            )

    @mock.patch('everything_dll_list.load_everything_dll')
    @mock.patch('everything_dll_list.init_functions')
    @mock.patch('everything_dll_list.run_search')
    def test_test_option_output_json(self, mock_run_search, mock_init, mock_load):
        mock_run_search.return_value = [
            {'path': r'C:\Windows\System32\drivers\etc\hosts', 'size': 959}
        ]
        test_args = ['everything_dll_list.py', '--test', '--json']
        with mock.patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                with self.assertRaises(SystemExit) as cm:
                    everything_dll_list.main()
            self.assertEqual(cm.exception.code, 0)
            data = json.loads(captured_output.getvalue().strip())
            self.assertTrue(data.get("passed") is True)
            self.assertIsInstance(data.get("size"), int)

    @mock.patch('everything_dll_list.load_everything_dll')
    @mock.patch('everything_dll_list.init_functions')
    @mock.patch('everything_dll_list.run_search')
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
            'everything_dll_list.py',
            '--search',
            'windows system32 drivers etc hosts ics',
            '--json'
        ]
        with mock.patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with mock.patch('sys.stdout', new=captured_output):
                # main() should not raise SystemExit for normal search
                everything_dll_list.main()
            output = captured_output.getvalue().strip()
            data = json.loads(output)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            entry = data[0]
            self.assertEqual(entry.get('name'), 'hosts.ics')
            self.assertEqual(entry.get('path'), r'C:\Windows\System32\drivers\etc\hosts.ics')
            self.assertIsInstance(entry.get('size'), int)

if __name__ == '__main__':
    unittest.main()
