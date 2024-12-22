"""Unit test module for JbgDict.get_prompt().

Typical Usage:
    python -m test                                                # Run *all* the test cases
    python -m test.unit_test                                      # Run *all* the unit test cases
    python -m test.unit_test.test_jbgdict                         # Run *all* jbgdict unit tests
    python -m test.unit_test.test_jbgdict.test_get_prompt         # Run just these unit tests
    python -m test.unit_test.test_jbgdict.test_get_prompt -k n01  # Run just this normal 1 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgdict.test_jbgdict import TestJbgDict
from tediousstart.tediousstart import execute_test_cases
# Local Imports


# pylint: disable = too-many-public-methods
class TestJbgDictGetPrompt(TestJbgDict):
    """The jgb_dict.get_prompt() unit test class.

    This class provides base functionality to run NEBS unit tests for jgb_dict.get_prompt().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def create_wd_input(self, filename: str, use_kwarg: bool = False) -> None:
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

    def call_callable(self) -> Any:
        """Calls jgb_dict.get_prompt().

        Overrides the parent method.  Defines the way to call jgb_dict.get_prompt().

        Args:
            None

        Returns:
            Return value of jgb_dict.get_prompt()

        Raises:
            Exceptions raised by jgb_dict.get_prompt() are bubbled up and handled by TediousUnitTest
        """
        jbg_dict_obj = self.setup_jbgdict_object()
        return jbg_dict_obj.get_prompt(*self._args, **self._kwargs)


class NormalTestJbgDictGetPrompt(TestJbgDictGetPrompt):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_word_game_round_1_definition_prompt(self):
        """Dictionarium Word Game Round 1 defintion prompt."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_1-2-Definition_prompt.html')
        self.expect_return('write a definition for purfoost')
        self.run_test()

    def test_n02_word_game_round_2_synonym_prompt(self):
        """Dictionarium Word Game Round 2 synonym prompt."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_2-1-Synonym_prompt.html')
        self.expect_return('write a synonym for purfoost: silly')
        self.run_test()

    def test_n03_word_game_round_3_sentence_prompt(self):
        """Dictionarium Word Game Round 3 sentence prompt."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_3-1-Sentence_prompt.html')
        self.expect_return('write a sentence using Funny')
        self.run_test()

    def test_n04_slang_phrase_round_1_definition_prompt(self):
        """Dictionarium Slang Phrase Round 1 defintion prompt."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_1-2-Definition_prompt.html')
        self.expect_return('write a definition for "hors d\'eserves"')
        self.run_test()

    def test_n05_slang_phrase_round_2_synonym_prompt(self):
        """Dictionarium Slang Phrase Round 2 synonym prompt."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_2-1-Synonym_prompt.html')
        self.expect_return('write a synonym for "hors d\'eserves": Whores Deserts')
        self.run_test()

    def test_n06_slang_phrase_round_3_sentence_prompt(self):
        """Dictionarium Slang Phrase Round 3 sentence prompt."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_3-1-Sentence_prompt.html')
        self.expect_return('write a sentence using Slut Treats')
        self.run_test()


class ErrorTestJbgDictGetPrompt(TestJbgDictGetPrompt):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Bad Data Type: None."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Bad Data Type: Path object."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'expected type')
        self.run_test()


