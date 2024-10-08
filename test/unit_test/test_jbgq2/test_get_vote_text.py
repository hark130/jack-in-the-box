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
from test.unit_test.test_jbgq2.test_jbgq2 import TestJbgQ2
from tediousstart.tediousstart import execute_test_cases
# Local Imports


# pylint: disable = protected-access
class TestJbgQ2GetVoteText(TestJbgQ2):
    """The jbg_q2.get_vote_text() unit test class.

    This class provides base functionality to run NEBS unit tests for jbg_q2.get_vote_text().
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
        self.jbg_q2_obj = self.setup_jbgq2_object()  # Test case needs access to the object

    def create_test_input(self, filename: str, use_kwarg: bool, *opt_args) -> None:
        """Translates file-based test input into a Selenium web driver for test case input.

        Args:
            filename: The file-based test input to create the web driver with.
            use_kwarg: If True, convert all arguments into keyword arguments.
            opt_args: A tuple of optional arguments:
                (vote_clues), or (vote_clues, clean_string)

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
            if not opt_args:
                self.set_test_input(web_driver=self.web_driver)
            elif len(opt_args) == 1:
                self.set_test_input(web_driver=self.web_driver, vote_clues=opt_args[0])
            elif len(opt_args) == 2:
                self.set_test_input(web_driver=self.web_driver, vote_clues=opt_args[0],
                                    clean_string=opt_args[1])
            else:
                self.fail_test_case(f'Invalid opt_args length: {opt_args}')
        else:
            if not opt_args:
                self.set_test_input(self.web_driver)
            elif len(opt_args) == 1:
                self.set_test_input(self.web_driver, opt_args[0])
            elif len(opt_args) == 2:
                self.set_test_input(self.web_driver, opt_args[0], opt_args[1])
            else:
                self.fail_test_case(f'Invalid opt_args length: {opt_args}')

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
        return self.jbg_q2_obj.get_vote_text(*self._args, **self._kwargs)


