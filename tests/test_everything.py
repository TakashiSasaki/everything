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

        # Mock the DLL functions to simulate finding one result.
        mock_dll.Everything_QueryW.return_value = True
        mock_dll.Everything_GetNumResults.return_value = 1

        # Mock the result data
        def get_full_path_name_w(index, buf, buf_len):
            if index == 0:
                buf.value = host_file_path
            return len(host_file_path)

        mock_dll.Everything_GetResultFullPathNameW.side_effect = get_full_path_name_w
        mock_dll.Everything_GetResultSize.return_value = True

        # Call the search method
        results = everything.search(host_file_path)

        # Check that the search was called with the correct query
        mock_dll.Everything_SetSearchW.assert_called_with(host_file_path)

        # Assertions
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'hosts')
        self.assertEqual(results[0]['path'], r'C:\Windows\System32\drivers\etc')
        self.assertEqual(results[0]['size'], 0)

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

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_match_whole_word(self, mock_init_functions, mock_load_dll):
        """Test setting the match whole word option."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        # Test with True (whole word matching)
        everything.set_match_whole_word(True)
        everything.dll.Everything_SetMatchWholeWord.assert_called_with(True)

        # Test with False (not whole word matching)
        everything.set_match_whole_word(False)
        everything.dll.Everything_SetMatchWholeWord.assert_called_with(False)

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_regex(self, mock_init_functions, mock_load_dll):
        """Test setting the regex option."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        # Test with True (regex enabled)
        everything.set_regex(True)
        everything.dll.Everything_SetRegex.assert_called_with(True)

        # Test with False (regex disabled)
        everything.set_regex(False)
        everything.dll.Everything_SetRegex.assert_called_with(False)

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_request_flags(self, mock_init_functions, mock_load_dll):
        """Test setting the request flags."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        test_flags = 0x00000001 | 0x00000002  # Example flags
        everything.set_request_flags(test_flags)
        everything.dll.Everything_SetRequestFlags.assert_called_with(test_flags)

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_max(self, mock_init_functions, mock_load_dll):
        """Test setting the maximum number of results."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        test_max_results = 500
        everything.set_max(test_max_results)
        everything.dll.Everything_SetMax.assert_called_with(test_max_results)

        everything.dll.Everything_SetMax.assert_called_with(test_max_results)

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_offset(self, mock_init_functions, mock_load_dll):
        """Test setting the offset."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        test_offset = 100
        everything.set_offset(test_offset)
        everything.dll.Everything_SetOffset.assert_called_with(test_offset)

        everything.dll.Everything_SetOffset.assert_called_with(test_offset)

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_sort_results_by_path(self, mock_init_functions, mock_load_dll):
        """Test sorting results by path."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        everything.sort_results_by_path()
        everything.dll.Everything_SortResultsByPath.assert_called_once()

    @patch('pyeverything.everything.load_everything_dll')
    @patch('pyeverything.everything.init_functions')
    def test_set_match_case_with_search_results(self, mock_init_functions, mock_load_dll):
        """Test set_match_case by observing search results."""
        mock_dll = MagicMock()
        mock_load_dll.return_value = mock_dll

        everything = Everything()

        # Variable to track the case sensitivity setting
        self.match_case_enabled = False

        def mock_set_match_case(enable):
            self.match_case_enabled = enable
            mock_dll.Everything_SetMatchCase.assert_called_with(enable)

        mock_dll.Everything_SetMatchCase.side_effect = mock_set_match_case

        # Mock search results for a file named "TestFile.txt"
        mock_filename = "TestFile.txt"
        mock_full_path = "C:\\Path\\To\\" + mock_filename

        def mock_query_w(b_block):
            return True

        def mock_get_num_results():
            if self.match_case_enabled and everything.dll.Everything_GetSearchW().value != mock_filename:
                return 0
            return 1

        def mock_get_result_full_path_name_w(index, buf, buf_len):
            if index == 0:
                # Ensure the buffer is large enough
                if buf_len < len(mock_full_path) + 1:
                    raise ValueError("Buffer too small")
                # Assign the value directly to the buffer's internal object
                ctypes.memmove(buf, mock_full_path, len(mock_full_path) * ctypes.sizeof(ctypes.c_wchar))
            return len(mock_full_path)

        def mock_get_result_size(index, size_var):
            size_var._obj.value = 1024
            return True

        mock_dll.Everything_QueryW.side_effect = mock_query_w
        mock_dll.Everything_GetNumResults.side_effect = mock_get_num_results
        mock_dll.Everything_GetResultFullPathNameW.side_effect = mock_get_result_full_path_name_w
        mock_dll.Everything_GetResultSize.side_effect = mock_get_result_size

        # Mock Everything_GetSearchW to return the last set search query
        everything.dll.Everything_SetSearchW.side_effect = lambda query: setattr(everything.dll.Everything_SetSearchW, 'value', query)
        everything.dll.Everything_GetSearchW.return_value = MagicMock(value="testfile.txt") # Default value

        # Test case-sensitive search (should find no results for lowercase query)
        everything.set_match_case(True)
        everything.dll.Everything_GetSearchW.return_value.value = "testfile.txt" # Set the search query for the mock
        results_case_sensitive = everything.search("testfile.txt")
        self.assertEqual(len(results_case_sensitive), 0)

        # Test case-insensitive search (should find results for lowercase query)
        everything.set_match_case(False)
        everything.dll.Everything_GetSearchW.return_value.value = "testfile.txt" # Set the search query for the mock
        results_case_insensitive = everything.search("testfile.txt")
        self.assertEqual(len(results_case_insensitive), 1)
        self.assertEqual(results_case_insensitive[0]["name"], mock_filename)

        # Test case-sensitive search with correct case (should find results)
        everything.set_match_case(True)
        everything.dll.Everything_GetSearchW.return_value.value = mock_filename # Set the search query for the mock
        results_case_sensitive_correct_case = everything.search(mock_filename)
        self.assertEqual(len(results_case_sensitive_correct_case), 1)
        self.assertEqual(results_case_sensitive_correct_case[0]["name"], mock_filename)

if __name__ == '__main__':
    unittest.main()
