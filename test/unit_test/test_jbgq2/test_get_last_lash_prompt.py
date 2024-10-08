"""Unit test module for JbgQ2.get_last_lash_prompt().

Typical Usage:
    python -m test                                                        # Run *all* the test cases
    python -m test.unit_test                                              # Run *all* unit tests
    python -m test.unit_test.test_jbgq2                                   # Run *all* jbgq2 tests
    python -m test.unit_test.test_jbgq2.test_get_last_lash_prompt         # Run just these tests
    python -m test.unit_test.test_jbgq2.test_get_last_lash_prompt -k n01  # Run just the n01 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgq2.test_jbgq2 import TestJbgQ2
from tediousstart.tediousstart import execute_test_cases
# Local Imports


class TestJbgQ2GetPrompt(TestJbgQ2):
    """The jbg_q2.get_last_lash_prompt() unit test class.

    This class provides base functionality to run NEBS unit tests for jbg_q2.get_last_lash_prompt().
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

    def call_callable(self) -> Any:
        """Calls jbg_q2.get_last_lash_prompt().

        Overrides the parent method.  Defines the way to call jbg_q2.get_last_lash_prompt().

        Args:
            None

        Returns:
            Return value of jbg_q2.get_last_lash_prompt()

        Raises:
            Exceptions raised by jbg_q2.get_last_lash_prompt() are bubbled up and handled by
            TediousUnitTest.
        """
        return self.jbg_q2_obj.get_last_lash_prompt(*self._args, **self._kwargs)

    def create_test_input(self, filename: str, use_kwarg: bool = False) -> None:
        """Translates file-based test input into a Selenium web driver for test case input.

        Args:
            filename: The file-based test input to create the web driver with.
            use_kwarg: Optional; If True, convert all arguments into keyword arguments.

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
            self.set_test_input(web_driver=self.web_driver)
        else:
            self.set_test_input(self.web_driver)


class NormalTestJbgQ2GetPrompt(TestJbgQ2GetPrompt):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page.

        jitb.selenium.get_last_lash_prompt() has been refactored to only work for Round 3 prompts.
        No more one-size-fits-all shenanigans.  I will refactor the JbgQ2 and jbg_q2
        functionality to be more 'recipe' driven and to lean heavily on jitb.selenium.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1.html')
        self.expect_return('Come up with a new hilarious sitcom with this word in the title: '
                           'SLIME')
        self.run_test()

    def test_n02_round_3_prompt_1_v2(self):
        """Another Quiplash 2 Round 3 'Last Lash' Prompt 1 page.

        jitb.selenium.get_last_lash_prompt() has been refactored to only work for Round 3 prompts.
        No more one-size-fits-all shenanigans.  I will refactor the JbgQ2 and jbg_q2
        functionality to be more 'recipe' driven and to lean heavily on jitb.selenium.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-v2.html')
        self.expect_return('Come up with a full name for this acronym! W.A.W.')
        self.run_test()

    def test_n03_round_3_prompt_1_acro_lash(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page: specifically the Acro Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-Acro_Lash.html')
        self.expect_return('Come up with a full name for this acronym! G.O.R.')
        self.run_test()

    def test_n04_round_3_prompt_1_comic_lash(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page: specifically the Comic Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-Comic_Lash.html')
        self.expect_return('Complete the Comic!   SEND')  # Odd edge case among the Last Lashes
        self.run_test()

    def test_n05_round_3_prompt_1_word_lash(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page: specifically the Word Lash."""
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-Word_Lash.html')
        self.expect_return('Come up with a romantic comedy film with this word in the title: WIG')
        self.run_test()

    def test_n06_round_3_prompt_1_v1_clean(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page; clean_prompt == True.

        jitb.selenium.get_last_lash_prompt() has been refactored to only work for Round 3 prompts.
        No more one-size-fits-all shenanigans.  I will refactor the JbgQ2 and jbg_q2
        functionality to be more 'recipe' driven and to lean heavily on jitb.selenium.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1.html', False)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title: '
                           'SLIME')
        self.run_test()

    def test_n07_round_3_prompt_1_v2_clean(self):
        """Another Quiplash 2 Round 3 'Last Lash' Prompt 1 page; clean_prompt == True w/ kwargs.

        jitb.selenium.get_last_lash_prompt() has been refactored to only work for Round 3 prompts.
        No more one-size-fits-all shenanigans.  I will refactor the JbgQ2 and jbg_q2
        functionality to be more 'recipe' driven and to lean heavily on jitb.selenium.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Prompt_1-v2.html', True)
        self.expect_return('Come up with a full name for this acronym! W.A.W.')
        self.run_test()


class ErrorTestJbgQ2GetPrompt(TestJbgQ2GetPrompt):
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

    def test_e03_jitb_logic_flaw(self):
        """Error input that's expected to fail.

        This BUG cropped up during live functional testing.  Technically, get_prompt() worked
        perfectly.  The logic that sent this page to get_prompt(), however, was flawed.
        """
        self.create_test_input('JackboxTv-Q2-Round_1-Vote_1-get_prompt-error.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()


class SpecialTestJbgQ2GetPrompt(TestJbgQ2GetPrompt):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        self.create_test_input('xkcd-Good_Code.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-login_start.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s03_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        self.create_test_input('JackboxTv-Q2-waiting_to_start.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s04_q2_splash_page(self):
        """Quiplash 2 splash page."""
        self.create_test_input('JackboxTv-Q2-splash_page.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s05_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        self.create_test_input('JackboxTv-Q2-Round_1.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s06_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_1-Vote_1.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s07_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        self.create_test_input('JackboxTv-Q2-Round_3.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s08_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s09_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        self.create_test_input('JackboxTv-Q2-Round_3-waiting.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s10_game_over(self):
        """Quiplash 2 game over page."""
        self.create_test_input('JackboxTv-Q2-Game_Over.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s11_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page.

        jitb.selenium's get_last_lash_prompt() does not permit Round 1 or Round 2 prompt pages.
        """
        self.create_test_input('JackboxTv-Q2-Round_1-Prompt_1.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()

    def test_s12_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page.

        jitb.selenium's get_last_lash_prompt() does not permit Round 1 or Round 2 prompt pages."""
        self.create_test_input('JackboxTv-Q2-Round_2-Prompt_1.html')
        self.expect_exception(RuntimeError, 'This is not a Last Lash prompt page')
        self.run_test()
# pylint: enable = protected-access


if __name__ == '__main__':
    execute_test_cases()
