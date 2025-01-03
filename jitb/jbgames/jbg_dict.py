"""Defines the package's Jackbox Games Dictionarium class."""

# Standard
from typing import Final
import time
# Third Party
from selenium.common.exceptions import (ElementNotInteractableException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import JbgAbc
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_globals import JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_webdriver import (click_a_button, get_char_limit, get_prompt,
                                 is_prompt_page, is_vote_page, vote_answers,
                                 write_an_answer)
from jitb.jitb_validation import validate_pos_int


DEFAULT_CHAR_LIMIT: Final[int] = 150  # Default maximum character limit


class JbgDict(JbgAbc):
    """Jackbox Games (JBG) Dictionarium (Dict) class."""

    # Methods are listed in expected 'call order'.
    def __init__(self, ai_obj: JitbAi, username: str) -> None:
        """JbgDict ctor.

        Args:
            ai_obj:  OpenAI API interface to use in this game.
            username:  The screen name used in this game.
        """
        # Pass these values as prompt_clues arguments to jitb_webdriver functions
        self._prompt_clues = ['Write a definition for', 'Write a synonym for',
                              'Write a sentence using']
        # Pass these values as vote_clues arguments to jitb_webdriver functions
        self._vote_clues = ['Vote for your favorite definition of',
                            'Vote for your favorite synonym',
                            'Vote for your favorite sentence using']
        # Hints the page is on the Dictionarium-specific "distribute likes" page
        self._wait_like_clues = ['distribute likes']
        # Update AI system: content message
        ai_obj.change_system_content('You are a witty person trying to win the Jackbox Game'
                                     'Dictionarium. When giving definitions or synonyms, do not '
                                     'repeat the original word, '
                                     'do not provide the part of speech, do not add extra context, '
                                     'and not not add extraneous commentary. '
                                     'Respond with just the definition or synonym.')
        super().__init__(ai_obj=ai_obj, username=username)

    # Parent Class Abstract Methods
    def play(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Determine web_driver's page id and call the relevant method.

        Raises:
            RuntimeError: An error message was found in the HTML or web_driver is the wrong page.
            TypeError: An internal attribute is the wrong data type.
            ValueError: An internal attribute contains an invalid value.
        """
        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # SETUP
        self._last_page = self._current_page  # Store the last page
        self._current_page = self.id_page(web_driver=web_driver)  # Get the current page

        # PLAY
        if self._last_page != self._current_page:
            if self._current_page == JbgPageIds.VOTE:
                self.vote_answers(web_driver=web_driver)
            elif self._current_page == JbgPageIds.ANSWER:
                self.answer_prompts(web_driver=web_driver, num_answers=1)

    def select_character(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Randomize an avatar selection from the available list.

        Args:
            web_driver: The webdriver object to interact with.

        Raises:
            NotImplementedError: Dictionarium does not allow players to choose avatars.
        """
        raise NotImplementedError('Dictionarium does not allow players to choose avatars')

    def answer_prompts(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                       num_answers: int = 2) -> None:
        """Read a prompt from the web_driver, ask the AI, and submit the AI's answer.

        Args:
            web_driver: The webdriver object to interact with.
            num_answers: Optional; Number of prompts to attempt to answer.
        """
        # LOCAL VARIABLES
        prompt_text = ''  # Input prompt

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)
        validate_pos_int(num_answers, 'num_answers')

        # ANSWER THEM
        for _ in range(num_answers):
            prompt_text = self.answer_prompt(web_driver=web_driver, last_prompt=prompt_text)

    def vote_answers(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read other answers to a prompt from the web_driver, ask the AI, and submit the answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        prompt_text = ''  # The prompt text

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # VOTE IT
        while True:
            try:
                prompt_text = vote_answers(web_driver=web_driver, last_prompt=prompt_text,
                                           ai_obj=self._ai_obj, element_name='prompt',
                                           element_type=By.ID, vote_clues=self._vote_clues,
                                           clean_string=True)
            except (ElementNotInteractableException, RuntimeError,
                    StaleElementReferenceException) as err:
                Logger.error(f'Failed to vote answers with {repr(err)}')
                break  # Something went wrong so let's just leave this loop
            if not prompt_text:
                break  # Nothing got answered

    def id_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> JbgPageIds:
        """Determine what type of Jackbox Games webpage web_driver is.

        The jackbox.tv login page should be universal so start with self._is_login_page()
        when defining this method in the child class.

        Args:
            web_driver: The webdriver object to interact with.

        Returns:
            The identified page as a JbgPageIds enum.
        """
        # LOCAL VARIABLES
        current_page = JbgPageIds.UNKNOWN  # What type of page is this?

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # DETERMINE PAGE
        if self.is_vote_page(web_driver=web_driver):
            current_page = JbgPageIds.VOTE
        elif self.is_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif self._is_login_page(web_driver=web_driver):
            current_page = JbgPageIds.LOGIN
        elif self.is_waiting_likes_page(web_driver=web_driver):
            current_page = JbgPageIds.DICT_WAIT_LIKE

        # DONE
        if current_page != JbgPageIds.UNKNOWN:
            Logger.debug(f'This is a(n) {current_page.name} page!')
        return current_page

    # Public Methods (alphabetical order)
    def answer_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                      last_prompt: str) -> str:
        """Generating answers for prompts.

        Args:
            last_prompt: The last prompt that was answered.  Helps this function avoid trying to
                answer the same prompt twice.

        Returns:
            The prompt that was answered as a string.

        Raises:
            RuntimeError: The prompt wasn't answered.
        """
        # LOCAL VARIABLES
        prompt_text = ''                 # Input prompt
        answer = ''                      # Answer to the prompt
        clicked_it = False               # Keep track of whether this prompt was answered or not
        num_loops = 5                    # Number of attempts to make for a new prompt

        # INPUT VALIDATION
        if not self.is_prompt_page(web_driver=web_driver):
            raise RuntimeError('This is not a prompt page')

        # WAIT FOR IT
        for _ in range(num_loops):
            try:
                prompt_text = self.get_prompt(web_driver=web_driver)
                if prompt_text and prompt_text != last_prompt:
                    break
                time.sleep(JITB_POLL_RATE)  # Give the prompt a chance to update from the last one
            except RuntimeError as err:
                if err.args[0] == 'This is not a prompt page':
                    Logger.debug("This was a prompt page but now it's not")
                    break  # It was(?) but now it's not...
                raise err from err

        # ANSWER IT
        answer = self.generate_ai_answer(prompt=prompt_text, ai_obj=self._ai_obj,
                                         length_limit=self.get_char_limit(web_driver=web_driver))
        clicked_it = self.submit_an_answer(web_driver=web_driver, submit_text=answer)

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer the prompt')
        Logger.debug(f'Answered prompt "{prompt_text}" with "{answer}"!')
        return prompt_text

    def get_char_limit(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> int:
        """Wraps jitb_webdriver.get_char_limit with game-specific details."""
        # LOCAL VARIABLES
        char_limit = None  # Character limit for the prompt

        # GET IT
        char_limit = get_char_limit(web_driver=web_driver, element_name='charRemaining',
                                    element_type=By.CLASS_NAME)
        if char_limit is None:
            char_limit = DEFAULT_CHAR_LIMIT

        # DONE
        return char_limit

    def get_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
        """Wraps jitb_webdriver.get_prompt with game-specific details."""
        return get_prompt(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                          prompt_clues=self._prompt_clues, clean_string=True)

    def is_prompt_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_prompt_page with game-specific details."""
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._prompt_clues)

    def is_vote_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_vote_page with game-specific details."""
        return is_vote_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                            vote_clues=self._vote_clues, clean_string=True)

    def is_waiting_likes_page(self,
                              web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Determine if this is an award-likes-while-you-are-waiting page.

        Returns:
            True if this is a 'distribute likes' waiting screen, False otherwise.
        """
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._wait_like_clues)

    def submit_an_answer(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                         submit_text: str) -> bool:
        """Write an answer and click the submit button.

        Returns:
            True if an answer was written and the button was clicked, False otherwise.
        """
        # LOCAL VARIABLES
        clicked_it = False  # Indicates whether the button was clicked or not

        # SUBMIT IT
        if self.write_an_answer(web_driver=web_driver, submit_text=submit_text):
            clicked_it = click_a_button(web_driver=web_driver, button_str='SUBMIT')

        # DONE
        return clicked_it

    def write_an_answer(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                        submit_text: str) -> bool:
        """Wraps jitb_webdriver.write_an_answer with game-specific details."""
        # LOCAL VARIABLES
        element_name = 'input-text-textarea'  # The field's element name
        element_type = By.ID                  # The field's element type
        # Success or failure off sending the submit_text to the element_name
        wrote_it = write_an_answer(web_driver=web_driver, submit_text=submit_text,
                                   element_name=element_name, element_type=element_type)

        # RESPONSE
        if not wrote_it:
            Logger.error(f'Failed to write the answer "{submit_text}" for element '
                         f'"{element_name}" (of type "{element_type}")')

        # DONE
        return wrote_it
