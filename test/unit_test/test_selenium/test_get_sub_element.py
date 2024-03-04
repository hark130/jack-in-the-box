"""Unit test module for jitb_selenium.get_element().

Typical Usage:
    python -m test                                                      # Run *all* the test cases
    python -m test.unit_test                                            # Run *all* unit test cases
    python -m test.unit_test.test_selenium                              # Run selenium tests
    python -m test.unit_test.test_selenium.test_get_sub_element         # Run these unit tests
    python -m test.unit_test.test_selenium.test_get_sub_element -k n01  # Run just the n01 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
from selenium.webdriver.common.by import By
import selenium
# Local Imports
from jitb.jitb_selenium import get_sub_element


class TestJitbSeleniumGetElement(TestJackboxGames):
    """The jitb_selenium.get_element() unit test class.

    This class provides base functionality to run NEBS unit tests for jitb_selenium.get_element().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def get_element_input(self, filename: str, by_arg: By = By.ID, value: str = None) \
            -> selenium.webdriver.remote.webelement.WebElement:
        """Use filename to create a web driver, fetch element value, and set that as input.

        1. Call self.create_web_driver()
        2. Call self.web_driver.get_element(by=by, value=value)
        3. Return the result

        Args:
            filename: Load this with a web driver.
            by: Optional; Selector to use when calling get_element().
            value: Optional; ID title to find in filename's web driver.

        Returns:
            A WebElement on success, None if not found.
        """
        self.create_web_driver(filename=filename)
        return self.web_driver.find_element(by=by_arg, value=value)

    def expect_element_return(self, parent_element: selenium.webdriver.remote.webelement.WebElement,
                              by_arg: By = By.ID, value: str = None) -> None:
        """Double do the child element extraction and pass that to self.expect_return."""
        child_element = parent_element.find_element(by=by_arg, value=value)
        if not child_element:
            self.fail_test_case(f'Failed to generate an expected return for {by_arg}:{value}')
        self.expect_return(child_element)

    # pylint: disable=too-many-arguments
    def set_element_input(self, filename: str, parent_by: By, parent_value: str,
                          child_by: Any, child_value: Any) \
            -> selenium.webdriver.remote.webelement.WebElement:
        """Setup the test input for this test case.

        1. Call self.get_element_input(filename, parent_by, parent_value) to get and element
            to search.
        2. Set that haystack element, along with child_by and child_value, as the actual test
            case input.

        Returns:
            The parent element used as the test input.  Use this element to 'double do' the
            expected results.
        """
        # LOCAL VARIABLES
        parent_element = self.get_element_input(filename=filename, by_arg=parent_by,
                                                value=parent_value)
        self.set_test_input(parent_element, child_by, child_value)
        return parent_element
    # pylint: enable=too-many-arguments

    def call_callable(self) -> Any:
        """Calls jitb_selenium.get_element().

        Overrides the parent method.  Defines the way to call jitb_selenium.get_element().

        Args:
            None

        Returns:
            Return value of jitb_selenium.get_element()

        Raises:
            Exceptions raised by jitb_selenium.get_element() are bubbled up and handled by
                TediousUnitTest
        """
        return get_sub_element(*self._args, **self._kwargs)


class NormalTestJitbSeleniumGetElement(TestJitbSeleniumGetElement):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'state-answer-question'  # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text'           # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='JackboxTv-Q2-Round_1-Prompt_1.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.expect_element_return(parent_element=parent_element, by_arg=child_by,
                                   value=child_value)
        self.run_test()

    def test_n02_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'game'                   # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text'           # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='JackboxTv-Q2-Round_1-Vote_1.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.expect_element_return(parent_element=parent_element, by_arg=child_by,
                                   value=child_value)
        self.run_test()

    def test_n03_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 Last Lash prompt page v1."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'page-quiplash'          # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text-alt'       # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='JackboxTv-Q2-Round_3-Prompt_1.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.expect_element_return(parent_element=parent_element, by_arg=child_by,
                                   value=child_value)
        self.run_test()

    def test_n04_round_3_prompt_1_v2(self):
        """Quiplash 2 Round 3 Last Lash prompt page v2."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'page-quiplash'          # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text-alt'       # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='JackboxTv-Q2-Round_3-Prompt_1-v2.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.expect_element_return(parent_element=parent_element, by_arg=child_by,
                                   value=child_value)
        self.run_test()

    def test_n05_round_3_vote_1_v1(self):
        """Quiplash 2 Round 3 Last Lash vote page v1."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'page-quiplash'          # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text-alt'       # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='JackboxTv-Q2-Round_3-Vote_1.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.expect_element_return(parent_element=parent_element, by_arg=child_by,
                                   value=child_value)
        self.run_test()

    def test_n06_round_3_vote_1_v2(self):
        """Quiplash 2 Round 3 Last Lash vote page v2."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'page-quiplash'          # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text-alt'       # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='JackboxTv-Q2-Round_3-Vote_1-v2.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.expect_element_return(parent_element=parent_element, by_arg=child_by,
                                   value=child_value)
        self.run_test()


class ErrorTestJitbSeleniumGetElement(TestJitbSeleniumGetElement):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_element_none(self):
        """Bad data type: web_element == None."""
        self.set_test_input(web_element=None)
        self.expect_exception(TypeError, 'Web element may not be None')
        self.run_test()

    def test_e02_bad_data_type_web_element_path(self):
        """Bad data type: web_element == Path()."""
        self.set_test_input(web_element=Path() / 'test/test_input/JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e03_bad_data_type_by_none(self):
        """Bad data type: by_arg == None."""
        self.set_test_input(
            web_element=self.get_element_input(filename='JackboxTV-login_start.html',
                                               value='app'), by_arg=None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e04_bad_data_type_by_package_enum(self):
        """Bad data type: by_arg == By."""
        self.set_test_input(
            web_element=self.get_element_input(filename='JackboxTV-login_start.html',
                                               value='app'), by_arg=By)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e05_bad_data_type_by_enum_literal(self):
        """Bad data type: by_arg == By."""
        self.set_test_input(
            web_element=self.get_element_input(filename='JackboxTV-login_start.html',
                                               value='app'), by_arg='By.ID')
        self.expect_exception(ValueError,
                              'Use By value from the selenium.webdriver.common.by module')
        self.run_test()

    def test_e06_bad_data_type_value_list(self):
        """Bad data type: value == []."""
        self.set_test_input(
            web_element=self.get_element_input(filename='JackboxTV-login_start.html',
                                               value='app'), value=[])
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e07_bad_data_type_value_bytes(self):
        """Bad data type: value == b''."""
        self.set_test_input(
            web_element=self.get_element_input(filename='JackboxTV-login_start.html',
                                               value='app'), value=b'find-this')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


class SpecialTestJitbSeleniumGetElement(TestJitbSeleniumGetElement):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        parent_by = By.ID                       # By type of the parent element
        parent_value = 'comic'                  # Name of the parent element
        child_by = By.ID                        # Child element by type (actual test input)
        child_value = 'question-text'           # Child element value name (actual test input)
        # Parent element (actual test input)
        parent_element = self.set_element_input(filename='xkcd-Good_Code.html',
                                                parent_by=parent_by, parent_value=parent_value,
                                                child_by=child_by, child_value=child_value)
        self.set_test_input(parent_element, child_by, child_value)
        self.expect_return(None)
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
