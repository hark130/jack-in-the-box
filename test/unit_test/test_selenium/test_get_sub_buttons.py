"""Unit test module for jitb_selenium.get_sub_buttons().

Typical Usage:
    python -m test                                                      # Run *all* the test cases
    python -m test.unit_test                                            # Run *all* unit test cases
    python -m test.unit_test.test_selenium                              # Run selenium tests
    python -m test.unit_test.test_selenium.test_get_sub_buttons         # Run these unit tests
    python -m test.unit_test.test_selenium.test_get_sub_buttons -k n01  # Run just the n01 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
# Local Imports
from jitb.jitb_selenium import get_sub_buttons


class TestJitbSeleniumGetSubButtons(TestJackboxGames):
    """The jitb_selenium.get_sub_buttons() unit test class.

    This class provides base functionality to run NEBS unit tests for
    jitb_selenium.get_sub_buttons().
    """

    DEFAULT_BUTTON_BY = By.XPATH        # We find buttons by XPath, by default.
    DEFAULT_BUTTON_VALUE = './/button'  # XPath value to find buttons.

    # CORE CLASS METHODS
    # Methods listed in call order
    def expect_buttons_return(self, filename: str, sub_by: str = By.ID,
                              sub_value: str = None) -> None:
        """Double do the button element extraction and pass that to self.expect_return."""
        # LOCAL VARIABLES
        child_element = None  # The WebElement found in web_element at sub_by and sub_value.
        button_elements = []  # List of button WebElements found in child_element

        # Create the web driver
        self.create_web_driver(filename=filename)
        # Find the child element
        try:
            child_element = self.web_driver.find_element(by=sub_by, value=sub_value)
        except (NoSuchElementException, StaleElementReferenceException) as err:
            self.fail_test_case(f'Failed to get child element using {sub_by}:{sub_value} '
                                f'with {err}')
        else:
            if not child_element:
                self.fail_test_case('web_driver.find_element() did not find anything for '
                                    f'{sub_by}:{sub_value}')
        # Find the child element's buttons
        button_elements = child_element.find_elements(by=self.DEFAULT_BUTTON_BY,
                                                      value=self.DEFAULT_BUTTON_VALUE)
        if not button_elements:
            self.fail_test_case('Failed to generate an expected return for '
                                f'{self.DEFAULT_BUTTON_BY}:{self.DEFAULT_BUTTON_VALUE}')
        self.expect_return(button_elements)

    def set_buttons_input(self, filename: str, in_by: Any = By.ID, in_value: Any = None,
                          use_kwargs: bool = False) -> None:
        """Setup the test input for this test case."""
        self.create_web_driver(filename=filename)
        if use_kwargs:
            self.set_test_input(web_driver=self.web_driver, sub_by=in_by, sub_value=in_value)
        else:
            self.set_test_input(self.web_driver, in_by, in_value)

    def call_callable(self) -> Any:
        """Calls jitb_selenium.get_sub_buttons().

        Overrides the parent method.  Defines the way to call jitb_selenium.get_sub_buttons().

        Args:
            None

        Returns:
            Return value of jitb_selenium.get_sub_buttons()

        Raises:
            Exceptions raised by jitb_selenium.get_sub_buttons() are bubbled up and handled by
                TediousUnitTest
        """
        return get_sub_buttons(*self._args, **self._kwargs)


class NormalTestJitbSeleniumGetSubButtons(TestJitbSeleniumGetSubButtons):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        filename = 'JackboxTV-login_start.html'  # File-based test input
        sub_by = By.ID                           # By for the sub-element
        sub_value = 'cc-main'                    # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n02_opening_instructions(self):
        """Quiplash 2 waiting to start.

        This page has hidden buttons in this inaccessible element.
        """
        filename = 'JackboxTv-Q2-waiting_to_start.html'  # File-based test input
        sub_by = By.ID                                   # By for the sub-element
        sub_value = 'lobby-main-menu'                    # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n03_q2_splash_page(self):
        """Quiplash 2 splash page.

        This page has hidden buttons, but not in this element.
        """
        filename = 'JackboxTv-Q2-splash_page.html'  # File-based test input
        sub_by = By.ID                              # By for the sub-element
        sub_value = 'state-logo'                    # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_return([])
        self.run_test()

    def test_n04_round_1(self):
        """Quiplash 2 Round 1 splash page.

        This page has hidden buttons, but not in this element.
        """
        filename = 'JackboxTv-Q2-Round_1.html'  # File-based test input
        sub_by = By.ID                          # By for the sub-element
        sub_value = 'state-round'               # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_return([])
        self.run_test()

    def test_n05_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Prompt_1.html'  # File-based test input
        sub_by = By.ID                                   # By for the sub-element
        sub_value = 'state-answer-question'              # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n06_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        sub_by = By.ID                                 # By for the sub-element
        sub_value = 'quiplash-vote'                    # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n07_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_2-Prompt_1.html'  # File-based test input
        sub_by = By.ID                                   # By for the sub-element
        sub_value = 'state-answer-question'              # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n08_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        filename = 'JackboxTv-Q2-Round_3.html'  # File-based test input
        sub_by = By.ID                          # By for the sub-element
        sub_value = 'state-round'               # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_return([])
        self.run_test()

    def test_n09_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1.html'  # File-based test input
        sub_by = By.ID                                   # By for the sub-element
        sub_value = 'state-answer-question'              # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n10_round_3_prompt_1_v2(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1-v2.html'  # File-based test input
        sub_by = By.ID                                      # By for the sub-element
        sub_value = 'state-answer-question'                 # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n11_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1.html'  # File-based test input
        sub_by = By.ID                                 # By for the sub-element
        sub_value = 'quiplash-vote'                    # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_buttons_return(filename=filename, sub_by=sub_by, sub_value=sub_value)
        self.run_test()

    def test_n12_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page.

        This page has hidden buttons, but not in this element.
        """
        filename = 'JackboxTv-Q2-Round_3-waiting.html'  # File-based test input
        sub_by = By.ID                                  # By for the sub-element
        sub_value = 'state-vote'                        # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_return([])
        self.run_test()

    def test_n13_game_over(self):
        """Quiplash 2 game over page.

        This page has hidden buttons, but not in this element.
        """
        filename = 'JackboxTv-Q2-Game_Over.html'  # File-based test input
        sub_by = By.ID                            # By for the sub-element
        sub_value = 'quiplash2-lobby-postgame'    # Name for the sub-element
        self.set_buttons_input(filename=filename, in_by=sub_by, in_value=sub_value)
        self.expect_return([])
        self.run_test()


