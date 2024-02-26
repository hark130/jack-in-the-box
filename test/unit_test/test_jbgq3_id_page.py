"""Unit test module for JbgQ3.id_page().

These unit tests will use source-controlled file-based input to create test input.

    Usage:
    1. Copy this file and rename it to `test_CALLABLE.py`
    2. Rename the internal 'CALLABLE' placeholders accordingly
    3. Source-control discretely named file-based test input (if applicable)
    4. Define numbered Test Cases within the NEBS classes whose name begins with `test_<NEBS>`
    5. `python3 -m test.unit_tests.test_CALLABLE` to run your test cases

    Troubleshooting:
    Q1. Why didn't my test cases run when I executed `python3 -m unittest`?
    A1a. Ensure your test case module's filename start with `test_`?
    A1b. Is there at least one method name that starts with `test_`?
    Q2. Why didn't my test cases execute with `python3 -m test.unit_tests.test_CALLABLE`?
    A2. Consider the following:
        - Did you replace the command's 'test_CALLABLE' with the actual name of your module?
        - Did you remove or comment out `execute_test_cases()` or the code block that executes
            `execute_test_cases()`?
        - Did you remove, comment, or modify `execute_test_cases()`'s behavior?
        - Is there at least one Test Case whose name starts with `test_`?
        - Try `python3 -m unittest -k CALLABLE` but replace CALLABLE with a substring related
            to your test cases and/or module
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
from jitb.jbgames.jbg_q3 import JbgQ3
from jitb.jitb_openai import JitbAi


class MockedJitbAi(JitbAi):
    """Mock the interfaces for the actual JitbAi for the purposes of testing."""

    def __init__(self, *args, **kwargs) -> None:
        """Class ctor.

        Args:
            model: Optional; OpenAI model to use.  See: https://platform.openai.com/docs/models
        """
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        """Do nothing."""

    def tear_down(self) -> None:
        """Do nothing."""

    def generate_answer(self, prompt: str, length_limit: int = 45) -> str:
        """Randomize from a generic list of answers."""
        generic_answers = ['42', 'the meaning of life', 'nothing', 'no one remembers',
                           'bubble gum', 'Maybe', 'Not sure', "It's possible", 'Could be.',
                           'Let me check', "Can't say", 'Likely', 'I doubt it',
                           "I'll think about it", 'Perhaps not', 'banana flavoring']
        return random.choice(generic_answers)

    # pylint: disable = no-value-for-parameter
    def generate_thriplash(self, prompt: str, length_limit: int = 30) -> list:
        """Get three response from generate_answer()."""
        answer_list = []
        for _ in range(3):
            answer_list.append(self.generate_answer()[:length_limit])

    def vote_favorite(self, prompt: str, answers: list) -> str:
        """Randomly choose an answer."""
        return random.choice(answers)


class TestJbgQ3IdPage(TediousUnitTest):
    """JbgQ3.id_page() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ3.id_page().
    """

    username = 'Test_JBG_Q3_ID_PAGE'  # Default username to use for these unit tests

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
        self.web_driver = None

    def setUp(self) -> None:
        """Prepares Test Case.

        Automate any preparation necessary before each Test Case executes.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        super().setUp()
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def tearDown(self) -> None:
        """Close the web driver."""
        super().tearDown()
        if self.web_driver:
            self.web_driver.close()

    def call_callable(self) -> Any:
        """Calls JbgQ3.id_page().

        Overrides the parent method.  Defines the way to call JbgQ3.id_page().

        Args:
            None

        Returns:
            Return value of JbgQ3IdPage

        Raises:
            Exceptions raised by JbgQ3IdPage are bubbled up and handled by TediousUnitTest
        """
        ai_obj = MockedJitbAi()
        jbg_q3_obj = JbgQ3(ai_obj=ai_obj, username=self.username)
        return jbg_q3_obj.id_page(*self._args, **self._kwargs)

    def create_test_input(self, filename: Path, use_kwarg: bool = False) -> None:
        """Translates file-based test input into a Selenium web driver."""
        # LOCAL VARIABLES
        input_html = Path() / 'test' / 'test_input' / filename   # File-based test input
        options = Options()                                      # Options for the web driver
        self.web_driver = None                                   # Web driver to load the input html

        # SETUP
        options.add_argument('--headless')
        self.web_driver = webdriver.Chrome(options=options)

        # CREATE IT
        self.web_driver.minimize_window()
        self.web_driver.get(input_html.absolute().as_uri())
        if use_kwarg:
            self.set_test_input(web_driver=self.web_driver)
        else:
            self.set_test_input(self.web_driver)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate JbgQ3IdPage return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.  Calls self._validate_return_value() method under the hood.

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.  The intended practice is to use the return value of the
                call_callable() method.

        Returns:
            None

        Raises:
            None
        """
        self._validate_return_value(return_value=return_value)


class NormalTestJbgQ3IdPage(TestJbgQ3IdPage):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_login_page(self):
        """Jackbox.tv Login page."""
        self.create_test_input('JackboxTV-login_start.html')
        self.expect_return(JbgPageIds.LOGIN)
        self.run_test()

    def test_n02_selection_start(self):
        """Quiplash 3 Avatar page; unselected."""
        self.create_test_input('JackboxTv-Q3-avatar_selection-start.html')
        self.expect_return(JbgPageIds.AVATAR)
        self.run_test()

    def test_n03_selection_chosen(self):
        """Quiplash 3 Avatar page; selected."""
        self.create_test_input('JackboxTv-Q3-avatar_selection-selected.html')
        self.expect_return(JbgPageIds.AVATAR)
        self.run_test()

    def test_n04_opening_instructions(self):
        """Quiplash 3 instructions splash page."""
        self.create_test_input('JackboxTv-Q3-Opening_Instructions.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n05_round_1(self):
        """Quiplash 3 Round 1 splash page."""
        self.create_test_input('JackboxTv-Q3-Round_1.html')
        self.expect_return(JbgPageIds.UNKNOWN)
        self.run_test()

    def test_n05_round_1_prompt_1(self):
        """Quiplash 3 Round 1 Prompt 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Prompt_1.html')
        self.expect_return(JbgPageIds.ANSWER)
        self.run_test()

    def test_n05_round_1_vote_1(self):
        """Quiplash 3 Round 1 Vote 1 page."""
        self.create_test_input('JackboxTv-Q3-Round_1-Vote_1-start.html')
        self.expect_return(JbgPageIds.VOTE)
        self.run_test()


class ErrorTestJbgQ3IdPage(TestJbgQ3IdPage):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_none(self):
        """Error input that's expected to fail."""
        self.set_test_input(None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e02_bad_data_type_path(self):
        """Error input that's expected to fail."""
        self.set_test_input(Path() / 'test' / 'test_input' / 'JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


class SpecialTestJbgQ3IdPage(TestJbgQ3IdPage):
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


if __name__ == '__main__':
    execute_test_cases()
