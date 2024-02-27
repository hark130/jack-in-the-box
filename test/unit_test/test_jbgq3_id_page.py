"""Unit test module for JbgQ3.id_page().

Typical Usage:
    python -m test                                      # Run *all* the test cases
    python -m test.unit_test                            # Run *all* the unit test cases
    python -m test.unit_test.test_jbgq3_id_page         # Run just these unit tests
    python -m test.unit_test.test_jbgq3_id_page -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jbgames.jbg_q3 import JbgQ3


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

    def test_n06_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Prompt_1.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n07_round_1_vote_1(self):
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
