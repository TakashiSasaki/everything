import pytest
import sys

def main():
    # Pass any arguments from the command line to pytest
    sys.exit(pytest.main(sys.argv[1:]))
