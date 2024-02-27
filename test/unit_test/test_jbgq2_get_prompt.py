"""Unit test module for JbgQ2.id_page().

Typical Usage:
    python -m test                                         # Run *all* the test cases
    python -m test.unit_test                               # Run *all* the unit test cases
    python -m test.unit_test.test_jbgq2_get_prompt         # Run just these unit tests
    python -m test.unit_test.test_jbgq2_get_prompt -k n01  # Run just this normal 1 unit test
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
from jitb.jbgames.jbg_q2 import JbgQ2, get_prompt
from jitb.jitb_openai import JitbAi
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jbgq2 import TestJbgQ2
from test.unit_test.test_jackbox_games import TestJackboxGames


class TestJbgQ2GetPrompt(TestJackboxGames):
    """The jbg_q2.get_prompt() unit test class.

    This class provides base functionality to run NEBS unit tests for jbg_q2.get_prompt().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def create_web_input(self, filename: Path, use_kwarg: bool = False) -> None:
        """Translate a path object into test input.

        Args:
            filename: Path object to convert to a web driver and use as file-based test input.
            use_kwarg: Optional; Will call the function using keyword arguments.
        """
        # LOCAL VARIABLES
        self.create_web_driver(filename=filename)  # Unit test input
        if use_kwarg:
            self.set_test_input(web_driver=self.web_driver)
        else:
            self.set_test_input(self.web_driver)

    def call_callable(self) -> Any:
        """Calls jbg_q2.get_prompt().

        Overrides the parent method.  Defines the way to call jbg_q2.get_prompt().

        Args:
            None

        Returns:
            Return value of jbg_q2.get_prompt()

        Raises:
            Exceptions raised by jbg_q2.get_prompt() are bubbled up and handled by TediousUnitTest
        """
        return get_prompt(*self._args, **self._kwargs)


class NormalTestJbgQ2GetPrompt(TestJbgQ2GetPrompt):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_1-Prompt_1.html')
        self.expect_return(['You know you’re staying at a dirty hotel when they offer '
                           'a free continental ________', '  SEND SAFETY QUIP', '(HALF POINTS)'])
        self.run_test()

    def test_n02_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_2-Prompt_1.html')
        self.expect_return(['A rejected title in the Magic School Bus series: '
                            'The Magic School Bus Goes to ________', '  SEND SAFETY QUIP',
                            '(HALF POINTS)'])
        self.run_test()

    def test_n03_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 'Last Lash' Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Prompt_1.html')
        self.expect_return(['Come up with a new hilarious sitcom with this word in the title:',
                            'SLIME', '  SEND'])
        self.run_test()

    def test_n04_round_3_prompt_1_v2(self):
        """Another Quiplash 2 Round 3 'Last Lash' Prompt 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Prompt_1-v2.html')
        self.expect_return(['Come up with a full name for this acronym!', 'W.A.W.', '  SEND'])
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


class SpecialTestJbgQ2GetPrompt(TestJbgQ2GetPrompt):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        self.create_web_input('xkcd-Good_Code.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        self.create_web_input('JackboxTV-login_start.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s03_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        self.create_web_input('JackboxTv-Q2-waiting_to_start.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s04_q2_splash_page(self):
        """Quiplash 2 splash page."""
        self.create_web_input('JackboxTv-Q2-splash_page.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s05_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        self.create_web_input('JackboxTv-Q2-Round_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s06_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_1-Vote_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s07_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        self.create_web_input('JackboxTv-Q2-Round_3.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s08_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        self.create_web_input('JackboxTv-Q2-Round_3-Vote_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s09_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        self.create_web_input('JackboxTv-Q2-Round_3-waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s10_game_over(self):
        """Quiplash 2 game over page."""
        self.create_web_input('JackboxTv-Q2-Game_Over.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