class ErrorTestJitbSeleniumGetSubButtons(TestJitbSeleniumGetSubButtons):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_element_none(self):
        """Bad data type: web_driver == None."""
        self.set_test_input(web_driver=None)
        self.expect_exception(TypeError, 'Web driver may not be None')
        self.run_test()

    def test_e02_bad_data_type_web_element_path(self):
        """Bad data type: web_driver == Path()."""
        self.set_test_input(web_driver=Path() / 'test/test_input/JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e03_bad_data_type_by_none(self):
        """Bad data type: sub_by == None."""
        self.set_buttons_input(filename='JackboxTV-login_start.html', in_by=None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e04_bad_data_type_by_package_enum(self):
        """Bad data type: sub_by == By."""
        self.set_buttons_input(filename='JackboxTV-login_start.html', in_by=By)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e05_bad_data_type_by_enum_literal(self):
        """Bad data type: sub_by == By."""
        self.set_buttons_input(filename='JackboxTV-login_start.html', in_by='By.ID')
        self.expect_exception(ValueError,
                              'Use By value from the selenium.webdriver.common.by module')
        self.run_test()

    def test_e06_bad_data_type_value_list(self):
        """Bad data type: sub_value == []."""
        self.set_buttons_input(filename='JackboxTV-login_start.html', in_value=[])
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e07_bad_data_type_value_bytes(self):
        """Bad data type: sub_value == b''."""
        self.set_buttons_input(filename='JackboxTV-login_start.html', in_value=b'find-this')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


class SpecialTestJitbSeleniumGetSubButtons(TestJitbSeleniumGetSubButtons):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def set_buttons_input_kwargs(self, filename: str, in_by: Any = By.ID,
                                 in_value: Any = None) -> None:
        """Kwarg-enabled wrapper around set_buttons_input(use_kwargs=True)."""
        self.set_buttons_input(filename=filename, in_by=in_by, in_value=in_value, use_kwargs=True)

    def test_s01_bad_data_type_web_element_none(self):
        """Bad data type: web_driver == None."""
        self.set_test_input(web_driver=None)
        self.expect_exception(TypeError, 'Web driver may not be None')
        self.run_test()

    def test_s02_bad_data_type_web_element_path(self):
        """Bad data type: web_driver == Path()."""
        self.set_test_input(web_driver=Path() / 'test/test_input/JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_s03_bad_data_type_by_none(self):
        """Bad data type: sub_by == None."""
        self.set_buttons_input_kwargs(filename='JackboxTV-login_start.html', in_by=None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_s04_bad_data_type_by_package_enum(self):
        """Bad data type: sub_by == By."""
        self.set_buttons_input_kwargs(filename='JackboxTV-login_start.html', in_by=By)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_s05_bad_data_type_by_enum_literal(self):
        """Bad data type: sub_by == By."""
        self.set_buttons_input_kwargs(filename='JackboxTV-login_start.html', in_by='By.ID')
        self.expect_exception(ValueError,
                              'Use By value from the selenium.webdriver.common.by module')
        self.run_test()

    def test_s06_bad_data_type_value_list(self):
        """Bad data type: sub_value == []."""
        self.set_buttons_input_kwargs(filename='JackboxTV-login_start.html', in_value=[])
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_s07_bad_data_type_value_bytes(self):
        """Bad data type: sub_value == b''."""
        self.set_buttons_input_kwargs(filename='JackboxTV-login_start.html', in_value=b'find-this')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
