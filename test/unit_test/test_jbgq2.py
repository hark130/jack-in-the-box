"""Unit test module for JbgQ2."""

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
from jitb.jbgames.jbg_q2 import JbgQ2
from jitb.jitb_openai import JitbAi
from test.mocked_jitb_ai import MockedJitbAi
from test.unit_test.test_jackbox_games import TestJackboxGames


class TestJbgQ2(TestJackboxGames):
    """JbgQ2 unit test class.

    This class provides base functionality to run NEBS unit tests for JbgQ2 methods.
    """

    username = 'Test_JBG_Q2'  # Default username to use for these unit tests

    # CORE CLASS METHODS
    # Methods listed in call order
    def setup_jbgq2_object(self) -> JbgQ2:
        """Setup the JbgQ2 object on behalf of call_callable()."""
        ai_obj = MockedJitbAi()                                    # Mocked JitbAi object
        jbg_q2_obj = JbgQ2(ai_obj=ai_obj, username=self.username)  # JbgQ2 object
        return jbg_q2_obj

    def call_callable(self) -> Any:
        """Child class defines test case callable.

        This method must be overridden by the child class.  Be sure to use the object
        returned by self.setup_jbgq2_object().

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # jbgq2_obj = self.setup_jbgq2_object()
        # return jbgq2_obj.the_method_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self._test_error.format('The child class must override the call_callable method'))
