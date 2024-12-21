"""Unit test module for JbgBr."""

# Standard Imports
from typing import Any
# Third Party Imports
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames
# Local Imports
from jitb.jbgames.jbg_br import JbgBr


class TestJbgBr(TestJackboxGames):
    """JbgBr unit test class.

    This class provides base functionality to run NEBS unit tests for JbgBr methods.
    """

    username = 'Test_JBG_BR'  # Default username to use for these unit tests

    # CORE CLASS METHODS
    # Methods listed in call order
    def setup_jbgbr_object(self) -> JbgBr:
        """Setup the JbgBr object on behalf of call_callable()."""
        ai_obj = MockedJitbAi()                                    # Mocked JitbAi object
        jbg_br_obj = JbgBr(ai_obj=ai_obj, username=self.username)  # JbgBr object
        return jbg_br_obj

    def call_callable(self) -> Any:
        """Child class defines test case callable.

        This method must be overridden by the child class.  Be sure to use the object
        returned by self.setup_jbgjb_object().

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # jbgbr_obj = self.setup_jbgbr_object()
        # return jbgbr_obj.the_method_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self._test_error.format('The child class must override the call_callable method'))
