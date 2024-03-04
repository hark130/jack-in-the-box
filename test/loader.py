"""Defines functionality to assist with automated test case loading and execution.

Execute load_and_run() from the __main__.py of a Python package that implements unittest-based
test cases.

    Typical usage example:

    # File: test/unit_test/__main__.py
    from test.loader import load_and_run

    if __name__ == '__main__':
        load_and_run('test/unit_test')  # Loads and runs all unit tests
"""


# Standard Imports
import unittest
# Third Party Imports
from hobo.disk_operations import validate_directory
from hobo.validation import validate_type
# Local Imports


def load_and_run(dirname: str, verbosity: int = 2) -> bool:
    """Load and run all unittest test cases found within dirname.

    Args:
        dirname: Directory, relative or absolute, to begin searching for test cases.
        verbosity: Optional; Verbosity level passed to unittest.TextTestRunner
            0 (quiet): total numbers of tests executed and the global result
            1 (default): verbosity=0 plus a dot for every successful test or a F for every failure
            2 (verbose): you get the help string of every test and the result

    Returns:
        True if all test cases passed, false otherwise.

    Raises:
        TypeError: Invalid data type.
        ValueError: Empty dirname or unsupported verbosity level.
        FileNotFoundError: Unable to locate dirname.
    """
    # LOCAL VARIABLES
    loader = None       # Test case loading object
    test_suite = None   # Test Suite of "discovered" test cases
    test_runner = None  # Test Runner object to run the test suite and display results

    # INPUT VALIDATION
    # dirname
    validate_directory(dirname, 'dirname', must_exist=True)
    # verbosity
    validate_type(verbosity, 'verbosity', int)
    if verbosity not in [0, 1, 2]:
        raise ValueError(f'Unsupported verbosity level: {verbosity}')

    # LOAD
    loader = unittest.TestLoader()  # Test case loading object
    test_suite = loader.discover(dirname)
    test_runner = unittest.TextTestRunner(verbosity=verbosity)

    # RUN
    return test_runner.run(test_suite).wasSuccessful()
