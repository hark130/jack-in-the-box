"""Unit test module for JbgBr.get_guess_prompt().

Typical Usage:
    python -m test                                                    # Run *all* the test cases
    python -m test.unit_test                                          # Run *all* the unit tests
    python -m test.unit_test.test_jbgbr                               # Run *all* jbgbr unit tests
    python -m test.unit_test.test_jbgbr.test_get_guess_prompt         # Run just these unit tests
    python -m test.unit_test.test_jbgbr.test_get_guess_prompt -k n01  # Run just this normal 1 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
import selenium
# Third Party Imports
from test.unit_test.test_jbgbr.test_jbgbr import TestJbgBr
from tediousstart.tediousstart import execute_test_cases
# Local Imports


# pylint: disable = too-many-public-methods
class TestJbgBrGetGuessPrompt(TestJbgBr):
    """The jgb_br.get_guess_prompt() unit test class.

    This class provides base functionality to run NEBS unit tests for jgb_br.get_guess_prompt().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def create_br_input(self, filename: str, use_kwarg: bool = False) -> None:
        """Translates file-based test input into a Selenium web driver for test case input.

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

    def expect_br_page_exception(self) -> None:
        """Single point of truth (SPOT) for 'wrong page' exception messages."""
        self.expect_exception(RuntimeError, "This is not a Blather 'Round guess page")

    def expect_get_guess_prompt_type_exception(self, received: type) -> None:
        """Single point of truth (SPOT) for 'wrong page' exception messages."""
        # LOCAL VARIABLES
        var_name = 'web_driver'                                   # The only one available
        expected = selenium.webdriver.chrome.webdriver.WebDriver  # The data type for web_driver

        # EXPECT IT
        self.expect_exception(TypeError, f'{var_name} expected type {expected}, '
                              f'instead received type {received}')

    def expect_page_exception(self) -> None:
        """Single point of truth (SPOT) for 'wrong page' exception messages."""
        self.expect_exception(RuntimeError, "This is not a prompt page")

    def call_callable(self) -> Any:
        """Calls jgb_br.get_guess_prompt().

        Overrides the parent method.  Defines the way to call jgb_br.get_guess_prompt().

        Args:
            None

        Returns:
            Return value of jgb_br.get_guess_prompt()

        Raises:
            Any exceptions raised bubble up and are handled by TediousUnitTest
        """
        jbg_br_obj = self.setup_jbgbr_object()
        return jbg_br_obj.get_guess_prompt(*self._args, **self._kwargs)


class NormalTestJbgBrGetGuessPrompt(TestJbgBrGetGuessPrompt):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_guess_1a(self):
        """Blather 'Round Round 1 Guess 1a."""
        self.create_br_input('JackboxTV-BR-5a-Guess.html')
        self.expect_return("Magugol is presenting a: story. It's a story about a dull good guy. "
                           "What story is magugol describing?")
        self.run_test()

    def test_n02_round_1_guess_1b(self):
        """Blather 'Round Round 1 Guess 1b."""
        self.create_br_input('JackboxTV-BR-5b-Guess.html')
        self.expect_return("Magugol is presenting a: story. It's a story about a dull good guy. "
                           "And a fantastic experience. "
                           "What story is magugol describing?")
        self.run_test()

    def test_n03_round_1_guess_1c(self):
        """Blather 'Round Round 1 Guess 1c."""
        self.create_br_input('JackboxTV-BR-5c-Guess.html')
        self.expect_return("Magugol is presenting a: story. It's a story about a dull good guy. "
                           "And a fantastic experience. "
                           "Whoa! A perky paddle. "
                           "What story is magugol describing?")
        self.run_test()

    def test_n04_round_1_guess_1d(self):
        """Blather 'Round Round 1 Guess 1d."""
        self.create_br_input('JackboxTV-BR-5d-Guess.html')
        self.expect_return("Magugol is presenting a: story. It's a story about a dull good guy. "
                           "And a fantastic experience. "
                           "Whoa! A perky paddle. "
                           "The hero adores the human. "
                           "What story is magugol describing?")
        self.run_test()

    def test_n05_round_1_guess_2a(self):
        """Blather 'Round Round 1 Guess 2a."""
        self.create_br_input('JackboxTV-BR-6a-Guess_Place.html')
        self.expect_return("Mumu is presenting a: place. It's a vibrant place. "
                           "What place is mumu describing?")
        self.run_test()

    def test_n06_round_1_guess_2b(self):
        """Blather 'Round Round 1 Guess 2b."""
        self.create_br_input('JackboxTV-BR-6b-Guess_Place.html')
        self.expect_return("Mumu is presenting a: place. It's a vibrant place. "
                           "It's where you have the brand. "
                           "What place is mumu describing?")
        self.run_test()

    def test_n07_round_1_guess_2c(self):
        """Blather 'Round Round 1 Guess 2c."""
        self.create_br_input('JackboxTV-BR-6c-Guess_Place-guessed_wrong.html')
        self.expect_return("Mumu is presenting a: place. It's a vibrant place. "
                           "It's where you have the brand. "
                           "What place is mumu describing?")
        self.run_test()

    def test_n08_round_1_guess_2d(self):
        """Blather 'Round Round 1 Guess 2d."""
        self.create_br_input('JackboxTV-BR-6d-Guess_Place.html')
        self.expect_return("Mumu is presenting a: place. It's a vibrant place. "
                           "It's where you have the brand. "
                           "So much rubber! "
                           "What place is mumu describing?")
        self.run_test()

    def test_n09_round_1_guess_2e(self):
        """Blather 'Round Round 1 Guess 2e."""
        self.create_br_input('JackboxTV-BR-6e-Guess_Place-guessed_wrong.html')
        self.expect_return("Mumu is presenting a: place. It's a vibrant place. "
                           "It's where you have the brand. "
                           "So much rubber! "
                           "What place is mumu describing?")
        self.run_test()

    def test_n10_round_2_guess_4b(self):
        """Blather 'Round Round 2 Guess 4b."""
        self.create_br_input('JackboxTV-BR-Round_2-4b-Guess_person.html')
        self.expect_return("Mumu is presenting a: person. They're a fictional  entity. "
                           "They are renowned for the patience. "
                           "What person is mumu describing?")
        self.run_test()


