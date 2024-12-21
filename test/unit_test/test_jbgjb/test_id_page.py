"""Unit test module for JbgJb.id_page().

Typical Usage:
    python -m test                                           # Run *all* the test cases
    python -m test.unit_test                                 # Run *all* the unit test cases
    python -m test.unit_test.test_jbgjb                      # Run *all* jbgjb unit tests cases
    python -m test.unit_test.test_jbgjb.test_id_page         # Run just these unit tests
    python -m test.unit_test.test_jbgjb.test_id_page -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgjb.test_jbgjb import TestJbgJb
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_page_ids import JbgPageIds


# pylint: disable = too-many-public-methods
class TestJbgJbIdPage(TestJbgJb):
    """JbgJb.id_page() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgJb.id_page().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls JbgJb.id_page().

        Overrides the parent method.  Defines the way to call JbgJb.id_page().

        Args:
            None

        Returns:
            Return value of JbgJb.id_page()

        Raises:
            Exceptions raised by JbgJb.id_page() are bubbled up and handled by TediousUnitTest
        """
        jbg_jb_obj = self.setup_jbgjb_object()
        return jbg_jb_obj.id_page(*self._args, **self._kwargs)


class NormalTestJbgJbIdPage(TestJbgJbIdPage):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-JB-Login_start.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n02_choose_catchphrase(self):
        """Joke Boat select catchphrase."""
        self.create_test_input('JackboxTV-JB-Login_catchphrase_start.html')
        self.expect_return(JbgPageIds.JB_CATCH)
        self.run_test()

    def test_n03_waiting_on_other_players(self):
        """Joke Boat waiting to start."""
        self.create_test_input('JackboxTV-JB-Login_waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n04_write_joke_topic_v1(self):
        """Joke Boat write joke topic page v1."""
        self.create_test_input('JackboxTV-JB-Write_joke_topic_v1.html')
        self.expect_return(JbgPageIds.JB_TOPIC)
        self.run_test()

    def test_n05_write_joke_topic_v2(self):
        """Joke Boat write joke topic page v2."""
        self.create_test_input('JackboxTV-JB-Write_joke_topic_v2.html')
        self.expect_return(JbgPageIds.JB_TOPIC)
        self.run_test()

    def test_n06_write_joke_topic_v3(self):
        """Joke Boat write joke topic page v3."""
        self.create_test_input('JackboxTV-JB-Write_joke_topic_v3.html')
        self.expect_return(JbgPageIds.JB_TOPIC)
        self.run_test()

    def test_n07_write_joke_topic_v4(self):
        """Joke Boat write joke topic page v4."""
        self.create_test_input('JackboxTV-JB-Write_joke_topic_v4.html')
        self.expect_return(JbgPageIds.JB_TOPIC)
        self.run_test()

    def test_n08_more_waiting(self):
        """Joke Boat post-joke topic page; waiting."""
        self.create_test_input('JackboxTV-JB-Post_joke_topic_waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n09_round_1_joke_1a_choose_setup(self):
        """Joke Boat Round 1 Joke 1a choose setup page."""
        self.create_test_input('JackboxTV-JB-Round_1-Joke_1-A_Choose_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n10_round_1_joke_1b_complete_setup(self):
        """Joke Boat Round 1 Joke 1b complete setup page."""
        self.create_test_input('JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n11_round_1_joke_1c_complete_punchline(self):
        """Joke Boat Round 1 Joke 1c complete punchline page."""
        self.create_test_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n12_round_1_joke_2a_choose_setup(self):
        """Joke Boat Round 1 Joke 2a choose setup page."""
        self.create_test_input('JackboxTV-JB-Round_1-Joke_2-A_Choose_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n13_round_1_joke_2b_complete_setup(self):
        """Joke Boat Round 1 Joke 2b complete setup page."""
        self.create_test_input('JackboxTV-JB-Round_1-Joke_2-B_Complete_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n14_round_1_joke_2c_complete_punchline(self):
        """Joke Boat Round 1 Joke 2c complete punchline page."""
        self.create_test_input('JackboxTV-JB-Round_1-Joke_2-C_Complete_your_punchline.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n15_round_1_waiting(self):
        """Joke Boat post-round 1 joke-completion; waiting."""
        self.create_test_input('JackboxTV-JB-Round_1_waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n16_round_1_vote_1(self):
        """Joke Boat Round 1 vote page."""
        self.create_test_input('JackboxTV-JB-Round_1-Vote_1.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n17_round_1_perform_joke_1(self):
        """Joke Boat Round 1 Your Turn; Perform joke 1? page."""
        self.create_test_input('JackboxTV-JB-Round_1-Perform_joke_1.html')
        self.expect_return(JbgPageIds.JB_PERFORM)
        self.run_test()

    def test_n18_round_1_perform_joke_2(self):
        """Joke Boat Round 1 Your Turn; Perform joke 2? page."""
        self.create_test_input('JackboxTV-JB-Round_1-Perform_joke_2.html')
        self.expect_return(JbgPageIds.JB_PERFORM)
        self.run_test()

    def test_n19_round_2_joke_1a_choose_setup(self):
        """Joke Boat Round 2 Joke 1a choose setup page."""
        self.create_test_input('JackboxTV-JB-Round_2-Joke_1-A_Choose_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n20_round_2_joke_1b_complete_setup(self):
        """Joke Boat Round 2 Joke 1b complete setup page."""
        self.create_test_input('JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n21_round_2_joke_1c_complete_punchline(self):
        """Joke Boat Round 2 Joke 1c complete punchline page."""
        self.create_test_input('JackboxTV-JB-Round_2-Joke_1-C_Complete_your_punchline.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n22_round_2_joke_2a_choose_setup(self):
        """Joke Boat Round 2 Joke 2a choose setup page."""
        self.create_test_input('JackboxTV-JB-Round_2-Joke_2-A_Choose_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n23_round_2_joke_2b_complete_setup(self):
        """Joke Boat Round 2 Joke 2b complete setup page."""
        self.create_test_input('JackboxTV-JB-Round_2-Joke_2-B_Complete_setup.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n24_round_2_joke_2c_complete_punchline(self):
        """Joke Boat Round 2 Joke 2c complete punchline page."""
        self.create_test_input('JackboxTV-JB-Round_2-Joke_2-C_Complete_your_punchline.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n25_round_2_vote_1(self):
        """Joke Boat Round 2 vote page."""
        self.create_test_input('JackboxTV-JB-Round_2-Vote_1.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n26_round_2_perform_joke_1(self):
        """Joke Boat Round 2 Your Turn; Perform joke 1? page."""
        self.create_test_input('JackboxTV-JB-Round_2-Perform_joke_1.html')
        self.expect_return(JbgPageIds.JB_PERFORM)
        self.run_test()

    def test_n27_round_2_perform_joke_2(self):
        """Joke Boat Round 2 Your Turn; Perform joke 2? page."""
        self.create_test_input('JackboxTV-JB-Round_2-Perform_joke_2.html')
        self.expect_return(JbgPageIds.JB_PERFORM)
        self.run_test()

    def test_n28_round_3a_pick_a_joke(self):
        """Joke Boat Round 3a pick a joke to rewrite."""
        self.create_test_input('JackboxTV-JB-Round_3-A_Pick_a_joke.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n29_round_3b_rewrite_punchline(self):
        """Joke Boat Round 3b rewrite punchline."""
        self.create_test_input('JackboxTV-JB-Round_3-B_Rewrite_punchline.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n30_round_3_perform_joke_1(self):
        """Joke Boat Round 3 Your Turn; Perform joke 1? page."""
        self.create_test_input('JackboxTV-JB-Round_3-Perform_joke_1.html')
        self.expect_return(JbgPageIds.JB_PERFORM)
        self.run_test()

    def test_n31_game_done_waiting(self):
        """Joke Boat game done; waiting page."""
        self.create_test_input('JackboxTV-JB-Game_Done-waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()


class ErrorTestJbgJbIdPage(TestJbgJbIdPage):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Error input that's expected to fail."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Error input that's expected to fail."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'expected type')
        self.run_test()


class SpecialTestJbgJbIdPage(TestJbgJbIdPage):
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
        """Joke Boat game over page; disconnected."""
        self.create_test_input('JackboxTV-JB-Game_Done-disconnected.html')
        self.expect_exception(RuntimeError, 'The room was disconnected')
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
