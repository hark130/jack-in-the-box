"""Unit test module for JbgBr.id_page().

Typical Usage:
    python -m test                                           # Run *all* the test cases
    python -m test.unit_test                                 # Run *all* the unit test cases
    python -m test.unit_test.test_jbgbr                      # Run *all* jbgbr unit tests cases
    python -m test.unit_test.test_jbgbr.test_id_page         # Run just these unit tests
    python -m test.unit_test.test_jbgbr.test_id_page -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgbr.test_jbgbr import TestJbgBr
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_page_ids import JbgPageIds


# pylint: disable = too-many-public-methods
class TestJbgBrIdPage(TestJbgBr):
    """JbgBr.id_page() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgBr.id_page().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls JbgBr.id_page().

        Overrides the parent method.  Defines the way to call JbgBr.id_page().

        Args:
            None

        Returns:
            Return value of JbgBr.id_page()

        Raises:
            Exceptions raised by JbgBr.id_page() are bubbled up and handled by TediousUnitTest
        """
        jbg_br_obj = self.setup_jbgbr_object()
        return jbg_br_obj.id_page(*self._args, **self._kwargs)


class NormalTestJbgBrIdPage(TestJbgBrIdPage):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_generic_login_page(self):
        """Jackbox.tv Login page (generic)."""
        self.create_test_input('JackboxTV-JB-Login_start.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n02_br_login_page(self):
        """Blather Round Login page."""
        self.create_test_input('JackboxTV-BR-1a-Login_Page-pre_login.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n03_br_post_login(self):
        """Blather Round waiting to start."""
        self.create_test_input('JackboxTV-BR-1b-Login_Page-waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n04_br_round_1_choose_secret_prompt(self):
        """Blather Round choose secret prompt."""
        self.create_test_input('JackboxTV-BR-2-Choose_Prompt.html')
        self.expect_return(JbgPageIds.BR_SECRET)
        self.run_test()

    def test_n05_br_round_1_post_secret_prompt(self):
        """Blather Round after secret prompt selection."""
        self.create_test_input('JackboxTV-BR-2b-Choose_Prompt-waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n06_br_round_1_describe_1a_make_sentence(self):
        """Blather Round describe secret prompt: make a sentence about the secret prompt."""
        self.create_test_input('JackboxTV-BR-3-Make_Sentence.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n07_br_round_1_describe_2a_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-4a-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n08_br_round_1_describe_2b_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-4b-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n09_br_round_1_describe_2c_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-4c-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n10_br_round_1_describe_2d_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-4d-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n11_br_round_1_describe_2e_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-4e-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n12_br_round_1_guess_story_1a(self):
        """Blather Round guess the secret prompt: story."""
        self.create_test_input('JackboxTV-BR-5a-Guess.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n13_br_round_1_guess_story_1b(self):
        """Blather Round guess the secret prompt: story."""
        self.create_test_input('JackboxTV-BR-5b-Guess.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n14_br_round_1_guess_story_1c(self):
        """Blather Round guess the secret prompt: story."""
        self.create_test_input('JackboxTV-BR-5c-Guess.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n15_br_round_1_guess_story_1d(self):
        """Blather Round guess the secret prompt: story."""
        self.create_test_input('JackboxTV-BR-5d-Guess.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n16_br_round_1_guess_place_1a(self):
        """Blather Round guess the secret prompt: place."""
        self.create_test_input('JackboxTV-BR-6a-Guess_Place.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n17_br_round_1_guess_place_1b(self):
        """Blather Round guess the secret prompt: place."""
        self.create_test_input('JackboxTV-BR-6b-Guess_Place.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n18_br_round_1_guess_place_1c(self):
        """Blather Round guess the secret prompt: place; guessed wrong."""
        self.create_test_input('JackboxTV-BR-6c-Guess_Place-guessed_wrong.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n19_br_round_1_guess_place_1d(self):
        """Blather Round guess the secret prompt: place."""
        self.create_test_input('JackboxTV-BR-6d-Guess_Place.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n20_br_round_1_guess_place_1e(self):
        """Blather Round guess the secret prompt: place."""
        self.create_test_input('JackboxTV-BR-6e-Guess_Place-guessed_wrong.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n21_br_round_1_guess_place_1f(self):
        """Blather Round guess the secret prompt: place."""
        self.create_test_input('JackboxTV-BR-6f-Guess_Place-guessed_right-waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n22_br_round_2_choose_secret_prompt(self):
        """Blather Round choose secret prompt."""
        self.create_test_input('JackboxTV-BR-Round_2-1-Choose_Prompt.html')
        self.expect_return(JbgPageIds.BR_SECRET)
        self.run_test()

    def test_n23_br_round_2_describe_1a_make_sentence(self):
        """Blather Round describe secret prompt: make a sentence about the secret prompt."""
        self.create_test_input('JackboxTV-BR-Round_2-2-Make_Sentence.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n24_br_round_2_describe_2a_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-Round_2-3a-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n25_br_round_2_describe_2b_continue(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-Round_2-3b-Describe.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n26_br_round_2_describe_2c_with_guesses(self):
        """Blather Round describe secret prompt: describe the secret prompt."""
        self.create_test_input('JackboxTV-BR-Round_2-3c-Describe_with_guesses.html')
        self.expect_return(JbgPageIds.BR_DESCRIBE)
        self.run_test()

    def test_n27_br_round_2_guess_person_1a(self):
        """Blather Round guess the secret prompt: person."""
        self.create_test_input('JackboxTV-BR-Round_2-4a-Guess_person.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n28_br_round_2_guess_person_1b(self):
        """Blather Round guess the secret prompt: person."""
        self.create_test_input('JackboxTV-BR-Round_2-4b-Guess_person.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n29_br_round_2_guess_person_1c(self):
        """Blather Round guess the secret prompt: person."""
        self.create_test_input('JackboxTV-BR-Round_2-4c-Guess_person.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()


class ErrorTestJbgBrIdPage(TestJbgBrIdPage):
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


class SpecialTestJbgBrIdPage(TestJbgBrIdPage):
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

    def test_s05_quiplash_3_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Prompt_1.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s06_quiplash_3_round_1_vote_1(self):
        """Quiplash 3 Round 1 Vote 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_s07_game_over_disconnected(self):
        """Joke Boat game over page; disconnected."""
        self.create_test_input('JackboxTV-JB-Game_Done-disconnected.html')
        self.expect_exception(RuntimeError, 'The room was disconnected')
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
