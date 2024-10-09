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
from test.unit_test.test_jbgjb.test_jbgjb import TestJbgJb
from tediousstart.tediousstart import execute_test_cases
# Local Imports


# pylint: disable = too-many-public-methods
class TestJbgJbGetPrompt(TestJbgJb):
    """The jbg_jb.get_prompt() unit test class.

    This class provides base functionality to run NEBS unit tests for jbg_jb.get_prompt().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def create_gp_input(self, filename: str, use_kwarg: bool, *gp_opt_args) -> None:
        """Translates file-based test input into a Selenium web driver for test case input.

        Args:
            filename: The file-based test input to create the web driver with.
            use_kwarg: Optional; If True, convert all arguments into keyword arguments.
            gp_opt_args: A tuple of optional get_prompt arguments:
                (prompt_clues), or (prompt_clues, clean_string)

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
            if not gp_opt_args:
                self.set_test_input(web_driver=self.web_driver)
            elif len(gp_opt_args) == 1:
                self.set_test_input(web_driver=self.web_driver, prompt_clues=gp_opt_args[0])
            elif len(gp_opt_args) == 2:
                self.set_test_input(web_driver=self.web_driver, prompt_clues=gp_opt_args[0],
                                    clean_string=gp_opt_args[1])
            else:
                self.fail_test_case(f'Invalid gp_opt_args length: {gp_opt_args}')
        else:
            if not gp_opt_args:
                self.set_test_input(self.web_driver)
            elif len(gp_opt_args) == 1:
                self.set_test_input(self.web_driver, gp_opt_args[0])
            elif len(gp_opt_args) == 2:
                self.set_test_input(self.web_driver, gp_opt_args[0], gp_opt_args[1])
            else:
                self.fail_test_case(f'Invalid gp_opt_args length: {gp_opt_args}')

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
        jbg_jb_obj = self.setup_jbgjb_object()
        return jbg_jb_obj.get_prompt(*self._args, **self._kwargs)


class NormalTestJbgJbGetPrompt(TestJbgJbGetPrompt):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_joke_1c_complete_punchline_clean_string(self):
        """Joke Boat Round 1 Joke 1c complete punchline page; Default optional args."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html',
                             use_kwarg)
        self.expect_return('Joke 1 (of 2) Write your punchline: my nickname is flip phone '
                           'because _______')
        self.run_test()

    def test_n02_round_1_joke_2c_complete_punchline_clean_string(self):
        """Joke Boat Round 1 Joke 2c complete punchline page; Default optional args."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-C_Complete_your_punchline.html',
                             use_kwarg)
        self.expect_return('Joke 2 (of 2) Write your punchline: god created sporting events by '
                           '_______')
        self.run_test()

    def test_n03_round_2_joke_1c_complete_punchline_clean_string(self):
        """Joke Boat Round 2 Joke 1c complete punchline page; Default optional args."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-C_Complete_your_punchline.html',
                             use_kwarg)
        self.expect_return('Joke 1 (of 2) Write your punchline: have you ever tried hoe-ing? '
                           "that's when you _______")
        self.run_test()

    def test_n04_round_2_joke_2c_complete_punchline_clean_string(self):
        """Joke Boat Round 2 Joke 2c complete punchline page; Default optional args."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-C_Complete_your_punchline.html',
                             use_kwarg)
        self.expect_return('Joke 2 (of 2) Write your punchline: i have more fears than '
                           '_______')
        self.run_test()

    def test_n05_round_3b_rewrite_punchline(self):
        """Joke Boat Round 3b rewrite punchline; Default optional args."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_3-B_Rewrite_punchline.html', use_kwarg)
        self.expect_return('Write the punchline to this joke: you ever notice how zombies are '
                           'just a fancy version of _______?')
        self.run_test()

    def test_n06_round_1_joke_1c_complete_punchline_clean_string(self):
        """Joke Boat Round 1 Joke 1c complete punchline page; clean_string == True."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html',
                             use_kwarg, None, True)
        self.expect_return('Joke 1 (of 2) Write your punchline: my nickname is flip phone '
                           'because _______')
        self.run_test()

    def test_n07_round_1_joke_2c_complete_punchline_clean_string(self):
        """Joke Boat Round 1 Joke 2c complete punchline page; clean_string == True."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-C_Complete_your_punchline.html',
                             use_kwarg, None, True)
        self.expect_return('Joke 2 (of 2) Write your punchline: god created sporting events by '
                           '_______')
        self.run_test()

    def test_n08_round_2_joke_1c_complete_punchline_clean_string(self):
        """Joke Boat Round 2 Joke 1c complete punchline page; clean_string == True."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-C_Complete_your_punchline.html',
                             use_kwarg, None, True)
        self.expect_return('Joke 1 (of 2) Write your punchline: have you ever tried hoe-ing? '
                           "that's when you _______")
        self.run_test()

    def test_n09_round_2_joke_2c_complete_punchline_clean_string(self):
        """Joke Boat Round 2 Joke 2c complete punchline page; clean_string == True."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-C_Complete_your_punchline.html',
                             use_kwarg, None, True)
        self.expect_return('Joke 2 (of 2) Write your punchline: i have more fears than '
                           '_______')
        self.run_test()

    def test_n10_round_3b_rewrite_punchline(self):
        """Joke Boat Round 3b rewrite punchline; clean_string == True."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_3-B_Rewrite_punchline.html',
                             use_kwarg, None, True)
        self.expect_return('Write the punchline to this joke: you ever notice how zombies are '
                           'just a fancy version of _______?')
        self.run_test()

    def test_n11_round_1_joke_1c_complete_punchline_clean_string(self):
        """Joke Boat Round 1 Joke 1c complete punchline page; clean_string == False."""
        use_kwarg = True  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_1-C_Complete_your_punchline.html',
                             use_kwarg, None, False)
        self.expect_return('Joke 1 (of 2)\nWrite your punchline:\nmy nickname is flip phone\n'
                           'because _______')
        self.run_test()

    def test_n12_round_1_joke_2c_complete_punchline_clean_string(self):
        """Joke Boat Round 1 Joke 2c complete punchline page; clean_string == False."""
        use_kwarg = True  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_1-Joke_2-C_Complete_your_punchline.html',
                             use_kwarg, None, False)
        self.expect_return('Joke 2 (of 2)\nWrite your punchline:\ngod created sporting events by\n'
                           '_______')
        self.run_test()

    def test_n13_round_2_joke_1c_complete_punchline_clean_string(self):
        """Joke Boat Round 2 Joke 1c complete punchline page; clean_string == False."""
        use_kwarg = True  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_1-C_Complete_your_punchline.html',
                             use_kwarg, None, False)
        self.expect_return('Joke 1 (of 2)\nWrite your punchline:\nhave you ever tried hoe-ing?\n'
                           "that’s when you _______")
        self.run_test()

    def test_n14_round_2_joke_2c_complete_punchline_clean_string(self):
        """Joke Boat Round 2 Joke 2c complete punchline page; clean_string == False."""
        use_kwarg = True  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_2-Joke_2-C_Complete_your_punchline.html',
                             use_kwarg, None, False)
        self.expect_return('Joke 2 (of 2)\nWrite your punchline:\ni have more fears than\n'
                           '_______')
        self.run_test()

    def test_n15_round_3b_rewrite_punchline(self):
        """Joke Boat Round 3b rewrite punchline; False."""
        use_kwarg = True  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Round_3-B_Rewrite_punchline.html',
                             use_kwarg, None, False)
        self.expect_return('Write the punchline to this joke:\nyou ever notice how zombies are '
                           'just a fancy version of\n_______?')
        self.run_test()


