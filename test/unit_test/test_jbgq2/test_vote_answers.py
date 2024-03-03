"""Unit test module for JbgQ2.vote_answers().

These unit tests will skip typical input testing (e.g., Error) because the jbg_q2.py functionality
that validates the identify of the web_driver is implicitly tested elsewhere.
See: test.unit_test.test_jbgq2.test_id_page.

Typical Usage:
    python -m test                                                # Run *all* the test cases
    python -m test.unit_test                                      # Run *all* the unit test cases
    python -m test.unit_test.test_jbgq2                           # Run *all* jbgq2 unit tests cases
    python -m test.unit_test.test_jbgq2.test_vote_answers         # Run just these unit tests
    python -m test.unit_test.test_jbgq2.test_vote_answers -k n01  # Run just this normal 1 unit test
"""

# Standard Imports
from typing import Any
# Third Party Imports
from test.unit_test.test_jbgq2.test_jbgq2 import TestJbgQ2
from tediousstart.tediousstart import execute_test_cases
# Local Imports


class TestJbgQ2VoteAnswers(TestJbgQ2):
    """JbgQ2.vote_answers() unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ2.vote_answers().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls JbgQ2.vote_answers().

        Overrides the parent method.  Defines the way to call JbgQ2.vote_answers().

        Args:
            None

        Returns:
            Return value of JbgQ2.vote_answers()

        Raises:
            Exceptions raised by JbgQ2.vote_answers() are bubbled up and handled by TediousUnitTest
        """
        jbg_q2_obj = self.setup_jbgq2_object()
        return jbg_q2_obj.vote_answers(*self._args, **self._kwargs)


class NormalTestJbgQ2VoteAnswers(TestJbgQ2VoteAnswers):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_round_3_vote_1(self):
        """Quiplash 2 Round 3 Vote 1 page.

        Minimum number of players so there's no vote for silver or bronze.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1.html')
        self.expect_return(None)
        self.run_test()

    def test_n02_round_3_vote_1_v2(self):
        """Quiplash 2 Round 3 Vote 1 v2 page.

        Minimum number of players so there's no vote for silver or bronze.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v2.html')
        self.expect_return(None)
        self.run_test()

    def test_n03_round_3_vote_1_v2(self):
        """Quiplash 2 Round 3 Vote 1 v3 page.

        Minimum number of players so there's no vote for silver or bronze.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_1-v3.html')
        self.expect_return(None)
        self.run_test()


class SpecialTestJbgQ2VoteAnswers(TestJbgQ2VoteAnswers):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_round_3_vote_2(self):
        """Quiplash 2 Round 3 Vote 2 page.

        There's enough players that the game called for a silver medal vote.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_2-Silver_Medal.html')
        self.expect_return(None)
        self.run_test()

    def test_s02_round_3_vote_3(self):
        """Quiplash 2 Round 3 Vote 3 page.

        There's enough players that the game called for a bronze medal vote.
        """
        self.create_test_input('JackboxTv-Q2-Round_3-Vote_3-Bronze_Medal.html')
        self.expect_return(None)
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
