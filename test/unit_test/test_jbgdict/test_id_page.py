"""Unit test module for JbgDict.id_page().

Typical Usage:
    python -m test                                             # Run *all* the test cases
    python -m test.unit_test                                   # Run *all* the unit test cases
    python -m test.unit_test.test_jbgdict                      # Run *all* jbgdict unit tests cases
    python -m test.unit_test.test_jbgdict.test_id_page         # Run just these unit tests
    python -m test.unit_test.test_jbgdict.test_id_page -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgdict.test_jbgdict import TestJbgDict
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_page_ids import JbgPageIds


# pylint: disable = too-many-public-methods
class TestJbgDictIdPage(TestJbgDict):
    """JbgDict.id_page() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgDict.id_page().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls JbgDict.id_page().

        Overrides the parent method.  Defines the way to call JbgDict.id_page().

        Args:
            None

        Returns:
            Return value of JbgDict.id_page()

        Raises:
            Exceptions raised by JbgDict.id_page() are bubbled up and handled by TediousUnitTest
        """
        jbg_dict_obj = self.setup_jbgdict_object()
        return jbg_dict_obj.id_page(*self._args, **self._kwargs)


class NormalTestJbgDictIdPage(TestJbgDictIdPage):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-Dict-Login_start.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n02_waiting_on_other_players(self):
        """Dictionarium waiting to start."""
        self.create_test_input('JackboxTV-Dict-Login_waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n03_word_game_round_1_1_waiting(self):
        """Dictionarium Word Game Round 1 waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_1-1-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n04_word_game_round_1_2_definition_prompt(self):
        """Dictionarium Word Game Round 1 prompt."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_1-2-Definition_prompt.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n05_word_game_round_1_3_waiting(self):
        """Dictionarium Word Game Round 1 more waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_1-3-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n06_word_game_round_1_4_vote(self):
        """Dictionarium Word Game Round 1 vote."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_1-4-Vote.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n07_word_game_round_1_5_waiting_likes(self):
        """Dictionarium Word Game Round 1 waiting with likes."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_1-5-Waiting_likes.html')
        self.expect_return(JbgPageIds.DICT_WAIT_LIKE)
        self.run_test()

    def test_n08_word_game_round_1_6_waiting(self):
        """Dictionarium Word Game Round 1 even more waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_1-6-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n09_word_game_round_2_1_synonym_prompt(self):
        """Dictionarium Word Game Round 2 prompt."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_2-1-Synonym_prompt.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n10_word_game_round_2_2_waiting(self):
        """Dictionarium Word Game Round 2 waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_2-2-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n11_word_game_round_2_3_vote(self):
        """Dictionarium Word Game Round 2 vote."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_2-3-Vote.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n12_word_game_round_2_4_waiting_likes(self):
        """Dictionarium Word Game Round 2 waiting with likes."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_2-4-Waiting_likes.html')
        self.expect_return(JbgPageIds.DICT_WAIT_LIKE)
        self.run_test()

    def test_n13_word_game_round_2_5_waiting(self):
        """Dictionarium Word Game Round 2 more waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_2-5-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n14_word_game_round_3_1_sentence_prompt(self):
        """Dictionarium Word Game Round 3 prompt."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_3-1-Sentence_prompt.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n15_word_game_round_3_2_waiting(self):
        """Dictionarium Word Game Round 3 waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_3-2-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n16_word_game_round_3_3_vote(self):
        """Dictionarium Word Game Round 3 vote."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_3-3-Vote.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n17_word_game_round_3_4_waiting_likes(self):
        """Dictionarium Word Game Round 3 waiting with likes."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_3-4-Waiting_likes.html')
        self.expect_return(JbgPageIds.DICT_WAIT_LIKE)
        self.run_test()

    def test_n18_word_game_round_3_5_waiting(self):
        """Dictionarium Word Game Round 3 even more waiting."""
        self.create_test_input('JackboxTV-Dict-Word_Game-Round_3-5-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n19_slang_phrase_round_1_1_waiting(self):
        """Dictionarium Slang Phrase Round 1 waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_1-1-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n20_slang_phrase_round_1_2_definition_prompt(self):
        """Dictionarium Slang Phrase Round 1 prompt."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_1-2-Definition_prompt.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n21_slang_phrase_round_1_3_waiting(self):
        """Dictionarium Slang Phrase Round 1 more waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_1-3-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n22_slang_phrase_round_1_4_vote(self):
        """Dictionarium Slang Phrase Round 1 vote."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_1-4-Vote.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n23_slang_phrase_round_1_5_waiting_likes(self):
        """Dictionarium Slang Phrase Round 1 waiting with likes."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_1-5-Waiting_likes.html')
        self.expect_return(JbgPageIds.DICT_WAIT_LIKE)
        self.run_test()

    def test_n24_slang_phrase_round_1_6_waiting(self):
        """Dictionarium Slang Phrase Round 1 even more waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_1-6-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n25_slang_phrase_round_2_1_synonym_prompt(self):
        """Dictionarium Slang Phrase Round 2 prompt."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_2-1-Synonym_prompt.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n26_slang_phrase_round_2_2_waiting(self):
        """Dictionarium Slang Phrase Round 2 waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_2-2-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n27_slang_phrase_round_2_3_waiting(self):
        """Dictionarium Slang Phrase Round 2 more waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_2-3-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n28_slang_phrase_round_2_4_vote(self):
        """Dictionarium Slang Phrase Round 2 vote."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_2-4-Vote.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n29_slang_phrase_round_2_5_waiting_likes(self):
        """Dictionarium Slang Phrase Round 2 waiting with likes."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_2-5-Waiting_likes.html')
        self.expect_return(JbgPageIds.DICT_WAIT_LIKE)
        self.run_test()

    def test_n30_slang_phrase_round_2_6_waiting(self):
        """Dictionarium Slang Phrase Round 2 so much waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_2-6-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n31_slang_phrase_round_3_1_sentence_prompt(self):
        """Dictionarium Slang Phrase Round 3 prompt."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_3-1-Sentence_prompt.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n32_slang_phrase_round_3_2_waiting(self):
        """Dictionarium Slang Phrase Round 3 waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_3-2-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n33_slang_phrase_round_3_3_waiting(self):
        """Dictionarium Slang Phrase Round 3 more waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_3-3-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n34_slang_phrase_round_3_4_vote(self):
        """Dictionarium Slang Phrase Round 3 vote."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_3-4-Vote.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()

    def test_n35_slang_phrase_round_3_5_waiting_likes(self):
        """Dictionarium Slang Phrase Round 3 waiting with likes."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_3-5-Waiting_likes.html')
        self.expect_return(JbgPageIds.DICT_WAIT_LIKE)
        self.run_test()

    def test_n36_slang_phrase_round_3_6_waiting(self):
        """Dictionarium Slang Phrase Round 3 even more waiting."""
        self.create_test_input('JackboxTV-Dict-Slang_Phrase-Round_3-6-Waiting.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n36_game_done_waiting(self):
        """Dictionarium game done; waiting page."""
        self.create_test_input('JackboxTV-Dict-End_of_game.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()


class ErrorTestJbgDictIdPage(TestJbgDictIdPage):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Bad Data Type: None."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Bad Data Type: Path object."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


class SpecialTestJbgDictIdPage(TestJbgDictIdPage):
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

    def test_s03_game_over_disconnected(self):
        """Dictionarium game over page; disconnected."""
        self.create_test_input('JackboxTV-Dict-Disconnected.html')
        self.expect_exception(RuntimeError, 'The room was disconnected')
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