class ErrorTestJbgJbGetPrompt(TestJbgJbGetPrompt):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_driver_none(self):
        """Bad input: web_driver; None."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'Web driver can not be of type None')
        self.run_test()

    def test_e02_bad_data_type_web_driver_path(self):
        """Bad input: web_driver; Path."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid web_driver data type of ')
        self.run_test()

    def test_e03_bad_data_type_prompt_clues_string(self):
        """Bad input: prompt_clues; string."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_start.html', use_kwarg, 'BAD DATA TYPE', True)
        self.expect_exception(TypeError, 'Invalid data type for clues')
        self.run_test()

    def test_e04_bad_data_type_prompt_clues_tuple(self):
        """Bad input: prompt_clues; tuple."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_start.html', use_kwarg, ('BAD', 'INPUT'), True)
        self.expect_exception(TypeError, 'Invalid data type for clues')
        self.run_test()

    def test_e05_bad_data_type_prompt_clues_entry(self):
        """Bad input: prompt_clues; list with a non-string."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_start.html', use_kwarg, ['good', 0xBAD], True)
        self.expect_exception(TypeError,
                              'The clues list entry value must be a string instead of type')
        self.run_test()

    def test_e06_bad_data_type_clean_string_none(self):
        """Bad input: clean_string; None."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_start.html', use_kwarg, None, None)
        self.expect_exception(TypeError, 'The clean_string value must be a string instead of type')
        self.run_test()

    def test_e07_bad_data_type_clean_string_string(self):
        """Bad input: clean_string; string."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_start.html', use_kwarg, None, 'True')
        self.expect_exception(TypeError, 'The clean_string value must be a string instead of type')
        self.run_test()


class SpecialTestJbgJbGetPrompt(TestJbgJbGetPrompt):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_web_input('xkcd-Good_Code.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s02_login_page(self):
        """Jackbox.tv Login page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_start.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s03_choose_catchphrase(self):
        """Joke Boat select catchphrase; False positive without any clues."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_catchphrase_start.html', use_kwarg)
        self.expect_return("Select how to complete your catchphrase: i'm a little _____!")
        self.run_test()

    def test_s04_waiting_on_other_players(self):
        """Joke Boat waiting to start."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Login_waiting.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a prompt page')
        self.run_test()

    def test_s05_write_joke_topic_v1(self):
        """Joke Boat write joke topic page v1; False positive without any clues."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_gp_input('JackboxTV-JB-Write_joke_topic_v1.html', use_kwarg)
        self.expect_return("Write as many topics as you can. A PERSON'S NAME")
        self.run_test()
# pylint: enable = too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
