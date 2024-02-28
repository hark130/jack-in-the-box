"""Unit test module for jitb_selenium.get_web_element_text().

Typical Usage:
    python -m test                                                           # Run *all* test cases
    python -m test.unit_test                                                 # Run *all* unit tests
    python -m test.unit_test.test_jitb_selenium_get_web_element_text         # Run these unit tests
    python -m test.unit_test.test_jitb_selenium_get_web_element_text -k n01  # Just run the n01 test
"""

# Standard Imports
from pathlib import Path
from typing import Any
from unittest import skip
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
from selenium.webdriver.common.by import By
import selenium
# Local Imports
from jitb.jitb_logger import Logger
from jitb.jitb_selenium import get_web_element_text


class TestJitbSeleniumGetWebElementText(TestJackboxGames):
    """The jitb_selenium.get_web_element_text() unit test class.

    This class provides base functionality to run NEBS unit tests for
    jitb_selenium.get_web_element_text().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
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
        Logger.initialize(debugging=True)  # Enable DEBUG logging while testing

    def expect_element_return(self, filename: str, by: str = By.ID, value: str = None) -> None:
        """Double do the child element text extraction and pass that to self.expect_return."""
        self.create_web_driver(filename=filename)
        child_element = self.web_driver.find_element(by=by, value=value)  # Expected return
        if not child_element:
            self.fail_test_case(f'Failed to generate an expected return for {by}:{value}')
        self.expect_return(child_element.text)

    def set_web_element_input(self, filename: str, in_by: Any, in_value: Any,
                              use_kwargs: bool = False) -> None:
        """Setup the test input for this test case."""
        self.create_web_driver(filename=filename)
        if use_kwargs:
            self.set_test_input(web_driver=self.web_driver, by=in_by, value=in_value)
        else:
            self.set_test_input(self.web_driver, in_by, in_value)

    def call_callable(self) -> Any:
        """Calls jitb_selenium.get_web_element_text().

        Overrides the parent method.  Defines the way to call jitb_selenium.get_web_element_text().

        Args:
            None

        Returns:
            Return value of jitb_selenium.get_web_element_text()

        Raises:
            Exceptions raised by jitb_selenium.get_web_element_text() are bubbled up and handled by
                TediousUnitTest
        """
        return get_web_element_text(*self._args, **self._kwargs)


class NormalTestJitbSeleniumGetWebElementText(TestJitbSeleniumGetWebElementText):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_1_prompt_1(self):
        """Quiplash 2 Round 1 Prompt 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Prompt_1.html'  # File-based test input
        in_by = By.ID                                    # By type of the element
        in_value = 'state-answer-question'               # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_element_return(filename=filename, by=in_by, value=in_value)
        self.run_test()

    def test_n02_round_1_vote_1(self):
        """Quiplash 2 Round 1 Vote 1 page."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        in_by = By.ID                                  # By type of the element
        in_value = 'game'                              # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_element_return(filename=filename, by=in_by, value=in_value)
        self.run_test()

    def test_n03_round_3_prompt_1_v1(self):
        """Quiplash 2 Round 3 Last Lash prompt page v1."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1.html'  # File-based test input
        in_by = By.ID                                    # By type of the element
        in_value = 'page-quiplash'                       # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_element_return(filename=filename, by=in_by, value=in_value)
        self.run_test()

    def test_n04_round_3_prompt_1_v2(self):
        """Quiplash 2 Round 3 Last Lash prompt page v2."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1-v2.html'  # File-based test input
        in_by = By.ID                                       # By type of the element
        in_value = 'page-quiplash'                          # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_element_return(filename=filename, by=in_by, value=in_value)
        self.run_test()

    def test_n05_round_3_vote_1_v1(self):
        """Quiplash 2 Round 3 Last Lash vote page v1."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1.html'  # File-based test input
        in_by = By.ID                                  # By type of the element
        in_value = 'page-quiplash'                     # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_element_return(filename=filename, by=in_by, value=in_value)
        self.run_test()

    def test_n06_round_3_vote_1_v2(self):
        """Quiplash 2 Round 3 Last Lash vote page v2."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1-v2.html'  # File-based test input
        in_by = By.ID                                     # By type of the element
        in_value = 'question-text-alt'                    # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_element_return(filename=filename, by=in_by, value=in_value)
        self.run_test()


class ErrorTestJitbSeleniumGetWebElementText(TestJitbSeleniumGetWebElementText):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_web_element_none(self):
        """Bad data type: web_driver == None."""
        self.set_test_input(web_driver=None)
        self.expect_exception(TypeError, 'Web driver may not be None')
        self.run_test()

    def test_e02_bad_data_type_web_element_path(self):
        """Bad data type: web_driver == Path()."""
        self.set_test_input(web_driver=Path() / 'test/test_input/JackboxTV-login_start.html')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e03_bad_data_type_by_none(self):
        """Bad data type: by == None."""
        self.create_web_driver(filename='JackboxTV-login_start.html')
        self.set_test_input(web_driver=self.web_driver, by=None)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e04_bad_data_type_by_package_enum(self):
        """Bad data type: by == By."""
        self.create_web_driver(filename='JackboxTV-login_start.html')
        self.set_test_input(web_driver=self.web_driver, by=By)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e05_bad_data_type_by_enum_literal(self):
        """Bad data type: by == By."""
        self.create_web_driver(filename='JackboxTV-login_start.html')
        self.set_test_input(web_driver=self.web_driver, by='By.ID')
        self.expect_exception(ValueError,
                              'Use By value from the selenium.webdriver.common.by module')
        self.run_test()

    def test_e06_bad_data_type_value_list(self):
        """Bad data type: value == []."""
        self.create_web_driver(filename='JackboxTV-login_start.html')
        self.set_test_input(web_driver=self.web_driver, value=[])
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e07_bad_data_type_value_bytes(self):
        """Bad data type: value == b''."""
        self.create_web_driver(filename='JackboxTV-login_start.html')
        self.set_test_input(web_driver=self.web_driver, value=b'find-this')
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()


class SpecialTestJitbSeleniumGetWebElementText(TestJitbSeleniumGetWebElementText):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_round_1_prompt_1(self):
        """KEY TEXT: Quiplash 2 Round 1 Prompt 1 page; value state-answer-question."""
        filename = 'JackboxTv-Q2-Round_1-Prompt_1.html'  # File-based test input
        in_by = By.ID                                    # By type of the element
        in_value = 'state-answer-question'               # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('You know you’re staying at a dirty hotel when they offer a free '
                           'continental ________\n  SEND SAFETY QUIP\n(HALF POINTS)')
        self.run_test()

    def test_s02_round_1_prompt_1_take_2(self):
        """KEY TEXT: Quiplash 2 Round 1 Prompt 1 page; value question-text."""
        filename = 'JackboxTv-Q2-Round_1-Prompt_1.html'  # File-based test input
        in_by = By.ID                                    # By type of the element
        in_value = 'question-text'                       # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('You know you’re staying at a dirty hotel when they offer a '
                           'free continental ________')
        self.run_test()

    def test_s03_round_1_vote_1(self):
        """KEY TEXT: Quiplash 2 Round 1 Vote 1 page; value state-vote."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        in_by = By.ID                                  # By type of the element
        in_value = 'state-vote'                        # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('An inappropriate time to wear a tuxedo\n' + \
                           'Which one do you like more?\n'.upper() + \
                           'SCRAPPLE\nBUTTE, MONTANA')
        self.run_test()

    @skip('This test case seems to indicate a need for get_sub_element()')
    def test_s04_round_1_vote_1_take_2(self):
        """KEY TEXT: Quiplash 2 Round 1 Vote 1 page; value question-text."""
        filename = 'JackboxTv-Q2-Round_1-Vote_1.html'  # File-based test input
        in_by = By.ID                                  # By type of the element
        in_value = 'question-text'                     # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('An inappropriate time to wear a tuxedo')
        # This may require get_sub_element() to work properly
        # NOTE: get_web_element('state-vote'), *then* get_sub_element('question-text')
        self.run_test()

    def test_s05_round_3_prompt_1_v1(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash prompt page v1; value state-answer-question."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1.html'  # File-based test input
        in_by = By.ID                                    # By type of the element
        in_value = 'state-answer-question'               # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title:\n'
                           'SLIME\n  SEND')
        self.run_test()

    def test_s06_round_3_prompt_1_v1_take_2(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash prompt page v1; value question-text-alt."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1.html'  # File-based test input
        in_by = By.ID                                    # By type of the element
        in_value = 'question-text-alt'                   # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title:')
        self.run_test()

    def test_s07_round_3_prompt_1_v2(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash prompt page v2; value state-answer-question."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1-v2.html'  # File-based test input
        in_by = By.ID                                       # By type of the element
        in_value = 'state-answer-question'                  # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a full name for this acronym!\nW.A.W.\n  SEND')
        self.run_test()

    def test_s08_round_3_prompt_1_v2_take_2(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash prompt page v2; value question-text-alt."""
        filename = 'JackboxTv-Q2-Round_3-Prompt_1-v2.html'  # File-based test input
        in_by = By.ID                                       # By type of the element
        in_value = 'question-text-alt'                      # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a full name for this acronym!')
        self.run_test()

    def test_s09_round_3_vote_1_v1(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash vote page v1; value state-vote."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1.html'  # File-based test input
        in_by = By.ID                                  # By type of the element
        in_value = 'state-vote'                        # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title:\n'
                           'SLIME\n' + 'Which one do you like more?'.upper() + '\nSLIMER\nSLIMEY')
        self.run_test()

    @skip('This test case seems to indicate a need for get_sub_element()')
    def test_s10_round_3_vote_1_v1_take_2(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash vote page v1; value question-text-alt."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1.html'  # File-based test input
        in_by = By.ID                                  # By type of the element
        in_value = 'question-text-alt'                 # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a new hilarious sitcom with this word in the title:')
        # This may require get_sub_element() to work properly
        # NOTE: get_web_element('state-vote'), *then* get_sub_element('question-text-alt')
        self.run_test()

    def test_s11_round_3_vote_1_v2(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash vote page v2; value state-vote."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1-v2.html'  # File-based test input
        in_by = By.ID                                     # By type of the element
        in_value = 'state-vote'                           # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a full name for this acronym!\n'
                           'W.A.W.\n' + 'Which one do you like more?'.upper() + '\nWIN A WAR\n5')
        self.run_test()

    @skip('This test case seems to indicate a need for get_sub_element()')
    def test_s12_round_3_vote_1_v2_take_2(self):
        """KEY TEXT: Quiplash 2 Round 3 Last Lash vote page v2; value question-text-alt."""
        filename = 'JackboxTv-Q2-Round_3-Vote_1-v2.html'  # File-based test input
        in_by = By.ID                                     # By type of the element
        in_value = 'question-text-alt'                    # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return('Come up with a full name for this acronym!')
        # This may require get_sub_element() to work properly
        # NOTE: get_web_element('state-vote'), *then* get_sub_element('question-text-alt')
        self.run_test()

    def test_s13_non_jackbox_game_page(self):
        """Non-Jackbox Games website."""
        filename = 'xkcd-Good_Code.html'    # File-based test input
        in_by = By.ID                       # By type of the element
        in_value = 'state-answer-question'  # Name of the element
        self.set_web_element_input(filename=filename, in_by=in_by, in_value=in_value)
        self.expect_return(None)
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
