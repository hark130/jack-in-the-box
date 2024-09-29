"""Unit test module for JbgQ3."""

# Standard Imports
from typing import Any
# Third Party Imports
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames
# Local Imports
from jitb.jbgames.jbg_q3 import JbgQ3


class TestJbgQ3(TestJackboxGames):
    """JbgQ3 unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ3 methods.
    """

    username = 'Test_JBG_Q3'  # Default username to use for these unit tests

    # CORE CLASS METHODS
    # Methods listed in call order
    def setup_jbgq3_object(self) -> JbgQ3:
        """Setup the JbgQ3 object on behalf of call_callable()."""
        ai_obj = MockedJitbAi()                                    # Mocked JitbAi object
        jbg_q3_obj = JbgQ3(ai_obj=ai_obj, username=self.username)  # JbgQ3 object
        return jbg_q3_obj

    def call_callable(self) -> Any:
        """Child class defines test case callable.

        This method must be overridden by the child class.  Be sure to use the object
        returned by self.setup_jbgjb_object().

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # jbgjb_obj = self.setup_jbgjb_object()
        # return jbgjb_obj.the_method_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self._test_error.format('The child class must override the call_callable method'))