class NormalTestJbgQ2GetVoteText(TestJbgQ2GetVoteText):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_vote_1_dirty_prompt(self):
        """Quiplash 2 Round 1 Vote 1 page; clean_prompt == False."""
        self.create_test_input('JackboxTv-Q2-Round_1-Vote_1.html', False,
                               self.jbg_q2_obj._vote_clues, False)
        self.expect_return('An inappropriate time to wear a tuxedo\n' +
                           'Which one do you like more?\n'.upper() +
                           'SCRAPPLE\nBUTTE, MONTANA')
        self.run_test()

    def test_n02_round_3_vote_1_dirty_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1.html', False,
                               self.jbg_q2_obj._vote_clues, False)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title:\n'
                           'SLIME\n' + 'Which one do you like more?'.upper() + '\nSLIMER\nSLIMEY')
        self.run_test()

    def test_n03_round_3_vote_1_v2_dirty_prompt(self):
        """Quiplash 2 Round 3 Vote 1 v2 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v2.html', False,
                               self.jbg_q2_obj._vote_clues, False)
        self.expect_return('Come up with a full name for this acronym!\nW.A.W.\n'
                           + 'Which one do you like more?'.upper() + '\nWIN A WAR\n5')
        self.run_test()

    def test_n04_round_3_vote_1_v3_dirty_prompt(self):
        """Quiplash 2 Round 3 Vote 1 v3 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v3.html', False,
                               self.jbg_q2_obj._vote_clues, False)
        self.expect_return('Come up with a full name for this acronym!\nG.O.R.\n'
                           + 'Which one do you like more?'.upper() + '\nGET ON READ\n'
                           + 'GUMMY ORGASM RECIPE')
        self.run_test()

    def test_n05_round_3_vote_1_acro_lash_dirty_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Acro Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v3.html', False,
                               self.jbg_q2_obj._vote_clues, False)
        self.expect_return('Come up with a full name for this acronym!\nG.O.R.\n'
                           + 'Which one do you like more?'.upper() + '\nGET ON READ\n'
                           + 'GUMMY ORGASM RECIPE')
        self.run_test()

    @skip('This test case needs file-based test input')
    def test_n06_round_3_vote_1_comic_lash_dirty_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Comic Lash."""
        self.create_test_input('', False)
        self.expect_return('')
        self.run_test()

    def test_n07_round_3_vote_1_word_lash_dirty_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Word Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-Word_Lash.html', False,
                               self.jbg_q2_obj._vote_clues, False)
        self.expect_return('Come up with a classic novel with this word in the title:\nFUDGE\n'
                           + 'Which one do you like more?'.upper()
                           + '\nFUDGE SOUP FOR THE SOUL\nWUTHERING FUDGES')
        self.run_test()

    def test_n08_round_1_vote_1_clean_prompt(self):
        """Quiplash 2 Round 1 Vote 1 page; clean_prompt == False."""
        self.create_test_input('JackboxTv-Q2-Round_1-Vote_1.html', False,
                               self.jbg_q2_obj._vote_clues, True)
        self.expect_return('An inappropriate time to wear a tuxedo ' +
                           'Which one do you like more? '.upper() +
                           'SCRAPPLE BUTTE, MONTANA')
        self.run_test()

    def test_n09_round_3_vote_1_clean_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1.html', False,
                               self.jbg_q2_obj._vote_clues, True)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title: '
                           'SLIME ' + 'Which one do you like more?'.upper() + ' SLIMER SLIMEY')
        self.run_test()

    def test_n10_round_3_vote_1_v2_clean_prompt(self):
        """Quiplash 2 Round 3 Vote 1 v2 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v2.html', False,
                               self.jbg_q2_obj._vote_clues, True)
        self.expect_return('Come up with a full name for this acronym! W.A.W. '
                           + 'Which one do you like more?'.upper() + ' WIN A WAR 5')
        self.run_test()

    def test_n11_round_3_vote_1_v3_clean_prompt(self):
        """Quiplash 2 Round 3 Vote 1 v3 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v3.html', False,
                               self.jbg_q2_obj._vote_clues, True)
        self.expect_return('Come up with a full name for this acronym! G.O.R. '
                           + 'Which one do you like more?'.upper() + ' GET ON READ '
                           + 'GUMMY ORGASM RECIPE')
        self.run_test()

    def test_n12_round_3_vote_1_acro_lash_clean_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Acro Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v3.html', False,
                               self.jbg_q2_obj._vote_clues, True)
        self.expect_return('Come up with a full name for this acronym! G.O.R. '
                           + 'Which one do you like more?'.upper() + ' GET ON READ '
                           + 'GUMMY ORGASM RECIPE')
        self.run_test()

    @skip('This test case needs file-based test input')
    def test_n13_round_3_vote_1_comic_lash_clean_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Comic Lash."""
        self.create_test_input('', False, self.jbg_q2_obj._vote_clues, True)
        self.expect_return('')
        self.run_test()

    def test_n14_round_3_vote_1_word_lash_clean_prompt(self):
        """Quiplash 2 Round 3 Vote 1 page: specifically the Word Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-Word_Lash.html', False,
                               self.jbg_q2_obj._vote_clues, True)
        self.expect_return('Come up with a classic novel with this word in the title: FUDGE '
                           + 'Which one do you like more?'.upper()
                           + ' FUDGE SOUP FOR THE SOUL WUTHERING FUDGES')
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
        self.create_test_input('xkcd-Good_Code.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-login_start.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s03_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        self.create_test_input('JackboxTv-Q2-waiting_to_start.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s04_q2_splash_page(self):
        """Quiplash 2 splash page."""
        self.create_test_input('JackboxTv-Q2-splash_page.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s05_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        self.create_test_input('JackboxTv-Q2-Round_1.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s06_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_1-Prompt_1.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s07_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_2-Prompt_1.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s08_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        self.create_test_input('JackboxTv-Q2-Round_3.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s09_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        self.create_test_input('JackboxTv-Q2-Round_3-waiting.html', False,
                               self.jbg_q2_obj._vote_clues)
        self.expect_standard_exception()
        self.run_test()

    def test_s10_game_over(self):
        """Quiplash 2 game over page."""
        self.create_test_input('JackboxTv-Q2-Game_Over.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s11_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1.html', False)
        self.expect_standard_exception()
        self.run_test()

    def test_s12_round_3_prompt_1_v2(self):
        """Another Quiplash 2 Round 3 'Last Lash' Prompt 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-v2.html', False)
        self.expect_standard_exception()
        self.run_test()

    @skip('Fix this failing test case in JITB-31')
    def test_s13_round_3_vote_2_silver_medal(self):
        """Quiplash 2 Round 3 Vote 2 page.

        Quiplash 2's Last Lash is unique in that enough players allow a voter to vote for
        gold, silver, and bronze choices.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_2-Silver_Medal.html', False)
        self.expect_return('Come up with a new TV show with this word in the title:\n' +
                           'CORN\nNOW AWARD YOUR SILVER MEDAL!\nWATCHING 2 MUCH CORN\n' +
                           'CORN HUB\nCORNY TONY\nTHE OTHER QUESTIONS PROLLY GONNA SAY CORNHUB\n' +
                           'AVATAR THE LAST CORNBENDER')
        self.run_test()

    @skip('Fix this failing test case in JITB-31')
    def test_s14_round_3_vote_3_bronze_medal(self):
        """Quiplash 2 Round 3 Vote 3 page.

        Quiplash 2's Last Lash is unique in that enough players allow a voter to vote for
        gold, silver, and bronze choices.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_3-Bronze_Medal.html', False)
        self.expect_return('Come up with a new TV show with this word in the title:\n' +
                           'CORN\nAND HAND OUT A BRONZE MEDAL TO YOUR THIRD FAVORITE.\n' +
                           'WATCHING 2 MUCH CORN\nCORN HUB\nCORNY TONY\n' +
                           'THE OTHER QUESTIONS PROLLY GONNA SAY CORNHUB\n' +
                           'AVATAR THE LAST CORNBENDER')
        self.run_test()
# pylint: enable = protected-access


if __name__ == '__main__':
    execute_test_cases()
