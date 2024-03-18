"""Unit test module for JbgJb.get_prompt().

Typical Usage:
    python -m test                                              # Run *all* the test cases
    python -m test.unit_test                                    # Run *all* the unit test cases
    python -m test.unit_test.test_jbgjb                         # Run *all* jbgjb unit tests cases
    python -m test.unit_test.test_jbgjb.test_get_prompt         # Run just these unit tests
    python -m test.unit_test.test_jbgjb.test_get_prompt -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jbgames.jbg_jb import get_prompt


# pylint: disable = too-many-public-methods
class TestJbgJbGetPrompt(TestJackboxGames):
    """The jbg_jb.get_prompt() unit test class.

    This class provides base functionality to run NEBS unit tests for jbg_jb.get_prompt().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def create_gp_input(self, filename: str, check_needles: bool = True,
                        use_kwarg: bool = False) -> None:
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
            self.set_test_input(web_driver=self.web_driver, check_needles=check_needles)
        else:
            self.set_test_input(self.web_driver, check_needles)

    def call_callable(self) -> Any:
        """Calls jbg_jb.get_prompt().

        Overrides the parent method.  Defines the way to call jbg_jb.get_prompt().

        Args:
            None

        Returns:
            Return value of jbg_jb.get_prompt()

        Raises:
            Exceptions raised by jbg_jb.get_prompt() are bubbled up and handled by TediousUnitTest
        """
        return get_prompt(*self._args, **self._kwargs)


