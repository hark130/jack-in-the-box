"""Unit test module for JbgQ3.get_vote_text().

Typical Usage:
    python -m test                                                 # Run *all* the test cases
    python -m test.unit_test                                       # Run *all* the unit test cases
    python -m test.unit_test.test_jbgq3                            # Run *all* jbgq3 test cases
    python -m test.unit_test.test_jbgq3.test_get_vote_text         # Run just these unit tests
    python -m test.unit_test.test_jbgq3.test_get_vote_text -k n01  # Run just this normal 1 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgq3.test_jbgq3 import TestJbgQ3
from tediousstart.tediousstart import execute_test_cases
# Local Imports


class TestJbgQ3GetVoteText(TestJbgQ3):
    """JbgQ3.get_vote_text() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ3.get_vote_text().
    """
    # CORE CLASS METHODS
    # Methods listed in call order
    def create_test_input(self, filename: str, use_kwarg: bool, *gp_opt_args) -> None:
        """Translates file-based test input into a Selenium web driver for test case input.

        Args:
            filename: The file-based test input to create the web driver with.
            use_kwarg: Optional; If True, convert all arguments into keyword arguments.
            gp_opt_args: A tuple of optional get_prompt arguments:
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
            if not gp_opt_args:
                self.set_test_input(web_driver=self.web_driver)
            elif len(gp_opt_args) == 1:
                self.set_test_input(web_driver=self.web_driver, vote_clues=gp_opt_args[0])
            elif len(gp_opt_args) == 2:
                self.set_test_input(web_driver=self.web_driver, vote_clues=gp_opt_args[0],
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
        """Calls JbgQ3.get_vote_text().

        Overrides the parent method.  Defines the way to call JbgQ3.get_vote_text().

        Args:
            None

        Returns:
            Return value of JbgQ3.get_vote_text()

        Raises:
            Exceptions raised by JbgQ3.get_vote_text() are bubbled up and handled by TediousUnitTest
        """
        jbg_q3_obj = self.setup_jbgq3_object()
        return jbg_q3_obj.get_vote_text(*self._args, **self._kwargs)


class NormalTestJbgQ3GetVoteText(TestJbgQ3GetVoteText):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_q3_round_1_vote_1_default_args(self):
        """Quiplash 3 Round 1 Vote 1; default args."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html', use_kwarg)
        self.expect_return('The weirdest thing your Uber driver could offer you  '
                           'Vote for your favorite')
        self.run_test()

    def test_n02_q3_round_1_vote_1_clean_string_true(self):
        """Quiplash 3 Round 1 Vote 1; clean_string == True."""
        use_kwarg = False    # Tells the test framework how to pass in the input
        vote_clues = None    # Vote page clues
        clean_string = True  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return('The weirdest thing your Uber driver could offer you  '
                           'Vote for your favorite')
        self.run_test()

    def test_n03_q3_round_1_vote_1_clean_string_false(self):
        """Quiplash 3 Round 1 Vote 1; clean_string == False."""
        use_kwarg = False     # Tells the test framework how to pass in the input
        vote_clues = None     # Vote page clues
        clean_string = False  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return('The weirdest thing your Uber driver could offer you\n\n'
                           'Vote for your favorite')
        self.run_test()

    def test_n04_q3_round_1_vote_1_kwargs(self):
        """Quiplash 3 Round 1 Vote 1; clean_string == False."""
        use_kwarg = True      # Tells the test framework how to pass in the input
        vote_clues = None     # Vote page clues
        clean_string = False  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return('The weirdest thing your Uber driver could offer you\n\n'
                           'Vote for your favorite')
        self.run_test()

    def test_n05_q3_round_2_vote_1_clean_string_true(self):
        """Quiplash 3 Round 2 Vote 1; clean_string == True."""
        use_kwarg = False    # Tells the test framework how to pass in the input
        vote_clues = None    # Vote page clues
        clean_string = True  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_2-Vote_1-start.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return('The discontinued Nobel Prize: the Nobel Prize in _______  '
                           'Vote for your favorite')
        self.run_test()

    def test_n06_q3_round_2_vote_1_clean_string_false(self):
        """Quiplash 3 Round 2 Vote 1; clean_string == False."""
        use_kwarg = False     # Tells the test framework how to pass in the input
        vote_clues = None     # Vote page clues
        clean_string = False  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_2-Vote_1-start.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return('The discontinued Nobel Prize: the Nobel Prize in _______\n\n'
                           'Vote for your favorite')
        self.run_test()

    def test_n07_q3_round_3_vote_1_clean_string_true(self):
        """Quiplash 3 Round 3 Vote 1; clean_string == True."""
        use_kwarg = False    # Tells the test framework how to pass in the input
        vote_clues = None    # Vote page clues
        clean_string = True  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_3-Vote_1.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return("Three Zoom backgrounds nobody's asking for "
                           'Vote for your favorite')
        self.run_test()

    def test_n08_q3_round_3_vote_1_clean_string_false(self):
        """Quiplash 3 Round 3 Vote 1; clean_string == False."""
        use_kwarg = False     # Tells the test framework how to pass in the input
        vote_clues = None     # Vote page clues
        clean_string = False  # Clean string
        self.create_test_input('JackboxTv-Q3-Round_3-Vote_1.html', use_kwarg,
                               vote_clues, clean_string)
        self.expect_return('Three Zoom backgrounds nobody’s asking for\n'
                           'Vote for your favorite')
        self.run_test()


class ErrorTestJbgQ3GetVoteText(TestJbgQ3GetVoteText):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_driver_none(self):
        """Bad input: web_driver; None."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e02_bad_data_type_web_driver_path(self):
        """Bad input: web_driver; Path."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e03_bad_data_type_vote_clues_string(self):
        """Bad input: vote_clues; string."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTV-JB-Login_start.html', use_kwarg, 'BAD DATA TYPE', True)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e04_bad_data_type_vote_clues_tuple(self):
        """Bad input: vote_clues; tuple."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTV-JB-Login_start.html', use_kwarg, ('BAD', 'INPUT'), True)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e05_bad_data_type_vote_clues_entry(self):
        """Bad input: vote_clues; list with a non-string."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTV-JB-Login_start.html', use_kwarg, ['good', 0xBAD], True)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e06_bad_data_type_clean_string_none(self):
        """Bad input: clean_string; None."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTV-JB-Login_start.html', use_kwarg, None, None)
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_e07_bad_data_type_clean_string_string(self):
        """Bad input: clean_string; string."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTV-JB-Login_start.html', use_kwarg, None, 'True')
        self.expect_exception(TypeError, 'expected type')
        self.run_test()


class SpecialTestJbgQ3GetVoteText(TestJbgQ3GetVoteText):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('xkcd-Good_Code.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()

    def test_s02_q3_avatar_start(self):
        """Quiplash 3 Avatar Selection start."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-avatar_selection-start.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()

    def test_s03_q3_avatar_selection(self):
        """Quiplash 3 Avatar Selection done."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-avatar_selection-selected.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()

    def test_s04_q3_instructions(self):
        """Quiplash 3 instructions (waiting) page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Opening_Instructions.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()

    def test_s05_q3_round_1(self):
        """Quiplash 3 Round 1 (waiting) page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_1.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()

    def test_s06_q3_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        use_kwarg = False                        # Tells the test framework how to pass in the input
        vote_clues = ['Vote for your favorite']  # Vote page clues
        self.create_test_input('JackboxTv-Q3-Round_2-Prompt_1.html', use_kwarg, vote_clues)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()

    def test_s07_q3_round_2_prompt_1(self):
        """Quiplash 3 Round 2 Prompt 1 page."""
        use_kwarg = False                        # Tells the test framework how to pass in the input
        vote_clues = ['Vote for your favorite']  # Vote page clues
        self.create_test_input('JackboxTv-Q3-Round_2-Prompt_2.html', use_kwarg, vote_clues)
        self.expect_exception(RuntimeError, 'This is not a vote page')
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
