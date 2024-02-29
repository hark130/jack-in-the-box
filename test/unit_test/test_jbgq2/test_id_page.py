"""Unit test module for JbgQ2.id_page().

Typical Usage:
    python -m test                                           # Run *all* the test cases
    python -m test.unit_test                                 # Run *all* the unit test cases
    python -m test.unit_test.test_jbgq2                      # Run *all* jbgq2 unit tests cases
    python -m test.unit_test.test_jbgq2.test_id_page         # Run just these unit tests
    python -m test.unit_test.test_jbgq2.test_id_page -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgq2.test_jbgq2 import TestJbgQ2
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_page_ids import JbgPageIds


class TestJbgQ2IdPage(TestJbgQ2):
    """JbgQ2.id_page() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ2.id_page().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls JbgQ2.id_page().

        Overrides the parent method.  Defines the way to call JbgQ2.id_page().

        Args:
            None

        Returns:
            Return value of JbgQ2.id_page()

        Raises:
            Exceptions raised by JbgQ2.id_page() are bubbled up and handled by TediousUnitTest
        """
        jbg_q2_obj = self.setup_jbgq2_object()
        return jbg_q2_obj.id_page(*self._args, **self._kwargs)


class NormalTestJbgQ2IdPage(TestJbgQ2IdPage):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-login_start.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n02_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        self.create_test_input('JackboxTv-Q2-waiting_to_start.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n03_q2_splash_page(self):
        """Quiplash 2 splash page."""
        self.create_test_input('JackboxTv-Q2-splash_page.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n04_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        self.create_test_input('JackboxTv-Q2-Round_1.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n05_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_1-Prompt_1.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n06_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_1-Vote_1.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n07_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_2-Prompt_1.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n08_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        self.create_test_input('JackboxTv-Q2-Round_3.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n09_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1.html')
        self.expect_return(JbgPageIds.Q2_LAST)
        self.run_test()

    def test_n10_round_3_prompt_1_v2(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-v2.html')
        self.expect_return(JbgPageIds.Q2_LAST)
        self.run_test()

    def test_n11_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n12_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        self.create_test_input('JackboxTv-Q2-Round_3-waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n13_game_over(self):
        """Quiplash 2 game over page."""
        self.create_test_input('JackboxTv-Q2-Game_Over.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()


class ErrorTestJbgQ2IdPage(TestJbgQ2IdPage):
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


class SpecialTestJbgQ2IdPage(TestJbgQ2IdPage):
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

    def test_s03_quiplash_3_selection_start(self):
        """Quiplash 3 Avatar page; unselected."""
        self.create_test_input('JackboxTv-Q3-avatar_selection-start.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s04_quiplash_3_selection_chosen(self):
        """Quiplash 3 Avatar page; selected."""
        self.create_test_input('JackboxTv-Q3-avatar_selection-selected.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s05_quiplash_3_opening_instructions(self):
        """Quiplash 3 instructions splash page."""
        self.create_test_input('JackboxTv-Q3-Opening_Instructions.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s06_quiplash_3_round_1(self):
        """Quiplash 3 Round 1 splash page."""
        self.create_test_input('JackboxTv-Q3-Round_1.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s07_quiplash_3_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Prompt_1.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s08_quiplash_3_round_1_vote_1(self):
        """Quiplash 3 Round 1 Vote 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s09_game_over_disconnected(self):
        """Quiplash 2 game over page; disconnected."""
        self.create_test_input('JackboxTv-Q2-Disconnected.html')
        self.expect_exception(RuntimeError, 'The room was disconnected')
        self.run_test()

    def test_s10_jitb_logic_flaw(self):
        """Live functional testing highlighted this logic flaw.

        Of course this isn't a prompt page... but how did it get there in the first place?
        """
        self.create_test_input('JackboxTv-Q2-Round_1-Vote_1-get_prompt-error.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
