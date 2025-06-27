#!/usr/bin/env python3
import unittest
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

if __name__ == '__main__':
    unittest.main()