class SpecialTestJbgDictGetPrompt(TestJbgDictGetPrompt):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        self.create_wd_input('xkcd-Good_Code.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        self.create_wd_input('JackboxTV-JB-Login_start.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s03_joke_boat_prompt_is_not_a_dictionarium_prompt(self):
        """Joke Boat Round 1 Joke 1c complete punchline page."""
        self.create_wd_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s04_login_page(self):
        """Jackbox.tv Login page."""
        self.create_wd_input('JackboxTV-Dict-Login_start.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s05_waiting_on_other_players(self):
        """Dictionarium waiting to start."""
        self.create_wd_input('JackboxTV-Dict-Login_waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s06_word_game_round_1_1_waiting(self):
        """Dictionarium Word Game Round 1 waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_1-1-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s07_word_game_round_1_3_waiting(self):
        """Dictionarium Word Game Round 1 more waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_1-3-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s08_word_game_round_1_4_vote(self):
        """Dictionarium Word Game Round 1 vote."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_1-4-Vote.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s09_word_game_round_1_5_waiting_likes(self):
        """Dictionarium Word Game Round 1 waiting with likes."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_1-5-Waiting_likes.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s10_word_game_round_1_6_waiting(self):
        """Dictionarium Word Game Round 1 even more waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_1-6-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s11_word_game_round_2_2_waiting(self):
        """Dictionarium Word Game Round 2 waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_2-2-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s12_word_game_round_2_3_vote(self):
        """Dictionarium Word Game Round 2 vote."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_2-3-Vote.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s13_word_game_round_2_4_waiting_likes(self):
        """Dictionarium Word Game Round 2 waiting with likes."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_2-4-Waiting_likes.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s14_word_game_round_2_5_waiting(self):
        """Dictionarium Word Game Round 2 more waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_2-5-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s15_word_game_round_3_2_waiting(self):
        """Dictionarium Word Game Round 3 waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_3-2-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s16_word_game_round_3_3_vote(self):
        """Dictionarium Word Game Round 3 vote."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_3-3-Vote.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s17_word_game_round_3_4_waiting_likes(self):
        """Dictionarium Word Game Round 3 waiting with likes."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_3-4-Waiting_likes.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s18_word_game_round_3_5_waiting(self):
        """Dictionarium Word Game Round 3 even more waiting."""
        self.create_wd_input('JackboxTV-Dict-Word_Game-Round_3-5-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s19_slang_phrase_round_1_1_waiting(self):
        """Dictionarium Slang Phrase Round 1 waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_1-1-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s20_slang_phrase_round_1_3_waiting(self):
        """Dictionarium Slang Phrase Round 1 more waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_1-3-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s21_slang_phrase_round_1_4_vote(self):
        """Dictionarium Slang Phrase Round 1 vote."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_1-4-Vote.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s22_slang_phrase_round_1_5_waiting_likes(self):
        """Dictionarium Slang Phrase Round 1 waiting with likes."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_1-5-Waiting_likes.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s23_slang_phrase_round_1_6_waiting(self):
        """Dictionarium Slang Phrase Round 1 even more waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_1-6-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s24_slang_phrase_round_2_2_waiting(self):
        """Dictionarium Slang Phrase Round 2 waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_2-2-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s25_slang_phrase_round_2_3_waiting(self):
        """Dictionarium Slang Phrase Round 2 more waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_2-3-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s26_slang_phrase_round_2_4_vote(self):
        """Dictionarium Slang Phrase Round 2 vote."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_2-4-Vote.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s27_slang_phrase_round_2_5_waiting_likes(self):
        """Dictionarium Slang Phrase Round 2 waiting with likes."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_2-5-Waiting_likes.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s28_slang_phrase_round_2_6_waiting(self):
        """Dictionarium Slang Phrase Round 2 so much waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_2-6-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s29_slang_phrase_round_3_2_waiting(self):
        """Dictionarium Slang Phrase Round 3 waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_3-2-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s30_slang_phrase_round_3_3_waiting(self):
        """Dictionarium Slang Phrase Round 3 more waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_3-3-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s31_slang_phrase_round_3_4_vote(self):
        """Dictionarium Slang Phrase Round 3 vote."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_3-4-Vote.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s32_slang_phrase_round_3_5_waiting_likes(self):
        """Dictionarium Slang Phrase Round 3 waiting with likes."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_3-5-Waiting_likes.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s33_slang_phrase_round_3_6_waiting(self):
        """Dictionarium Slang Phrase Round 3 even more waiting."""
        self.create_wd_input('JackboxTV-Dict-Slang_Phrase-Round_3-6-Waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s34_game_done_waiting(self):
        """Dictionarium game done; waiting page."""
        self.create_wd_input('JackboxTV-Dict-End_of_game.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s35_game_over_disconnected(self):
        """Dictionarium game over page; disconnected."""
        self.create_test_input('JackboxTV-Dict-Disconnected.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
