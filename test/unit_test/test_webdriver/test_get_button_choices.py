"""Unit test module for jitb_webdriver.get_button_choices().

Typical Usage:
    python -m test                                                          # Run *all* the tests
    python -m test.unit_test                                                # Run *all* unit tests
    python -m test.unit_test.test_webdriver                                 # Run webdriver tests
    python -m test.unit_test.test_webdriver.test_get_button_choices         # Run these unit tests
    python -m test.unit_test.test_webdriver.test_get_button_choices -k n01  # Run just the n01 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jitb_webdriver import get_button_choices


class TestJitbWebdriverGetButtonChoices(TestJackboxGames):
    """The jitb_webdriver.get_button_choices() unit test class.

    This class provides base functionality to run NEBS unit tests for
    jitb_webdriver.get_button_choices().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def set_buttons_input(self, filename: str, *opt_args) -> None:
        """Setup the test input for this test case.

        Args:
            filename: File-based test input used to create the webdriver.
            opt_args: Optional; Passed in as additional arg (use for the optional exclude arg).
        """
        self.create_web_driver(filename=filename)
        if not self.web_driver:
            self.fail_test_case('Failed to create a web driver')
        if opt_args:
            self.set_test_input(self.web_driver, opt_args[0])
        else:
            self.set_test_input(self.web_driver)

    def call_callable(self) -> Any:
        """Calls jitb_webdriver.get_button_choices().

        Overrides the parent method.  Defines the way to call jitb_webdriver.get_button_choices().

        Returns:
            Return value of jitb_webdriver.get_button_choices()

        Raises:
            Exceptions raised by jitb_webdriver.get_button_choices() are bubbled up and handled by
                TediousUnitTest
        """
        return get_button_choices(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate return value.

        Overrides the parent method.  Only compares the expected keys against what is returned.

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.
        """
        # Type
        if not isinstance(return_value, dict):
            self._add_test_failure(f'Expected type dict but it was of type {type(return_value)}')
        elif sorted(list(return_value.keys())) != sorted(self._exp_return):
            self._add_test_failure(f'Expected {self._exp_return} but received '
                                   f'{list(return_value.keys())}')


class NormalTestJitbWebdriverGetButtonChoices(TestJitbWebdriverGetButtonChoices):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        filename = 'JackboxTV-login_start.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['Got it!', 'Opt out'])  # Odd, but legit (see: DEFAULT_BUTTON_VALUE)
        self.run_test()

    def test_n02_q2_opening_instructions(self):
        """Quiplash 2 waiting to start."""
        filename = 'JackboxTv-Q2-waiting_to_start.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_n03_q2_splash_page(self):
        """Quiplash 2 splash page."""
        filename = 'JackboxTv-Q2-splash_page.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_n04_q2_round_1(self):
        """Quiplash 2 Round 1 splash page."""
        filename = 'JackboxTv-Q2-Round_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_n05_q2_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Prompt_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['  SEND', 'SAFETY QUIP\n(HALF POINTS)'])
        self.run_test()

    def test_n06_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['SCRAPPLE', 'BUTTE, MONTANA'])
        self.run_test()

    def test_n07_q2_round_2_prompt_1(self):
        """Quiplash 2 Round 2 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_2-Prompt_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['  SEND', 'SAFETY QUIP\n(HALF POINTS)'])
        self.run_test()

    def test_n08_q2_round_3(self):
        """Quiplash 2 Round 3 splash page."""
        filename = 'JackboxTv-Q2-Round_3.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_n09_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['  SEND'])
        self.run_test()

    def test_n10_q2_round_3_prompt_1_v2(self):
        """Quiplash 2 Round 3 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1-v2.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['  SEND'])
        self.run_test()

    def test_n11_q2_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['SLIMER', 'SLIMEY'])
        self.run_test()

    def test_n12_q2_round_3_waiting(self):
        """Quiplash 2 Round 3 waiting page."""
        filename = 'JackboxTv-Q2-Round_3-waiting.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_n13_q2_game_over(self):
        """Quiplash 2 game over page."""
        filename = 'JackboxTv-Q2-Game_Over.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_n14_joke_boat_catchphrase_selection(self):
        """Joke Boat catchphrase selection page."""
        filename = 'JackboxTV-JB-Login_catchphrase_start.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['cult', 'wireless router', 'floss'])
        self.run_test()

    def test_n15_joke_boat_round_1b_complete_setup(self):
        """Joke Boat Round 1 Complete Setup."""
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['hoe', 'flip phone', 'deck of cards'])
        self.run_test()

    def test_n16_joke_boat_round_2b_complete_setup(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return(['hoe', 'lasso', 'alarm clock'])
        self.run_test()


class ErrorTestJitbWebdriverGetButtonChoices(TestJitbWebdriverGetButtonChoices):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_element_none(self):
        """Bad data type: web_driver == None."""
        self.set_test_input(web_driver=None)
        self.expect_exception(TypeError, 'Web driver can not be of type None')
        self.run_test()

    def test_e02_bad_data_type_web_element_path(self):
        """Bad data type: web_driver == Path()."""
        self.set_test_input(web_driver=Path() / 'test/test_input/JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid web_driver data type of ')
        self.run_test()


class SpecialTestJitbWebdriverGetButtonChoices(TestJitbWebdriverGetButtonChoices):
    """Special Test Cases.

    Organize the Special Test Cases.

    NOTE: Testing the exclusion of 'Reset my choices' from the exclude list, and then expecting
    it in the return value, fails.  I presume it's because that button is not enabled while the
    game isn't active?  Or maybe it tries to verify one reset per game using cookies?  Regardless,
    the exclusion feature works.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        filename = 'xkcd-Good_Code.html'  # File-based test input
        self.set_buttons_input(filename)
        self.expect_return([])
        self.run_test()

    def test_s02_joke_boat_round_1b_complete_setup_exclude_legit_button_1(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'hoe'])
        self.expect_return(['flip phone', 'deck of cards'])
        self.run_test()

    def test_s03_joke_boat_round_1b_complete_setup_exclude_legit_button_2(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'flip phone'])
        self.expect_return(['hoe', 'deck of cards'])
        self.run_test()

    def test_s04_joke_boat_round_1b_complete_setup_exclude_legit_button_3(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'deck of cards'])
        self.expect_return(['hoe', 'flip phone'])
        self.run_test()

    def test_s05_joke_boat_round_2b_complete_setup_exclude_legit_button_1(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'hoe'])
        self.expect_return(['lasso', 'alarm clock'])
        self.run_test()

    def test_s06_joke_boat_round_2b_complete_setup_exclude_legit_button_2(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'lasso'])
        self.expect_return(['hoe', 'alarm clock'])
        self.run_test()

    def test_s07_joke_boat_round_2b_complete_setup_exclude_legit_button_3(self):
        """Joke Boat Round 1 Complete Setup: Override button choices."""
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'alarm clock'])
        self.expect_return(['hoe', 'lasso'])
        self.run_test()

    def test_s08_joke_boat_round_1b_complete_setup_exclude_case_insensitive_1(self):
        """Joke Boat Round 1 Complete Setup: Override button choices.

        Use varying case and expect the same results.
        """
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'hoe'])
        self.expect_return(['flip phone', 'deck of cards'])
        self.run_test()

    def test_s09_joke_boat_round_1b_complete_setup_exclude_case_insensitive_2(self):
        """Joke Boat Round 1 Complete Setup: Override button choices.

        Use varying case and expect the same results.
        """
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'fLIP pHONE'])
        self.expect_return(['hoe', 'deck of cards'])
        self.run_test()

    def test_s10_joke_boat_round_1b_complete_setup_exclude_case_insensitive_3(self):
        """Joke Boat Round 1 Complete Setup: Override button choices.

        Use varying case and expect the same results.
        """
        filename = 'JackboxTV-JB-Round_1-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'dEck oF cArds'])
        self.expect_return(['hoe', 'flip phone'])
        self.run_test()

    def test_s11_joke_boat_round_2b_complete_setup_exclude_case_insensitive_1(self):
        """Joke Boat Round 1 Complete Setup: Override button choices.

        Use varying case and expect the same results.
        """
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'HOE'])
        self.expect_return(['lasso', 'alarm clock'])
        self.run_test()

    def test_s12_joke_boat_round_2b_complete_setup_exclude_case_insensitive_2(self):
        """Joke Boat Round 1 Complete Setup: Override button choices.

        Use varying case and expect the same results.
        """
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'Lasso'])
        self.expect_return(['hoe', 'alarm clock'])
        self.run_test()

    def test_s13_joke_boat_round_2b_complete_setup_exclude_case_insensitive_3(self):
        """Joke Boat Round 1 Complete Setup: Override button choices.

        Use varying case and expect the same results.
        """
        filename = 'JackboxTV-JB-Round_2-Joke_1-B_Complete_setup.html'  # File-based test input
        self.set_buttons_input(filename, ['Reset my choices', 'alarm Clock'])
        self.expect_return(['hoe', 'lasso'])
        self.run_test()

    def test_s14_round_1_vote_1_exclude_case_insensitive_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        self.set_buttons_input(filename, ['scrapple'])
        self.expect_return(['BUTTE, MONTANA'])
        self.run_test()

    def test_s15_round_1_vote_1_exclude_case_insensitive_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        self.set_buttons_input(filename, ['BUTTE, MONTANA'.lower()])
        self.expect_return(['SCRAPPLE'])
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