class NormalTestJbgJbGetPrompt(TestJbgJbGetPrompt):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_joke_1c_complete_punchline(self):
        """Joke Boat Round 1 Joke 1c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html')
        self.expect_return('Joke 1 (of 2)\nWrite your punchline:\nmy nickname is flip phone\n'
                           'because _______')
        self.run_test()

    def test_n02_round_1_joke_2c_complete_punchline(self):
        """Joke Boat Round 1 Joke 2c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-C_Complete_your_punchline.html')
        self.expect_return('Joke 2 (of 2)\nWrite your punchline:\ngod created sporting events by\n'
                           '_______')
        self.run_test()

    def test_n03_round_2_joke_1c_complete_punchline(self):
        """Joke Boat Round 2 Joke 1c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-C_Complete_your_punchline.html')
        self.expect_return('Joke 1 (of 2)\nWrite your punchline:\nhave you ever tried hoe-ing?\n'
                           'that’s when you _______')
        self.run_test()

    def test_n04_round_2_joke_2c_complete_punchline(self):
        """Joke Boat Round 2 Joke 2c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-C_Complete_your_punchline.html')
        self.expect_return('Joke 2 (of 2)\nWrite your punchline:\ni have more fears than\n'
                           '_______')
        self.run_test()

    def test_n05_round_3b_rewrite_punchline(self):
        """Joke Boat Round 3b rewrite punchline."""
        self.create_gp_input('JackboxTV-JB-Round_3-B_Rewrite_punchline.html')
        self.expect_return('Write the punchline to this joke:\nyou ever notice how zombies are '
                           'just a fancy version of\n_______?')
        self.run_test()

    def test_n06_round_1_joke_1c_complete_punchline_check_needles(self):
        """Joke Boat Round 1 Joke 1c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html',
                             check_needles=True)
        self.expect_return('Joke 1 (of 2)\nWrite your punchline:\nmy nickname is flip phone\n'
                           'because _______')
        self.run_test()

    def test_n07_round_1_joke_2c_complete_punchline_check_needles(self):
        """Joke Boat Round 1 Joke 2c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-C_Complete_your_punchline.html',
                             check_needles=True)
        self.expect_return('Joke 2 (of 2)\nWrite your punchline:\ngod created sporting events by\n'
                           '_______')
        self.run_test()

    def test_n08_round_2_joke_1c_complete_punchline_check_needles(self):
        """Joke Boat Round 2 Joke 1c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-C_Complete_your_punchline.html',
                             check_needles=True)
        self.expect_return('Joke 1 (of 2)\nWrite your punchline:\nhave you ever tried hoe-ing?\n'
                           'that’s when you _______')
        self.run_test()

    def test_n09_round_2_joke_2c_complete_punchline_check_needles(self):
        """Joke Boat Round 2 Joke 2c complete punchline page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-C_Complete_your_punchline.html',
                             check_needles=True)
        self.expect_return('Joke 2 (of 2)\nWrite your punchline:\ni have more fears than\n'
                           '_______')
        self.run_test()

    def test_n10_round_3b_rewrite_punchline(self):
        """Joke Boat Round 3b rewrite punchline."""
        self.create_gp_input('JackboxTV-JB-Round_3-B_Rewrite_punchline.html',
                             check_needles=True)
        self.expect_return('Write the punchline to this joke:\nyou ever notice how zombies are '
                           'just a fancy version of\n_______?')
        self.run_test()

    def test_n11_choose_catchphrase_check_needles_false(self):
        """Joke Boat select catchphrase; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Login_catchphrase_start.html', check_needles=False)
        self.expect_return('Select how to complete your catchphrase:\n'
                           "i’m a little _____!")
        self.run_test()

    def test_n12_write_joke_topic_v1_check_needles_false(self):
        """Joke Boat write joke topic page v1; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v1.html', check_needles=False)
        self.expect_return('Write as many topics as you can.\n'
                           "A PERSON’S NAME")
        self.run_test()

    def test_n13_write_joke_topic_v2_check_needles_false(self):
        """Joke Boat write joke topic page v2; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v2.html', check_needles=False)
        self.expect_return('Write as many topics as you can.\n'
                           'A BRAND')
        self.run_test()

    def test_n14_write_joke_topic_v3_check_needles_false(self):
        """Joke Boat write joke topic page v3; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v3.html', check_needles=False)
        self.expect_return('Write as many topics as you can.\n'
                           'A LOCATION')
        self.run_test()

    def test_n15_write_joke_topic_v4_check_needles_false(self):
        """Joke Boat write joke topic page v4; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v4.html', check_needles=False)
        self.expect_return('Write as many topics as you can.\n'
                           'AN OBJECT')
        self.run_test()

    def test_n16_round_1_perform_joke_1_check_needles_false(self):
        """Joke Boat Round 1 Your Turn; Perform joke 1? page; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Round_1-Perform_joke_1.html', check_needles=False)
        self.expect_return("It’s your turn. What do you want to do?\n"
                           'my nickname is flip phone because i flip out')
        self.run_test()

    def test_n17_round_1_perform_joke_2_check_needles_false(self):
        """Joke Boat Round 1 Your Turn; Perform joke 2? page; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Round_1-Perform_joke_2.html', check_needles=False)
        self.expect_return("It’s your turn. What do you want to do?\n"
                           'god created sporting events by making humans angry')
        self.run_test()

    def test_n18_round_2_perform_joke_1_check_needles_false(self):
        """Joke Boat Round 2 Your Turn; Perform joke 1? page; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Round_2-Perform_joke_1.html', check_needles=False)
        self.expect_return("It’s your turn. What do you want to do?\n"
                           'i have more fears than you')
        self.run_test()

    def test_n19_round_2_perform_joke_2_check_needles_false(self):
        """Joke Boat Round 2 Your Turn; Perform joke 2? page; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Round_2-Perform_joke_2.html', check_needles=False)
        self.expect_return("It’s your turn. What do you want to do?\n"
                           "have you ever tried hoe-ing? that’s when you turn tricks for money")
        self.run_test()

    def test_n20_round_3_perform_joke_1_check_needles_false(self):
        """Joke Boat Round 3 Your Turn; Perform joke 1? page; check_needles == False."""
        self.create_gp_input('JackboxTV-JB-Round_3-Perform_joke_1.html', check_needles=False)
        self.expect_return("It’s your turn. What do you want to do?\n"
                           'you ever notice how zombies are just a fancy version of skeletons?')
        self.run_test()


class ErrorTestJbgJbGetPrompt(TestJbgJbGetPrompt):
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


class SpecialTestJbgJbGetPrompt(TestJbgJbGetPrompt):
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
        self.create_gp_input('JackboxTV-JB-Login_start.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s03_choose_catchphrase(self):
        """Joke Boat select catchphrase."""
        self.create_gp_input('JackboxTV-JB-Login_catchphrase_start.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s04_waiting_on_other_players(self):
        """Joke Boat waiting to start."""
        self.create_gp_input('JackboxTV-JB-Login_waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s05_write_joke_topic_v1(self):
        """Joke Boat write joke topic page v1."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s06_write_joke_topic_v2(self):
        """Joke Boat write joke topic page v2."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v2.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s07_write_joke_topic_v3(self):
        """Joke Boat write joke topic page v3."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v3.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s08_write_joke_topic_v4(self):
        """Joke Boat write joke topic page v4."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v4.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s09_more_waiting(self):
        """Joke Boat post-joke topic page; waiting."""
        self.create_gp_input('JackboxTV-JB-Post_joke_topic_waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s10_round_1_joke_1a_choose_setup(self):
        """Joke Boat Round 1 Joke 1a choose setup page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-A_Choose_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s11_round_1_joke_1b_complete_setup(self):
        """Joke Boat Round 1 Joke 1b complete setup page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s12_round_1_joke_2a_choose_setup(self):
        """Joke Boat Round 1 Joke 2a choose setup page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-A_Choose_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s13_round_1_joke_2b_complete_setup(self):
        """Joke Boat Round 1 Joke 2b complete setup page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-B_Complete_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s14_round_1_waiting(self):
        """Joke Boat post-round 1 joke-completion; waiting."""
        self.create_gp_input('JackboxTV-JB-Round_1_waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s15_round_1_vote_1(self):
        """Joke Boat Round 1 vote page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Vote_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s16_round_1_perform_joke_1(self):
        """Joke Boat Round 1 Your Turn; Perform joke 1? page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Perform_joke_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s17_round_1_perform_joke_2(self):
        """Joke Boat Round 1 Your Turn; Perform joke 2? page."""
        self.create_gp_input('JackboxTV-JB-Round_1-Perform_joke_2.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s18_round_2_joke_1a_choose_setup(self):
        """Joke Boat Round 2 Joke 1a choose setup page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-A_Choose_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s19_round_2_joke_1b_complete_setup(self):
        """Joke Boat Round 2 Joke 1b complete setup page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s20_round_2_joke_2a_choose_setup(self):
        """Joke Boat Round 2 Joke 2a choose setup page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-A_Choose_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s21_round_2_joke_2b_complete_setup(self):
        """Joke Boat Round 2 Joke 2b complete setup page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-B_Complete_setup.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s22_round_2_vote_1(self):
        """Joke Boat Round 2 vote page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Vote_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s23_round_2_perform_joke_1(self):
        """Joke Boat Round 2 Your Turn; Perform joke 1? page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Perform_joke_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s24_round_2_perform_joke_2(self):
        """Joke Boat Round 2 Your Turn; Perform joke 2? page."""
        self.create_gp_input('JackboxTV-JB-Round_2-Perform_joke_2.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s25_round_3a_pick_a_joke(self):
        """Joke Boat Round 3a pick a joke to rewrite."""
        self.create_gp_input('JackboxTV-JB-Round_3-A_Pick_a_joke.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s26_round_3_perform_joke_1(self):
        """Joke Boat Round 3 Your Turn; Perform joke 1? page."""
        self.create_gp_input('JackboxTV-JB-Round_3-Perform_joke_1.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s27_game_done_waiting(self):
        """Joke Boat game done; waiting page."""
        self.create_gp_input('JackboxTV-JB-Game_Done-waiting.html')
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s28_choose_catchphrase_check_needles_true(self):
        """Joke Boat select catchphrase; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Login_catchphrase_start.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s29_write_joke_topic_v1_check_needles_true(self):
        """Joke Boat write joke topic page v1; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v1.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s30_write_joke_topic_v2_check_needles_true(self):
        """Joke Boat write joke topic page v2; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v2.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s31_write_joke_topic_v3_check_needles_true(self):
        """Joke Boat write joke topic page v3; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v3.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s32_write_joke_topic_v4_check_needles_true(self):
        """Joke Boat write joke topic page v4; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v4.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s33_round_1_perform_joke_1_check_needles_true(self):
        """Joke Boat Round 1 Your Turn; Perform joke 1? page; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Round_1-Perform_joke_1.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s34_round_1_perform_joke_2_check_needles_true(self):
        """Joke Boat Round 1 Your Turn; Perform joke 2? page; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Round_1-Perform_joke_2.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s35_round_2_perform_joke_1_check_needles_true(self):
        """Joke Boat Round 2 Your Turn; Perform joke 1? page; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Round_2-Perform_joke_1.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s36_round_2_perform_joke_2_check_needles_true(self):
        """Joke Boat Round 2 Your Turn; Perform joke 2? page; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Round_2-Perform_joke_2.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s37_round_3_perform_joke_1_check_needles_true(self):
        """Joke Boat Round 3 Your Turn; Perform joke 1? page; check_needles == True."""
        self.create_gp_input('JackboxTV-JB-Round_3-Perform_joke_1.html',
                             check_needles=True, use_kwarg=True)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
