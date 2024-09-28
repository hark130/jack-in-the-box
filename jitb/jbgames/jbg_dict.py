"""Defines the package's Jackbox Games Dictionarium class."""

# Standard
from string import digits, punctuation, whitespace
from typing import Final, List
import time
# Third Party
from selenium.common.exceptions import (ElementNotInteractableException, NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import JbgAbc
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_globals import JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_misc import clean_up_string
from jitb.jitb_openai import JitbAi
from jitb.jitb_selenium import get_buttons, get_web_element, get_web_element_text
from jitb.jitb_webdriver import (click_a_button, get_button_choices, get_char_limit, get_prompt,
                                 get_vote_text, is_prompt_page, is_vote_page, vote_answers,
                                 write_an_answer)


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
        if not isinstance(num_answers, int):
            raise TypeError(f'Invalid data type of {type(num_answers)} for the num_answers')
        if num_answers < 1:
            raise ValueError(f'Invalid value of {num_answers} detected for num_answers')

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
            prompt_text = vote_answers(web_driver=web_driver, last_prompt=prompt_text,
                                       ai_obj=self._ai_obj, element_name='prompt',
                                       element_type=By.ID, vote_clues=self._vote_clues,
                                       clean_string=True)
            if not prompt_text:
                break
            if not self.is_vote_page(web_driver=web_driver):
                break

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
        char_limit = DEFAULT_CHAR_LIMIT  # Maximum character limit

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
        """Determine if this is this a award-likes-while-you-are-waiting page.

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

    def validate_status(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Validates the web_driver and internal attributes.

        Args:
            web_driver: The webdriver object to interact with.
        """
        self._check_web_driver(web_driver=web_driver)
        self._validate_core_attributes()

    def write_an_answer(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                        submit_text: str) -> bool:
        """Wraps jitb_webdriver.write_an_answer with game-specific details."""
        return write_an_answer(web_driver=web_driver, submit_text=submit_text,
                               element_name='input-text-textarea', element_type=By.ID)


# Public Functions (alphabetical order)
# def get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                check_needles: bool = True) -> str:
#     """Get the prompt text from the question-text web element.

#     Strips newlines from the prompt text.

#     Args:
#         web_driver: The web driver to get the prompt from.
#         check_needles: Optional; If True, will verify prompt needles are found.

#     Returns:
#         The game prompt text.

#     Raises:
#         RuntimeError: No prompts found or web_driver isn't a prompt page.
#         TypeError: Bad data type.
#         ValueError: Invalid by value.
#     """
#     # LOCAL VARIABLES
#     needle = 'prompt'  # Web element id to find in web_driver
#     prompt_text = ''   # The prompt's text as a string

#     # INPUT VALIDATION
#     _validate_web_driver(web_driver=web_driver)
#     if not  _is_prompt_page(web_driver, check_needles=check_needles):
#         raise RuntimeError('This is not a prompt page')

#     # GET IT
#     try:
#         prompt_text = get_web_element_text(web_driver=web_driver, by_arg=By.ID, value=needle)

#         # TESTING
#         test_value = get_web_element_text(web_driver=web_driver, by_arg=By.CLASS_NAME,
#                                           value='charRemaining')
#         print(f'TEST VALUE: {test_value} (of type {type(test_value)})')  # DEBUGGING
#     except (RuntimeError, TypeError, ValueError) as err:
#         raise RuntimeError(f'The call to get_web_element_text() for the {needle} element value '
#                            f'failed with {repr(err)}') from err
#     else:
#         if prompt_text is None:
#             raise RuntimeError(f'Unable to locate the {needle} element value')
#         if not prompt_text:
#             raise RuntimeError(f'Did not detect any text using the {needle} element value')

#     # DONE
#     return clean_up_string(prompt_text)


# def get_vote_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                   check_needles: bool = True) -> str:
#     """Get the vote text from various web elements, assemble them, and return it.

#     Args:
#         web_driver: The web driver to get the prompt from.
#         check_needles: Optional; If True, will verify prompt needles are found.

#     Returns:
#         The game vote text.

#     Raises:
#         RuntimeError: No prompts found or web_driver isn't a vote page.
#         TypeError: Bad data type.
#         ValueError: Invalid by value.
#     """
#     # LOCAL VARIABLES
#     needle = 'prompt'  # Web element to look for
#     vote_text = ''     # The full vote prompt

#     # INPUT VALIDATION
#     _validate_web_driver(web_driver=web_driver)
#     if not _is_vote_page(web_driver, check_needles=check_needles):
#         raise RuntimeError('This is not a vote page')

#     # GET THEM
#     try:
#         vote_text = get_web_element_text(web_driver=web_driver, by_arg=By.ID, value=needle)
#     except (RuntimeError, TypeError, ValueError) as err:
#         raise RuntimeError(f'The call to get_web_element_text() for the {needle} element value '
#                            f'failed with {repr(err)}') from err
#     else:
#         if vote_text is None:
#             raise RuntimeError(f'Unable to locate the {needle} element value')
#         if not vote_text:
#             raise RuntimeError(f'Did not detect any text using the {needle} element value')

#     # DONE
#     return vote_text


# # Private Functions (alphabetical order)
# def _click_a_button(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                     button_str: str) -> bool:
#     """Standardize the way buttons are clicked.

#     Args:
#         web_driver: The webdriver object to interact with.
#         button_str: The substring to search for within the button text.

#     Returns:
#         True if a button was clicked, false otherwise.
#     """
#     # LOCAL VARIABLES
#     buttons = get_buttons(web_driver=web_driver)  # All the buttons from web_driver
#     clicked_it = False                            # Return value

#     # CLICK IT
#     for button in buttons:
#         # Find it
#         if button_str.lower() in button.text.lower() and button.is_enabled():
#             # Click it
#             try:
#                 button.click()
#             except ElementNotInteractableException as err:
#                 Logger.debug(f'Failed to click "{button.text}" with {repr(err)}')
#             else:
#                 clicked_it = True
#             finally:
#                 break  # pylint: disable = lost-exception

#     # DONE
#     return clicked_it


# def _is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                     check_needles: bool = True) -> bool:
#     """Determine if this is a prompt page.

#     Args:
#         web_driver: The web driver to check.
#         check_needles: Optional; If True, will verify prompt needles are found.

#     Returns:
#         True if this is a regular prompt screen, False otherwise.
#     """
#     # LOCAL VARIABLES
#     element_name = 'prompt'  # The web element value to search for
#     prompt_page = False      # Prove this true
#     temp_text = ''           # Text from the web element
#     # List of prompt needles from various Joke Boat voting screens
#     prompts = ['Write a definition for', 'Write a synonym for', 'Write a sentence using']

#     # IS IT?
#     try:
#         temp_text = get_web_element_text(web_driver, By.ID, element_name)
#         if temp_text:
#             if check_needles:
#                 for prompt in prompts:
#                     if prompt.lower() in temp_text.lower():
#                         prompt_page = True  # If we made it here, it's a prompt page
#                         break  # Found one.  Stop looking.
#             else:
#                 prompt_page = True  # Far enough
#     except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
#         pass  # Not a prompt page

#     # DONE
#     return prompt_page


# def _is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                   check_needles: bool = True) -> bool:
#     """Determine if this is this a vote page.

#     Args:
#         web_driver: The web driver to check.
#         check_needles: Optional; If True, will verify vote needles are found.

#     Returns:
#         True if this is a regular vote screen, False otherwise.
#     """
#     # LOCAL VARIABLES
#     element_name = 'prompt'  # The web element value to search for
#     vote_page = False        # Prove this true
#     temp_text = ''           # Temp prompt text
#     # List of prompt needles from various Joke Boat voting screens
#     prompts = ['Vote for your favorite definition of', 'Vote for your favorite synonym',
#                'Vote for your favorite sentence using']

#     # IS IT?
#     try:
#         temp_text = get_web_element_text(web_driver, By.ID, element_name)
#         if temp_text:
#             temp_text = clean_up_string(dirty_string=temp_text)  # Remove newlines
#             if check_needles:
#                 for prompt in prompts:
#                     if prompt.lower() in temp_text.lower():
#                         vote_page = True  # If we made it here, it's a vote page
#                         break  # Found one.  Stop looking.
#             else:
#                 vote_page = True  # Far enough
#     except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
#         pass  # Not a vote page

#     # DONE
#     return vote_page


# def _is_waiting_likes_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                            check_needles: bool = True) -> bool:
#     """Determine if this is this a award-likes-while-you-are-waiting page.

#     Args:
#         web_driver: The web driver to check.
#         check_needles: Optional; If True, will verify vote needles are found.

#     Returns:
#         True if this is a 'distribute likes' waiting screen, False otherwise.
#     """
#     # LOCAL VARIABLES
#     element_name = 'prompt'  # The web element value to search for
#     likes_page = False       # Prove this true
#     temp_text = ''           # Temp prompt text
#     # List of prompt needles from various Joke Boat voting screens
#     prompts = ['distribute likes']

#     # IS IT?
#     try:
#         temp_text = get_web_element_text(web_driver, By.ID, element_name)
#         if temp_text:
#             temp_text = clean_up_string(dirty_string=temp_text)  # Remove newlines
#             if check_needles:
#                 for prompt in prompts:
#                     if prompt.lower() in temp_text.lower():
#                         likes_page = True  # If we made it here, it's a vote page
#                         break  # Found one.  Stop looking.
#             else:
#                 likes_page = True  # Far enough
#     except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
#         pass  # Not a vote page

#     # DONE
#     return likes_page


# def _submit_an_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                       field_str: str, submit_text: str) -> bool:
#     """Standardize the way keys are sent to text fields.

#     Args:
#         web_driver: The webdriver object to interact with.
#         field_str: The name of the prompt to fill.

#     Returns:
#         True if successful, false otherwise.
#     """
#     # LOCAL VARIABLES
#     sent_it = False  # Return value

#     # SUBMIT IT
#     prompt_input = get_web_element(web_driver, By.ID, field_str)
#     if prompt_input:
#         try:
#             prompt_input.send_keys(submit_text)
#         except ElementNotInteractableException as err:
#             Logger.debug(f'Failed to submit "{submit_text}" into "{field_str}" with {repr(err)}')
#         else:
#             sent_it = True
#     else:
#         Logger.debug(f'Unable to locate "{field_str}" by ID')

#     # DONE
#     return sent_it


# def _validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
#     """Validate a web driver."""
#     if not web_driver:
#         raise TypeError('Web driver can not be of type None')
#     if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
#         raise TypeError(f'Invalid web_driver data type of {type(web_driver)}')


# # pylint: disable = too-many-branches
# def _vote_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
#                  last_prompt: str, ai_obj: JitbAi, check_needles: bool = True) -> str:
#     """Generate votes for other players prompts.

#     Args:
#         web_driver: The web driver to check.
#         last_prompt: The last prompt that was answered.  Helps this function avoid trying to
#             answer the same prompt twice.
#         ai_obj: The JitbAi object to use.
#         check_needles: Optional; If True, will verify vote needles are found.

#     Returns:
#         The prompt that was answered as a string.

#     Raises:
#         RuntimeError: The prompt wasn't answered.
#     """
#     # LOCAL VARIABLES
#     prompt_text = ''    # Input prompt
#     buttons = []        # List of web elements for the buttons
#     button = None       # The web element of the button to click
#     clicked_it = False  # Keep track of whether this prompt was answered or not
#     num_loops = 5       # Number of attempts to wait for a new prompt
#     choice_list = []    # List of possible answers
#     favorite = ''       # OpenAI's favorite answer
#     button_dict = {}    # Sanitized text are the keys and actual button text are the values
#     temp_text = ''      # Temp sanitized button text

#     # WAIT FOR IT
#     for _ in range(num_loops):
#         try:
#             # prompt_text = get_prompt(web_driver=web_driver)[0]
#             prompt_text = get_vote_text(web_driver=web_driver, check_needles=check_needles)
#             if prompt_text and prompt_text != last_prompt:
#                 break
#             if not _is_vote_page(web_driver, check_needles=check_needles):
#                 prompt_text = ''
#                 break
#             time.sleep(JITB_POLL_RATE / 2)  # Less sleep, faster voting
#         except NoSuchElementException:
#             prompt_text = ''  # Must have been the last prompt to vote
#         except RuntimeError as err:
#             if err.args[0] == 'This is not a vote page':
#                 break  # It was(?) but now it's not...
#             raise err from err

#     # ANSWER IT
#     if prompt_text and prompt_text != last_prompt:
#         # buttons = get_sub_buttons(web_driver=web_driver, sub_by=By.ID, sub_value='quiplash-vote')
#         buttons = get_buttons(web_driver=web_driver)
#         buttons = [button for button in buttons if button.is_enabled()]
#         # Form the selection list
#         for button in buttons:
#             if button.text:
#                 temp_text = button.text.strip('\n')
#                 button_dict[temp_text] = button.text
#                 choice_list.append(temp_text)
#         # Ask the AI
#         favorite = ai_obj.vote_favorite(prompt=prompt_text, answers=choice_list)
#         # Click it
#         clicked_it = _click_a_button(web_driver=web_driver, button_str=button_dict[favorite])
#     else:
#         prompt_text = ''  # Nothing got answered

#     # DONE
#     if prompt_text and prompt_text != last_prompt and not clicked_it:
#         raise RuntimeError('Did not vote an answer')
#     if clicked_it:
#         temp_text = prompt_text.replace('\n', ' ')
#         Logger.debug(f'Chose "{favorite}" for "{temp_text}"!')
#     return prompt_text
# # pylint: enable = too-many-branches
