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
        """Integration test: Verify set_regex calls the DLL function correctly."""
        with patch('pyeverything.everything.load_everything_dll') as mock_load_dll, \
             patch('pyeverything.everything.init_functions') as mock_init_functions:
            mock_dll = MagicMock()
            mock_load_dll.return_value = mock_dll

            everything = Everything()

            # Test with True
            everything.set_regex(True)
            mock_dll.Everything_SetRegex.assert_called_with(True)

            # Test with False
            everything.set_regex(False)
            mock_dll.Everything_SetRegex.assert_called_with(False)

            mock_dll.Everything_SetRegex.assert_called_with(False)

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

if __name__ == '__main__':
    unittest.main()