class ErrorTestJbgBrGetGuessPrompt(TestJbgBrGetGuessPrompt):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Bad Data Type: None."""
        self.set_test_input(None)
        self.expect_get_guess_prompt_type_exception(received=type(None))
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Bad Data Type: Path object."""
        self.set_test_input(['.', 'test', 'test_input', 'JackboxTV-login_start.html'])
        self.expect_get_guess_prompt_type_exception(received=list)
        self.run_test()


class SpecialTestJbgBrGetGuessPrompt(TestJbgBrGetGuessPrompt):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        self.create_br_input('xkcd-Good_Code.html')
        self.expect_page_exception()
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        self.create_br_input('JackboxTV-JB-Login_start.html')
        self.expect_page_exception()
        self.run_test()

    def test_s03_joke_boat_prompt_is_not_a_blather_round_prompt(self):
        """Joke Boat Round 1 Joke 1c complete punchline page."""
        self.create_br_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html')
        self.expect_page_exception()
        self.run_test()

    def test_s04_login_page(self):
        """Jackbox.tv Login page."""
        self.create_br_input('JackboxTV-BR-1a-Login_Page-pre_login.html')
        self.expect_page_exception()
        self.run_test()

    def test_s05_waiting_on_other_players(self):
        """Blather 'Round waiting to start."""
        self.create_br_input('JackboxTV-BR-1b-Login_Page-waiting.html')
        self.expect_page_exception()
        self.run_test()

    def test_s06_round_1_waiting(self):
        """Blather 'Round Chose secret prompt; waiting."""
        self.create_br_input('JackboxTV-BR-2b-Choose_Prompt-waiting.html')
        self.expect_page_exception()
        self.run_test()

    def test_s07_round_1_guess_2f(self):
        """Blather 'Round Round 1 Guess 2f."""
        self.create_br_input('JackboxTV-BR-6f-Guess_Place-guessed_right-waiting.html')
        self.expect_page_exception()
        self.run_test()

    def test_s08_round_1_make_a_sentence(self):
        """Blather 'Round Round 1 make a sentence."""
        self.create_br_input('JackboxTV-BR-3-Make_Sentence.html')
        self.expect_page_exception()
        self.run_test()

    def test_s09_round_1_describe(self):
        """Blather 'Round Round 1 describe."""
        self.create_br_input('JackboxTV-BR-4a-Describe.html')
        self.expect_page_exception()
        self.run_test()

    def test_s10_round_2_make_a_sentence(self):
        """Blather 'Round Round 2 make a sentence."""
        self.create_br_input('JackboxTV-BR-Round_2-2-Make_Sentence.html')
        self.expect_page_exception()
        self.run_test()

    def test_s11_round_2_describe(self):
        """Blather 'Round Round 2 describe."""
        self.create_br_input('JackboxTV-BR-Round_2-3b-Describe.html')
        self.expect_page_exception()
        self.run_test()

    def test_s12_game_done_waiting(self):
        """Blather 'Round game done; waiting page."""
        self.create_br_input('JackboxTV-Dict-End_of_game.html')
        self.expect_page_exception()
        self.run_test()

    def test_s13_game_over_disconnected(self):
        """Blather 'Round game over page; disconnected."""
        self.create_test_input('JackboxTV-Dict-Disconnected.html')
        self.expect_page_exception()
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
