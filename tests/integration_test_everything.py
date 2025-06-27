#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the pyeverything directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyeverything.everything import Everything

class TestEverythingIntegration(unittest.TestCase):

    def setUp(self):
        # Initialize the Everything class for integration tests
        self.everything = Everything()
        self.everything.dll.Everything_Reset()

    def test_search_hosts_file_integration(self):
        """Integration test: Search for C:\Windows\System32\drivers\etc\hosts"""
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"

        # Perform the actual search
        results = self.everything.search(host_file_path)

        # Assert that the hosts file is found in the results
        found = False
        for item in results:
            if item["path"].lower() == host_file_path.lower():
                found = True
                break
        self.assertTrue(found, f"Hosts file not found in search results: {host_file_path}")

        # Optionally, check if the size is non-zero if the file exists on disk
        if os.path.exists(host_file_path):
            actual_size = os.path.getsize(host_file_path)
            if actual_size > 0:
                found_item = next((item for item in results if item["path"].lower() == host_file_path.lower()), None)
                self.assertIsNotNone(found_item)
                self.assertGreater(found_item["size"], 0, "Found hosts file has zero size in search results")

    def test_search_common_string_returns_many_results(self):
        """Integration test: Search for a common string and ensure many results are returned."""
        query = "exe"
        results = self.everything.search(query, count=200) # Request more than 100 results
        self.assertGreaterEqual(len(results), 100, f"Expected at least 100 results for '{query}', but got {len(results)}")

    def test_set_match_case_integration(self):
        """Integration test: Verify set_match_case functionality with actual searches."""
        import tempfile

        # Create a temporary file with mixed case name
        temp_dir = tempfile.gettempdir()
        mixed_case_filename = "TeStFiLe_Integration.txt"
        temp_file_path = os.path.join(temp_dir, mixed_case_filename)

        # Ensure the file exists for the test
        with open(temp_file_path, "w") as f:
            f.write("This is a test file.")

        try:
            # Give Everything a moment to index the new file (optional, but good practice)
            # In a real scenario, you might need to wait or trigger an index update
            import time
            time.sleep(1) 

            # Test case-sensitive search (should not find the file with lowercase query)
            self.everything.set_match_case(True)
            results_case_sensitive = self.everything.search(mixed_case_filename.lower())
            self.assertEqual(len(results_case_sensitive), 0, "Case-sensitive search found unexpected results")

            # Test case-insensitive search (should find the file with lowercase query)
            self.everything.set_match_case(False)
            results_case_insensitive = self.everything.search(mixed_case_filename.lower())
            self.assertGreater(len(results_case_insensitive), 0, "Case-insensitive search found no results")
            found_in_insensitive = False
            for item in results_case_insensitive:
                if item["path"].lower() == temp_file_path.lower():
                    found_in_insensitive = True
                    break
            self.assertTrue(found_in_insensitive, f"File not found in case-insensitive search: {temp_file_path}")

        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_set_match_whole_word_integration(self):
        """Integration test: Verify set_match_whole_word calls the DLL function correctly."""
        # We need to patch the DLL functions for this test, as we are not testing search behavior
        # but rather the correct calling of the DLL function.
        with patch('pyeverything.everything.load_everything_dll') as mock_load_dll, \
             patch('pyeverything.everything.init_functions') as mock_init_functions:
            mock_dll = MagicMock()
            mock_load_dll.return_value = mock_dll

            everything = Everything()

            # Test with True
            everything.set_match_whole_word(True)
            mock_dll.Everything_SetMatchWholeWord.assert_called_with(True)

            # Test with False
            everything.set_match_whole_word(False)
            mock_dll.Everything_SetMatchWholeWord.assert_called_with(False)

            mock_dll.Everything_SetMatchWholeWord.assert_called_with(False)

    def test_set_regex_integration(self):
        """Integration test: Verify set_regex enables regex searching."""
        # Test with regex enabled
        self.everything.set_regex(True)
        regex_query = ".*\.txt$"  # Matches any file ending with .txt
        results = self.everything.search(regex_query)
        self.assertGreater(len(results), 0, "Expected results for regex search")
        # Verify that at least some results actually end with .txt
        found_txt = False
        for item in results:
            if item["name"].lower().endswith(".txt"):
                found_txt = True
                break
        self.assertTrue(found_txt, "No .txt files found in regex search results")

        # Test with regex disabled (should not find results for regex query)
        self.everything.set_regex(False)
        results_no_regex = self.everything.search(regex_query)
        # It's hard to assert 0 results here because a literal search for ".*\.txt$" might return something
        # if a file literally has that name. Instead, we'll just ensure it doesn't crash and reset.
        # A more robust test would involve creating and deleting a file with a literal regex name.
        # For now, we just ensure the function can be toggled.

        # Reset regex mode
        self.everything.set_regex(False)

    def test_set_request_flags_integration(self):
        """Integration test: Verify set_request_flags calls the DLL function correctly."""
        with patch('pyeverything.everything.load_everything_dll') as mock_load_dll, \
             patch('pyeverything.everything.init_functions') as mock_init_functions:
            mock_dll = MagicMock()
            mock_load_dll.return_value = mock_dll

            everything = Everything()

            # Test with a sample flag value
            test_flags = 0x00000001 # Example flag
            everything.set_request_flags(test_flags)
            mock_dll.Everything_SetRequestFlags.assert_called_with(test_flags)

    def test_set_max_integration(self):
        """Integration test: Verify set_max limits the number of search results."""
        query = "exe"  # A common query likely to return many results

        # Test with max_results = 1
        results = self.everything.search(query, count=1)
        self.assertEqual(len(results), 1, "Expected 1 result when max_results is 1")

        # Test with max_results = 2
        results = self.everything.search(query, count=2)
        self.assertEqual(len(results), 2, "Expected 2 results when max_results is 2")

        # Test with max_results = 3
        results = self.everything.search(query, count=3)
        self.assertEqual(len(results), 3, "Expected 3 results when max_results is 3")

        # Test with max_results = 4
        results = self.everything.search(query, count=4)
        self.assertEqual(len(results), 4, "Expected 4 results when max_results is 4")

        # Reset max_results to default (0 means no limit)
        self.everything.set_max(0)

    def test_set_offset_integration(self):
        """Integration test: Verify set_offset correctly offsets search results."""
        query = "exe"  # A common query likely to return many results

        # Get all results to establish a baseline
        all_results = self.everything.search(query, count=0, offset=0)

        if len(all_results) < 5:  # Ensure there are enough results to test offset
            self.skipTest("Not enough search results to test offset functionality effectively.")

        # Test with offset = 1
        offset_results_1 = self.everything.search(query, offset=1)
        self.assertEqual(len(offset_results_1), len(all_results) - 1, "Offset 1 should return one less result")
        self.assertEqual(offset_results_1[0], all_results[1], "First result with offset 1 should be second overall result")

        # Test with offset = 2
        offset_results_2 = self.everything.search(query, offset=2)
        self.assertEqual(len(offset_results_2), len(all_results) - 2, "Offset 2 should return two less results")
        self.assertEqual(offset_results_2[0], all_results[2], "First result with offset 2 should be third overall result")

        # Test with offset = 0 (reset)
        reset_results = self.everything.search(query, offset=0)
        self.assertEqual(len(reset_results), len(all_results), "Resetting offset to 0 should return all results")
        self.assertEqual(reset_results[0], all_results[0], "First result after reset should be original first result")

    def test_sort_results_by_path_integration(self):
        """Integration test: Verify sort_results_by_path calls the DLL function correctly."""
        with patch('pyeverything.everything.load_everything_dll') as mock_load_dll, \
             patch('pyeverything.everything.init_functions') as mock_init_functions:
            mock_dll = MagicMock()
            mock_load_dll.return_value = mock_dll

            everything = Everything()

            everything.sort_results_by_path()
            mock_dll.Everything_SortResultsByPath.assert_called_once()

if __name__ == '__main__':
    unittest.main()
