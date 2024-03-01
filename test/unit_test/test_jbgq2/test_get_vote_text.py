"""Unit test module for JbgQ2.get_vote_text().

Typical Usage:
    python -m test                                                 # Run *all* the test cases
    python -m test.unit_test                                       # Run *all* the unit test cases
    python -m test.unit_test.test_jbgq2                            # Run *all* jbgq2 unit tests
    python -m test.unit_test.test_jbgq2.test_get_vote_text         # Run just these unit tests
    python -m test.unit_test.test_jbgq2.test_get_vote_text -k n01  # Run just this normal 1 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
from unittest import skip
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_q2 import get_vote_text


class TestJbgQ2GetVoteText(TestJackboxGames):
    """The jbg_q2.get_vote_text() unit test class.

    This class provides base functionality to run NEBS unit tests for jbg_q2.get_vote_text().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def expect_standard_exception(self) -> None:
        """Expect RuntimeError('This is not a vote page')."""
        self.expect_exception(RuntimeError, 'This is not a vote page')

    def call_callable(self) -> Any:
        """Calls jbg_q2.get_vote_text().

        Overrides the parent method.  Defines the way to call jbg_q2.get_vote_text().

        Args:
            None

        Returns:
            Return value of jbg_q2.get_vote_text()

        Raises:
            Exceptions raised by jbg_q2.get_vote_text() are bubbled up and handled by
            TediousUnitTest.
        """
        return get_vote_text(*self._args, **self._kwargs)


class NormalTestJbgQ2GetVoteText(TestJbgQ2GetVoteText):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_1-Vote_1.html')
        self.expect_return('An inappropriate time to wear a tuxedo\n' +
                           'Which one do you like more?\n'.upper() +
                           'SCRAPPLE\nBUTTE, MONTANA')
        self.run_test()

    def test_n02_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Vote_1.html')
        self.expect_return('Come up with a new hilarious sitcom with this word in the title:\n'
                           'SLIME\n' + 'Which one do you like more?'.upper() + '\nSLIMER\nSLIMEY')
        self.run_test()

    def test_n03_round_3_vote_1_v2(self):
        """Quiplash 2 Round 3 Vote 1 v2 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Vote_1-v2.html')
        self.expect_return('Come up with a full name for this acronym!\nW.A.W.\n'
                           + 'Which one do you like more?'.upper() + '\nWIN A WAR\n5')
        self.run_test()

    def test_n04_round_3_vote_1_v3(self):
        """Quiplash 2 Round 3 Vote 1 v3 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Vote_1-v3.html')
        self.expect_return('Come up with a full name for this acronym!\nG.O.R.\n'
                           + 'Which one do you like more?'.upper() + '\nGET ON READ\n'
                           + 'GUMMY ORGASM RECIPE')
        self.run_test()

    def test_n05_round_3_vote_1_acro_lash(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Acro Lash."""
        self.create_web_input('JackboxTv-Q2-Round_3-Vote_1-v3.html')
        self.expect_return('Come up with a full name for this acronym!\nG.O.R.\n'
                           + 'Which one do you like more?'.upper() + '\nGET ON READ\n'
                           + 'GUMMY ORGASM RECIPE')
        self.run_test()

    @skip('test_n06_round_3_vote_1_comic_lash needs test input')
    def test_n06_round_3_vote_1_comic_lash(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Comic Lash."""
        self.create_web_input('')
        self.expect_return('')
        self.run_test()

    def test_n07_round_3_vote_1_word_lash(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Word Lash."""
        self.create_web_input('JackboxTv-Q2-Round_3-Vote_1-Word_Lash.html')
        self.expect_return('Come up with a classic novel with this word in the title:\nFUDGE\n'
                           + 'Which one do you like more?'.upper()
                           + '\nFUDGE SOUP FOR THE SOUL\nWUTHERING FUDGES')
        self.run_test()


class ErrorTestJbgQ2GetVoteText(TestJbgQ2GetVoteText):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Error input that's expected to fail."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'Web driver can not be of type None')
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Error input that's expected to fail."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid web_driver data type of ')
        self.run_test()


class SpecialTestJbgQ2GetVoteText(TestJbgQ2GetVoteText):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        self.create_web_input('xkcd-Good_Code.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        self.create_web_input('JackboxTV-login_start.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s03_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        self.create_web_input('JackboxTv-Q2-waiting_to_start.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s04_q2_splash_page(self):
        """Quiplash 2 splash page."""
        self.create_web_input('JackboxTv-Q2-splash_page.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s05_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        self.create_web_input('JackboxTv-Q2-Round_1.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s06_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_1-Prompt_1.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s07_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_2-Prompt_1.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s08_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        self.create_web_input('JackboxTv-Q2-Round_3.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s09_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        self.create_web_input('JackboxTv-Q2-Round_3-waiting.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s10_game_over(self):
        """Quiplash 2 game over page."""
        self.create_web_input('JackboxTv-Q2-Game_Over.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s11_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Prompt_1.html')
        self.expect_standard_exception()
        self.run_test()

    def test_s12_round_3_prompt_1_v2(self):
        """Another Quiplash 2 Round 3 'Last Lash' Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Prompt_1-v2.html')
        self.expect_standard_exception()
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
