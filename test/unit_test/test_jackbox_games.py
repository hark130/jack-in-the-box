"""Base class for common Jackbox Games unit testing functionality."""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tediousstart.tediousunittest import TediousUnitTest
# Local Imports
from jitb.jitb_logger import Logger


class TestJackboxGames(TediousUnitTest):
    """Jackbox Games unit test class.

    This class provides base functionality to run NEBS unit tests for the JbgAbc child classes.
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def __init__(self, *args, **kwargs) -> None:
        """TestJbgQ3IdPage ctor.

        TestJbgQ3IdPage constructor.  Initializes attributes after constructing the parent
        object.

        Args:
            args: Arguments to pass to the parent class ctor
            kwargs: Keyword arguments to pass to the parent class ctor

        Returns:
            None

        Raises:
            None
        """
        super().__init__(*args, **kwargs)
        self.web_driver = None  # Selenium based Chrome web driver

    def setUp(self) -> None:
        """Prepares Test Case.

        Automate any preparation necessary before each Test Case executes.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        super().setUp()
        Logger.initialize(debugging=True)  # Enable DEBUG logging while testing

    def tearDown(self) -> None:
        """Close the web driver."""
        super().tearDown()
        if self.web_driver:
            self.web_driver.quit()
        Logger.shutdown()

    def call_callable(self) -> Any:
        """Child class defines test case callable.

        This method must be overridden by the child class.

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # return jbgames_obj.the_method_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self._test_error.format('The child class must override the call_callable method'))

    def create_web_driver(self, filename: str) -> None:
        """Translates file-based test input into a Selenium web driver for the self.web_driver."""
        # LOCAL VARIABLES
        input_html = Path() / 'test' / 'test_input' / filename   # File-based test input
        options = Options()                                      # Options for the web driver

        # VALIDATION
        if not input_html.is_file():
            self.fail_test_case(f'Filename {input_html.absolute()} is not actually a file.')

        # SETUP
        options.add_argument('--headless')
        if not self.web_driver:
            self.web_driver = webdriver.Chrome(options=options)
            self.web_driver.minimize_window()
            self.web_driver.get(input_html.absolute().as_uri())

    def create_web_input(self, filename: Path, use_kwarg: bool = False) -> None:
        """Translate a path object into test input.

        Args:
            filename: Path object to convert to a web driver and use as file-based test input.
            use_kwarg: Optional; Will call the function using keyword arguments.
        """
        self.create_web_driver(filename=filename)  # Unit test input
        if use_kwarg:
            self.set_test_input(web_driver=self.web_driver)
        else:
            self.set_test_input(self.web_driver)

    def create_test_input(self, filename: str, use_kwarg: bool = False) -> None:
        """Translates file-based test input into a Selenium web driver for test case input.

        Calls self.create_web_driver() to create the web driver.  Then passes that web driver
        to self.set_test_input().
        """
        # LOCAL VARIABLES
        input_html = Path() / 'test' / 'test_input' / filename   # File-based test input

        # CREATE WEB DRIVER
        self.create_web_driver(filename=filename)
        if not self.web_driver:
            self.fail_test_case('Failed to create a web driver')

        # CREATE TEST INPUT
        self.web_driver.get(input_html.absolute().as_uri())
        if use_kwarg:
            self.set_test_input(web_driver=self.web_driver)
        else:
            self.set_test_input(self.web_driver)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate JbgQ3.id_page() return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.  Calls self._validate_return_value() method under the hood.

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.  The intended practice is to use the return value of the
                call_callable() method.

        Returns:
            None

        Raises:
            None
        """
        self._validate_return_value(return_value=return_value)
