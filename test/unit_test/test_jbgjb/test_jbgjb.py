"""Unit test module for JbgJb."""

# Standard Imports
from typing import Any
# Third Party Imports
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames
# Local Imports
from jitb.jbgames.jbg_jb import JbgJb


class TestJbgJb(TestJackboxGames):
    """JbgJb unit test class.

    This class provides base functionality to run NEBS unit tests for JbgJb methods.
    """

    username = 'Test_JBG_JB'  # Default username to use for these unit tests

    # CORE CLASS METHODS
    # Methods listed in call order
    def setup_jbgjb_object(self) -> JbgJb:
        """Setup the JbgJb object on behalf of call_callable()."""
        ai_obj = MockedJitbAi()                                    # Mocked JitbAi object
        jbg_jb_obj = JbgJb(ai_obj=ai_obj, username=self.username)  # JbgJb object
        return jbg_jb_obj

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
