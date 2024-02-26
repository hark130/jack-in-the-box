"""Defines the package's Jackbox Games Abstract Base Class (ABC)."""

# Standard
from abc import ABC, abstractmethod
from typing import Final, List
# Third Party
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_openai import JitbAi


# List of observed errors reported by Jackbox Games html
ERROR_LIST: Final[List] = ['Room not found']


class JbgAbc(ABC):
    """Jackbox Games (JBG) Abstract Base Class (ABC).

    Typical Usage:
    1. Inherit from JbgAbc
    2. Define a validation method which calls (at a minimum):
        - self._check_web_driver()
        - self._validate_core_attributes()
    3. Define any Jackbox Game-specific functionality (e.g., Quiplash 3 has a Thriplash prompt)
    4. Define the abstract methods, using your validation method.
    """

    # Methods are listed in expected 'call order'.
    def __init__(self, ai_obj: JitbAi, username: str) -> None:
        """JbgAbc ctor.

        Args:
            ai_obj:  OpenAI API interface to use in this game.
            username:  The screen name used in this game.
        """
        self._ai_obj = ai_obj                    # OpenAI API interface to use in this game
        self._avatar_chosen = False              # Only choose one avatar
        self._username = username                # The screen name used in this game
        self._last_page = JbgPageIds.UNKNOWN     # The last page processed
        self._current_page = JbgPageIds.UNKNOWN  # The current page being processed

    @abstractmethod
    def play(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Determine web_driver's page id and call the relevant method.

        Typical definition should look something like this:

        self._current_page = self.id_page(web_driver=web_driver)
        if self._last_page != self._current_page:
            if self._current_page == JbgQuip3IntPages.LOGIN:
                pass  # Wait for the page to change because we already logged in
            elif self._current_page == JbgQuip3IntPages.AVATAR and not self._avatar_chosen:
                self.select_character(web_driver=web_driver)
                self._avatar_chosen = True
            elif self._current_page == JbgQuip3IntPages.ANSWER:
                self.answer_prompts(web_driver=web_driver)
            elif self._current_page == JbgQuip3IntPages.VOTE:
                self.vote_answers(web_driver=web_driver)
            elif [...]

        Raises:
            RuntimeError: An error message was found in the HTML or web_driver is the wrong page.
            TypeError: An internal attribute is the wrong data type.
            ValueError: An internal attribute contains an invalid value.
        """
        pass

    @abstractmethod
    def select_character(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Randomize an avatar selection from the available list.

        Args:
            web_driver: The webdriver object to interact with.

        Raises:
            RuntimeError: An error message was found in the HTML, this isn't the character
                selection page, or a character selection failed.
        """
        pass

    @abstractmethod
    def answer_prompts(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read a prompt from the web_driver, ask the AI, and submit the AI's answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        pass

    @abstractmethod
    def vote_answers(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read other answers to a prompt from the web_driver, ask the AI, and submit the answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        pass

    @abstractmethod
    def id_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> JbgPageIds:
        """Determine what type of Jackbox Games webpage web_driver is.

        The jackbox.tv login page should be universal so start with self._is_login_page()
        when defining this method in the child class.

        Args:
            web_driver: The webdriver object to interact with.
        """
        pass

    # Private methods in alphabetical order.
    def _check_web_driver(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Check the driver's page source for known errors.

        Raises:
            RuntimeError: An error message was found in the HTML or the room was disconnected.
        """
        # LOCAL VARIABLES
        temp_we = None  # Temp web element object

        # CHECK IT
        if web_driver:
            # Check for errors
            for error in ERROR_LIST:
                if error in web_driver.page_source:
                    raise RuntimeError(error)
            # Verify not disconnected
            try:
                temp_we = web_driver.find_element(By.ID, 'swal2-title')
            except NoSuchElementException:
                pass  # It's good that we didn't find it
            else:
                if temp_we.text.lower().startswith('Disconnected'.lower()):
                    raise RuntimeError('The room was disconnected')

    def _is_login_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Determine if this is this the login page.

        This method may not need to be a method but it's uniquely related to this class so
        here it is.

        Returns:
            True if this is the login screen, False otherwise.
        """
        # LOCAL VARIABLES
        login_page = False  # Prove this true

        # IS IT?
        try:
            web_driver.find_element(By.ID, 'roomcode')
            web_driver.find_element(By.ID, 'username')
            web_driver.find_element(By.ID, 'button-join')
        except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
            pass  # Not the character selection page
        else:
            login_page = True  # If we made it here, it's the login page

        # DONE
        return login_page

    def _validate_core_attributes(self) -> None:
        """Validate private attribute types and values.

        Call this method in any inherited child class methods performing similar validation
        for child-class specific attributes.

        Raises:
            TypeError: An internal attribute is the wrong data type.
            ValueError: An internal attribute contains an invalid value.
        """
        # JitbAi
        if not isinstance(self._ai_obj, JitbAi):
            raise TypeError(f'Invalid data type of {type(self._ai_obj)} for the AI object')
        # Avatar Chosen
        if not isinstance(self._avatar_chosen, bool):
            raise TypeError(f'Invalid data type of {type(self._avatar_chosen)} for "avatar chosen"')
        # Username
        if not isinstance(self._username, str):
            raise TypeError(f'Invalid data type of {type(self._username)} for the username')
        if not self._username:
            raise ValueError('The username may not be blank')
        # Last page
        _validate_page_id(page_id=self._last_page, var_name='last page')
        # Current page
        _validate_page_id(page_id=self._current_page, var_name='current page')


# Private functions
def _validate_page_id(page_id: JbgPageIds, var_name: str) -> None:
    """Validate a JbgPageIds object.

    Raises:
        TypeError: page_id is the wrong data type.
    """
    if not isinstance(page_id, JbgPageIds):
        raise TypeError(f'JbgPageIds "{var_name}" is an invalid data type of {type(page_id)}')
