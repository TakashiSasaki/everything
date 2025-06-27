#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
import os
import ctypes

# Since the new class is in pyeverything/everything.py, we need to make sure the path is correct
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyeverything.everything import Everything

class TestEverything(unittest.TestCase):

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_search_hosts_file(self, mock_init_functions, mock_load_dll):
        """Test searching for the hosts file."""
        # Mock the DLL loading and initialization
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        # Create an instance of the Everything class
        everything = Everything()

        # The path to search for
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"

        # Call the search method
        results = everything.search(host_file_path)

        # Check that the search was called with the correct query
        everything.dll.Everything_SetSearchW.assert_called_with(host_file_path)

        # For this test, we'll assume the mock DLL returns at least one result
        # In a real scenario, we would mock the return values of the DLL functions
        everything.dll.Everything_GetNumResults.return_value = 1

        # Mock the result data
        def get_full_path_name_w(index, buf, buf_len):
            if index == 0:
                buf.value = host_file_path
            return len(host_file_path)

        everything.dll.Everything_GetResultFullPathNameW.side_effect = get_full_path_name_w
        everything.dll.Everything_GetResultSize.return_value = True

        # Re-run search to get mocked results
        results = everything.search(host_file_path)

        # Assertions
        self.assertIsInstance(results, list)

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_match_case(self, mock_init_functions, mock_load_dll):
        """Test setting the match case option."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        # Test with True (case-sensitive)
        everything.set_match_case(True)
        everything.dll.Everything_SetMatchCase.assert_called_with(True)

        # Test with False (case-insensitive)
        everything.set_match_case(False)
        everything.dll.Everything_SetMatchCase.assert_called_with(False)

if __name__ == '__main__':
    unittest.main()
