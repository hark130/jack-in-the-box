"""Unit test module for JbgQ3.id_page().

These unit tests will use source-controlled file-based input to create test input.

    Usage:
    1. Copy this file and rename it to `test_CALLABLE.py`
    2. Rename the internal 'CALLABLE' placeholders accordingly
    3. Source-control discretely named file-based test input (if applicable)
    4. Define numbered Test Cases within the NEBS classes whose name begins with `test_<NEBS>`
    5. `python3 -m test.unit_tests.test_CALLABLE` to run your test cases

    Troubleshooting:
    Q1. Why didn't my test cases run when I executed `python3 -m unittest`?
    A1a. Ensure your test case module's filename start with `test_`?
    A1b. Is there at least one method name that starts with `test_`?
    Q2. Why didn't my test cases execute with `python3 -m test.unit_tests.test_CALLABLE`?
    A2. Consider the following:
        - Did you replace the command's 'test_CALLABLE' with the actual name of your module?
        - Did you remove or comment out `execute_test_cases()` or the code block that executes
            `execute_test_cases()`?
        - Did you remove, comment, or modify `execute_test_cases()`'s behavior?
        - Is there at least one Test Case whose name starts with `test_`?
        - Try `python3 -m unittest -k CALLABLE` but replace CALLABLE with a substring related
            to your test cases and/or module
"""

# Standard Imports
from pathlib import Path
from typing import Any
import random
import warnings
# Third Party Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousunittest import TediousUnitTest
# Local Imports
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jbgames.jbg_q3 import JbgQ3
from jitb.jitb_openai import JitbAi
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames


class TestJbgQ3IdPage(TestJackboxGames):
    """JbgQ3.id_page() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ3.id_page().
    """

    username = 'Test_JBG_Q3_ID_PAGE'  # Default username to use for these unit tests

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls JbgQ3.id_page().

        Overrides the parent method.  Defines the way to call JbgQ3.id_page().

        Args:
            None

        Returns:
            Return value of JbgQ3.id_page()

        Raises:
            Exceptions raised by JbgQ3.id_page() are bubbled up and handled by TediousUnitTest
        """
        ai_obj = MockedJitbAi()
        jbg_q3_obj = JbgQ3(ai_obj=ai_obj, username=self.username)
        return jbg_q3_obj.id_page(*self._args, **self._kwargs)


class NormalTestJbgQ3IdPage(TestJbgQ3IdPage):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-login_start.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n02_selection_start(self):
        """Quiplash 3 Avatar page; unselected."""
        self.create_test_input('JackboxTv-Q3-avatar_selection-start.html')
        self.expect_return(JbgPageIds.AVATAR)
        self.run_test()

    def test_n03_selection_chosen(self):
        """Quiplash 3 Avatar page; selected."""
        self.create_test_input('JackboxTv-Q3-avatar_selection-selected.html')
        self.expect_return(JbgPageIds.AVATAR)
        self.run_test()

    def test_n04_opening_instructions(self):
        """Quiplash 3 instructions splash page."""
        self.create_test_input('JackboxTv-Q3-Opening_Instructions.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n05_round_1(self):
        """Quiplash 3 Round 1 splash page."""
        self.create_test_input('JackboxTv-Q3-Round_1.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n05_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Prompt_1.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n05_round_1_vote_1(self):
        """Quiplash 3 Round 1 Vote 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()


class ErrorTestJbgQ3IdPage(TestJbgQ3IdPage):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Error input that's expected to fail."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Error input that's expected to fail."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


class SpecialTestJbgQ3IdPage(TestJbgQ3IdPage):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        self.create_test_input('xkcd-Good_Code.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s02_kwarg(self):
        """Use the keyword argument."""
        self.create_test_input(filename='JackboxTV-login_start.html', use_kwarg=True)
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
