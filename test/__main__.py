"""Defines the logic for running all existing unittest test cases as a package.

    Typical usage example:

    python -m test
"""
# Standard Imports
import sys
# Third Party Imports
# Local Imports
from test.loader import load_and_run


if __name__ == '__main__':
    # Run all test cases discovered in this package
    # Exit 0 on success, 1 otherwise
    sys.exit(not load_and_run('test'))
