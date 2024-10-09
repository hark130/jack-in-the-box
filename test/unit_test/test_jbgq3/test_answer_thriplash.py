"""Unit test module for JbgQ3.answer_thriplash().

Typical Usage:
    python -m test                                                    # Run *all* the test cases
    python -m test.unit_test                                          # Run *all* the unit tests
    python -m test.unit_test.test_jbgq3                               # Run *all* jbgq3 test cases
    python -m test.unit_test.test_jbgq3.test_answer_thriplash         # Run just these unit tests
    python -m test.unit_test.test_jbgq3.test_answer_thriplash -k n01  # Run just this normal 1 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgq3.test_jbgq3 import TestJbgQ3
from tediousstart.tediousstart import execute_test_cases
# Local Imports


class TestJbgQ3AnswerThriplash(TestJbgQ3):
    """JbgQ3.answer_thriplash() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ3.answer_thriplash().
    """
    # CORE CLASS METHODS
    # Methods listed in call order
    def create_test_input(self, filename: str, use_kwarg: bool) -> None:
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

    def call_callable(self) -> Any:
        """Calls JbgQ3.answer_thriplash().

        Overrides the parent method.  Defines the way to call JbgQ3.answer_thriplash().

        Args:
            None

        Returns:
            Return value of JbgQ3.answer_thriplash()

        Raises:
            Exceptions raised by JbgQ3.answer_thriplash() are bubbled up and handled by TediousUnitTest
        """
        jbg_q3_obj = self.setup_jbgq3_object()
        return jbg_q3_obj.answer_thriplash(*self._args, **self._kwargs)


class NormalTestJbgQ3AnswerThriplash(TestJbgQ3AnswerThriplash):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_q3_round_3_thriplash(self):
        """Quiplash 3 Round 3 Thriplash."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_3-Prompt_1.html', use_kwarg)
        self.expect_return(None)
        self.run_test()


class ErrorTestJbgQ3AnswerThriplash(TestJbgQ3AnswerThriplash):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_driver_none(self):
        """Bad input: web_driver; None."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'Invalid data type of ')
        self.run_test()

    def test_e02_bad_data_type_web_driver_path(self):
        """Bad input: web_driver; Path."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type of ')
        self.run_test()


class SpecialTestJbgQ3AnswerThriplash(TestJbgQ3AnswerThriplash):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('xkcd-Good_Code.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s02_q3_avatar_start(self):
        """Quiplash 3 Avatar Selection start."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-avatar_selection-start.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s03_q3_avatar_selection(self):
        """Quiplash 3 Avatar Selection done."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-avatar_selection-selected.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s04_q3_instructions(self):
        """Quiplash 3 instructions (waiting) page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Opening_Instructions.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s05_q3_round_1(self):
        """Quiplash 3 Round 1 (waiting) page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_1.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s06_q3_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_2-Prompt_1.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s07_q3_round_2_prompt_1(self):
        """Quiplash 3 Round 2 Prompt 1 page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_2-Prompt_2.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()

    def test_s08_q3_round_3_vote_1(self):
        """Quiplash 3 Round 3 Vote 1 page."""
        use_kwarg = False  # Tells the test framework how to pass in the input
        self.create_test_input('JackboxTv-Q3-Round_3-Vote_1.html', use_kwarg)
        self.expect_exception(RuntimeError, 'This is not the Thriplash prompt page')
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
