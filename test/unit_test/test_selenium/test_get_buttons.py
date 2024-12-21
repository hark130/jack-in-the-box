"""Unit test module for jitb_selenium.get_buttons().

Typical Usage:
    python -m test                                                  # Run *all* the test cases
    python -m test.unit_test                                        # Run *all* unit test cases
    python -m test.unit_test.test_selenium                          # Run selenium tests
    python -m test.unit_test.test_selenium.test_get_buttons         # Run these unit tests
    python -m test.unit_test.test_selenium.test_get_buttons -k n01  # Run just the n01 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
from selenium.webdriver.common.by import By
# Local Imports
from jitb.jitb_selenium import get_buttons


class TestJitbSeleniumGetButtons(TestJackboxGames):
    """The jitb_selenium.get_buttons() unit test class.

    This class provides base functionality to run NEBS unit tests for
    jitb_selenium.get_buttons().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def expect_buttons_return(self, filename: str, by_arg: str = By.XPATH,
                              value: str = '//button') -> None:
        """Double do the button element extraction and pass that to self.expect_return."""
        self.create_web_driver(filename=filename)
        child_elements = self.web_driver.find_elements(by=by_arg, value=value)  # Expected return
        if not child_elements:
            self.fail_test_case(f'Failed to generate an expected return for {by_arg}:{value}')
        self.expect_return(child_elements)

    def set_buttons_input(self, filename: str, use_kwargs: bool = False) -> None:
        """Setup the test input for this test case."""
        self.create_web_driver(filename=filename)
        if use_kwargs:
            self.set_test_input(web_driver=self.web_driver)
        else:
            self.set_test_input(self.web_driver)

    def call_callable(self) -> Any:
        """Calls jitb_selenium.get_buttons().

        Overrides the parent method.  Defines the way to call jitb_selenium.get_buttons().

        Args:
            None

        Returns:
            Return value of jitb_selenium.get_buttons()

        Raises:
            Exceptions raised by jitb_selenium.get_buttons() are bubbled up and handled by
                TediousUnitTest
        """
        return get_buttons(*self._args, **self._kwargs)


class NormalTestJitbSeleniumGetButtons(TestJitbSeleniumGetButtons):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        filename = 'JackboxTV-login_start.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n02_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        filename = 'JackboxTv-Q2-waiting_to_start.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n03_q2_splash_page(self):
        """Quiplash 2 splash page."""
        filename = 'JackboxTv-Q2-splash_page.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n04_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        filename = 'JackboxTv-Q2-Round_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n05_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Prompt_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n06_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n07_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_2-Prompt_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n08_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        filename = 'JackboxTv-Q2-Round_3.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n09_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n10_round_3_prompt_1_v2(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1-v2.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n11_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n12_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        filename = 'JackboxTv-Q2-Round_3-waiting.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()

    def test_n13_game_over(self):
        """Quiplash 2 game over page."""
        filename = 'JackboxTv-Q2-Game_Over.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_buttons_return(filename)
        self.run_test()


class ErrorTestJitbSeleniumGetButtons(TestJitbSeleniumGetButtons):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_element_none(self):
        """Bad data type: web_driver == None."""
        self.set_test_input(web_driver=None)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e02_bad_data_type_web_element_path(self):
        """Bad data type: web_driver == Path()."""
        self.set_test_input(web_driver=Path() / 'test/test_input/JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'expected type')
        self.run_test()


class SpecialTestJitbSeleniumGetButtons(TestJitbSeleniumGetButtons):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        filename = 'xkcd-Good_Code.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
