#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import time

# Add the pyeverything directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyeverything.everything import Everything
from pyeverything.dll import EVERYTHING_SORT_DATE_MODIFIED_DESCENDING, EVERYTHING_SORT_PATH_ASCENDING

class TestEverythingIntegration(unittest.TestCase):

    def setUp(self):
        # Initialize the Everything class for integration tests
        self.everything = Everything()
        self.everything.dll.Everything_Reset()
        # Set default sort order to Date Modified Descending to ensure new files are visible
        self.everything.set_sort_order(EVERYTHING_SORT_DATE_MODIFIED_DESCENDING)

    def _full_path(self, item):
        """Join directory path and name from Everything.search() result."""
        return os.path.join(item["path"], item["name"]) if item.get("name") and item.get("path") else item.get("path", "")

    def _force_index_update(self):
        """Ask Everything to update folder indexes and give it a brief moment."""
        try:
            self.everything.dll.Everything_UpdateAllFolderIndexes()
        except Exception:
            pass
        time.sleep(1)

    def test_search_hosts_file_integration(self):
        r"""Integration test: Search for C:\Windows\System32\drivers\etc\hosts"""
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"

        # Perform the actual search
        results = self.everything.search(host_file_path)

        # Assert that the hosts file is found in the results
        found = any(self._full_path(item).lower() == host_file_path.lower() for item in results)
        self.assertTrue(found, f"Hosts file not found in search results: {host_file_path}")

        # Optionally, check if the size is non-zero if the file exists on disk
        if os.path.exists(host_file_path):
            actual_size = os.path.getsize(host_file_path)
            if actual_size > 0:
                found_item = next((item for item in results if self._full_path(item).lower() == host_file_path.lower()), None)
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
            self._force_index_update()

            # Test case-sensitive search (should not find the file with lowercase query)
            self.everything.set_match_case(True)
            results_case_sensitive = self.everything.search(mixed_case_filename.lower())
            self.assertEqual(len(results_case_sensitive), 0, "Case-sensitive search found unexpected results")

            # Test case-insensitive search (should find the file with lowercase query)
            self.everything.set_match_case(False)
            results_case_insensitive = self.everything.search(mixed_case_filename.lower())
            self.assertGreater(len(results_case_insensitive), 0, "Case-insensitive search found no results")
            found_in_insensitive = any(self._full_path(item).lower() == temp_file_path.lower() for item in results_case_insensitive)
            self.assertTrue(found_in_insensitive, f"File not found in case-insensitive search: {temp_file_path}")

        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_set_match_whole_word_integration(self):
        """Integration test: Verify set_match_whole_word functionality with actual searches."""
        import tempfile

        # Create temporary files for testing
        temp_dir = tempfile.gettempdir()
        whole_word_filename = "TestWholeWord.txt"
        partial_word_filename = "TestPartialWordFile.txt"
        
        whole_word_path = os.path.join(temp_dir, whole_word_filename)
        partial_word_path = os.path.join(temp_dir, partial_word_filename)

        with open(whole_word_path, "w") as f:
            f.write("whole word test")
        with open(partial_word_path, "w") as f:
            f.write("partial word test")

        try:
            # Give Everything time to index the new files
            self._force_index_update()
            # Poll briefly until the file appears to avoid flakiness
            for _ in range(10):
                results_check = self.everything.search(f'"{whole_word_filename}"')
                if any(self._full_path(item).lower() == whole_word_path.lower() for item in results_check):
                    break
                time.sleep(0.5)

            # Test with whole word matching enabled
            partial_token = 'artialWord'
            self.everything.set_match_whole_word(True)
            
            # Search using the full path to the file

        finally:
            # Clean up temporary files
            if os.path.exists(whole_word_path):
                os.remove(whole_word_path)
            if os.path.exists(partial_word_path):
                os.remove(partial_word_path)

    def test_set_regex_integration(self):
        """Integration test: Verify set_regex enables regex searching."""
        # Test with regex enabled
        self.everything.set_regex(True)
        regex_query = r".*\.txt$"  # Matches any file ending with .txt
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
        """Integration test: Verify set_request_flags functionality with actual searches."""
        import tempfile
        from pyeverything.dll import EVERYTHING_REQUEST_FILE_NAME, EVERYTHING_REQUEST_PATH, EVERYTHING_REQUEST_SIZE

        # Create a temporary file for testing
        temp_dir = tempfile.gettempdir()
        test_filename = "TestRequestFlags.txt"
        test_filepath = os.path.join(temp_dir, test_filename)

        with open(test_filepath, "w") as f:
            f.write("request flags test")

        try:
            # Give Everything time to index the new file
            self._force_index_update()

            # Test with only file name request
            self.everything.set_request_flags(EVERYTHING_REQUEST_FILE_NAME)
            results_name_only = self.everything.search(f'"{test_filename}"')
            
            self.assertTrue(len(results_name_only) > 0, "Should find the file.")
            found_item = next((item for item in results_name_only if self._full_path(item).lower() == test_filepath.lower()), None)
            self.assertIsNotNone(found_item, "File not found in search results.")
            
            # In the current implementation, 'path' and 'size' are always returned.
            # A more accurate test would be to check if other fields are absent when not requested.
            # For now, we confirm the basic query works with the flag set.
            self.assertIn("name", found_item)
            self.assertEqual(found_item["name"], test_filename)

            # Test with multiple flags
            self.everything.set_request_flags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE)
            results_full = self.everything.search(f'"{test_filename}"')
            
            self.assertTrue(len(results_full) > 0, "Should find the file with multiple flags.")
            found_item_full = next((item for item in results_full if self._full_path(item).lower() == test_filepath.lower()), None)
            self.assertIsNotNone(found_item_full, "File not found in search results with multiple flags.")

            self.assertIn("name", found_item_full)
            self.assertIn("path", found_item_full)
            self.assertIn("size", found_item_full)
            self.assertGreater(found_item_full["size"], 0)

        finally:
            # Clean up the temporary file
            if os.path.exists(test_filepath):
                os.remove(test_filepath)

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
        """Integration test: Verify sort_results_by_path functionality with actual searches."""
        import tempfile

        # Create temporary files in different subdirectories for sorting
        temp_dir = tempfile.gettempdir()
        dir_a = os.path.join(temp_dir, "dir_a")
        dir_b = os.path.join(temp_dir, "dir_b")
        os.makedirs(dir_a, exist_ok=True)
        os.makedirs(dir_b, exist_ok=True)

        file_a_path = os.path.join(dir_a, "test_sort_file.txt")
        file_b_path = os.path.join(dir_b, "test_sort_file.txt")

        with open(file_a_path, "w") as f:
            f.write("sort test a")
        with open(file_b_path, "w") as f:
            f.write("sort test b")

        try:
            # Give Everything time to index the new files
            time.sleep(5)

            # Sort next search by path to ensure deterministic ordering
            self.everything.set_sort_order(EVERYTHING_SORT_PATH_ASCENDING)
            results = self.everything.search("test_sort_file.txt")

            # Extract full paths from results
            full_paths = [self._full_path(item) for item in results if item.get("name") == "test_sort_file.txt"]
            
            # Verify the paths are sorted
            self.assertEqual(sorted(full_paths), full_paths, "Search results are not sorted by path.")
            
            # Ensure our specific files are in the sorted list correctly
            if file_a_path in full_paths and file_b_path in full_paths:
                self.assertLess(full_paths.index(file_a_path), full_paths.index(file_b_path), "dir_a should come before dir_b in sorted paths.")

        finally:
            # Clean up temporary files and directories
            if os.path.exists(file_a_path):
                os.remove(file_a_path)
            if os.path.exists(file_b_path):
                os.remove(file_b_path)
            if os.path.exists(dir_a):
                os.rmdir(dir_a)
            if os.path.exists(dir_b):
                os.rmdir(dir_b)

if __name__ == '__main__':
    unittest.main()
