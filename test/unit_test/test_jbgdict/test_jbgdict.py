"""Unit test module for JbgDict."""

# Standard Imports
from typing import Any
# Third Party Imports
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames
# Local Imports
from jitb.jbgames.jbg_dict import JbgDict


class TestJbgDict(TestJackboxGames):
    """JbgDict unit test class.

    This class provides base functionality to run NEBS unit tests for JbgDict methods.
    """

    username = 'Test_JBG_Dict'  # Default username to use for these unit tests

    # CORE CLASS METHODS
    # Methods listed in call order
    def setup_jbgdict_object(self) -> JbgDict:
        """Setup the JbgDict object on behalf of call_callable()."""
        ai_obj = MockedJitbAi()                                        # Mocked JitbAi object
        jbg_dict_obj = JbgDict(ai_obj=ai_obj, username=self.username)  # JbgDict object
        return jbg_dict_obj

    def call_callable(self) -> Any:
        """Child class defines test case callable.

        This method must be overridden by the child class.  Be sure to use the object
        returned by self.setup_jbgdict_object().

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # jbgdict_obj = self.setup_jbgdict_object()
        # return jbgdict_obj.the_method_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self._test_error.format('The child class must override the call_callable method'))
