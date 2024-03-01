"""Defines the package's Jackbox Games Quiplash 2 class."""

# Standard
from typing import Final
import time
# Third Party
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import JbgAbc
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_globals import JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_selenium import get_buttons, get_sub_buttons, get_web_element, get_web_element_text


# A 'needle' to help differentiate between regular prompts and the Round 3 'Last Lash' prompt
NORMAL_PROMPT_NEEDLE: Final[str] = 'SEND SAFETY QUIP'  # This does not appears on the Last Lash
# A 'needle' to help differentiate a Comic Lash from the other Round 3 'Last Last' examples.
COMIC_LAST_NEEDLE: Final[str] = '   SEND'  # Only the Comic Last Lash seems to get this


class JbgQ2(JbgAbc):
    """Jackbox Games (JBG) Quiplash 2 (Q2) class."""

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
            if self._current_page == JbgPageIds.ANSWER:
                self.answer_prompts(web_driver=web_driver)
            elif self._current_page == JbgPageIds.Q2_LAST:
                self.answer_last_lash(web_driver=web_driver)
            elif self._current_page == JbgPageIds.VOTE:
                self.vote_answers(web_driver=web_driver)

    def select_character(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Randomize an avatar selection from the available list.

        Args:
            web_driver: The webdriver object to interact with.

        Raises:
            NotImplementedError: Quiplash 2 does not allow players to choose avatars.
        """
        raise NotImplementedError('Quiplash 2 does not allow players to choose avatars')

    def answer_last_lash(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read a prompt from the web_driver, ask the AI, and submit the AI's answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # ANSWER THEM
        _answer_last_lash(web_driver=web_driver, ai_obj=self._ai_obj)

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
            prompt_text = _answer_prompt(web_driver=web_driver, last_prompt=prompt_text,
                                         ai_obj=self._ai_obj)

    def vote_answers(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read other answers to a prompt from the web_driver, ask the AI, and submit the answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        prompt_text = ''  # The prompt text

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)
        if not _is_vote_page(web_driver=web_driver):
            raise RuntimeError('This is not a voting page.')

        # VOTE IT
        while True:
            prompt_text = _vote_answer(web_driver=web_driver, last_prompt=prompt_text,
                                       ai_obj=self._ai_obj)
            if not prompt_text:
                break
            if not _is_vote_page(web_driver):
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
        if self._is_login_page(web_driver=web_driver):
            current_page = JbgPageIds.LOGIN
        elif _is_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif _is_last_lash_page(web_driver=web_driver):
            current_page = JbgPageIds.Q2_LAST
        elif _is_vote_page(web_driver=web_driver):
            current_page = JbgPageIds.VOTE

        # DONE
        if current_page != JbgPageIds.UNKNOWN:
            Logger.debug(f'This is a(n) {current_page.name} page!')
        return current_page

    # Public Methods (alphabetical order)
    def validate_status(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Validates the web_driver and internal attributes."""
        self._check_web_driver(web_driver=web_driver)
        self._validate_core_attributes()

    # Private Methods (alphabetical order)
    # N/A


# Public Functions (alphabetical order)
def get_last_lash_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
    """Get the Last Lash prompt text from the state-answer-question web element.

    Do not use this for the Round 1 or 2.

    Args:
        web_driver: The web driver to get the prompt from.

    Returns:
        The game's Last Lash prompt text.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a prompt page.
        TypeError: Bad data type.
        ValueError: Invalid by value.
    """
    # LOCAL VARIABLES
    needle = 'state-answer-question'  # Web element id to find in web_driver
    prompt_text = ''                  # The prompt's text as a string
    prompt_list = []                  # Use this to cleanup the text

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)
    if not _is_last_lash_page(web_driver):
        raise RuntimeError('This is not a Last Lash prompt page')

    # GET IT
    try:
        prompt_text = get_web_element_text(web_driver=web_driver, by_arg=By.ID, value=needle)
    except (RuntimeError, TypeError, ValueError) as err:
        Logger.debug(f'get_last_lash_prompt() call to get_web_element_text() failed with {err}')
        raise RuntimeError(f'The call to get_web_element_text() for the {needle} element value '
                           f'failed with {repr(err)}') from err
    else:
        if prompt_text is None:
            raise RuntimeError(f'Unable to locate the {needle} element value')
        if not prompt_text:
            raise RuntimeError(f'Did not detect any text using the {needle} element value')

    # CLEAN IT UP
    prompt_list = prompt_text.split('\n')[:2]  # Testing shows we only care about the first two
    prompt_text = ' '.join(prompt_list)  # Put it back together into one string

    # DONE
    return prompt_text


def get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
    """Get the prompt text from the question-text web element.

    Do not use this for the Round 3 Last Lash prompt because the Last Lash prompt
    commonly has multiple lines.

    Args:
        web_driver: The web driver to get the prompt from.

    Returns:
        The game prompt text.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a prompt page.
        TypeError: Bad data type.
        ValueError: Invalid by value.
    """
    # LOCAL VARIABLES
    needle = 'question-text'  # Web element id to find in web_driver
    prompt_text = ''          # The prompt's text as a string

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)
    if not _is_prompt_page(web_driver, verify_regular=True):
        raise RuntimeError('This is not a prompt page')

    # GET IT
    try:
        prompt_text = get_web_element_text(web_driver=web_driver, by_arg=By.ID, value=needle)
    except (RuntimeError, TypeError, ValueError) as err:
        raise RuntimeError(f'The call to get_web_element_text() for the {needle} element value '
                           f'failed with {repr(err)}') from err
    else:
        if prompt_text is None:
            raise RuntimeError(f'Unable to locate the {needle} element value')
        if not prompt_text:
            raise RuntimeError(f'Did not detect any text using the {needle} element value')

    # DONE
    return prompt_text


def get_vote_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
    """Get the vote text from various web elements, assemble them, and return it.

    Combinations of vote text could appear in one or more of the following web elements:
        - question-text-alt
        - question-text
        - vote-text

    Args:
        web_driver: The web driver to get the prompt from.

    Returns:
        The game vote text.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a vote page.
        TypeError: Bad data type.
        ValueError: Invalid by value.
    """
    # LOCAL VARIABLES
    needle = 'state-vote'  # Web element to look for
    vote_text = ''         # The full vote prompt

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)
    if not _is_vote_page(web_driver):
        raise RuntimeError('This is not a vote page')

    # GET THEM
    try:
        vote_text = get_web_element_text(web_driver=web_driver, by_arg=By.ID, value=needle)
    except (RuntimeError, TypeError, ValueError) as err:
        raise RuntimeError(f'The call to get_web_element_text() for the {needle} element value '
                           f'failed with {repr(err)}') from err
    else:
        if vote_text is None:
            raise RuntimeError(f'Unable to locate the {needle} element value')
        if not vote_text:
            raise RuntimeError(f'Did not detect any text using the {needle} element value')

    # DONE
    return vote_text


# Private Functions (alphabetical order)
def _answer_last_lash(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                      ai_obj: JitbAi) -> None:
    """Generate an answer for the Last Lash (Round 3) prompt."""
    # LOCAL VARIABLES
    prompt_text = ''    # Input prompt
    gen_answer = ''     # Answer generated by OpenAI
    input_field = None  # Web element for the input field
    buttons = []        # List of button web elements
    clicked_it = False  # Keep track of whether this prompt was answered or not
    # Replacement prompt when a Comic Lash is detected
    comic_text = 'The other players are being shown a picture you can not see. ' \
        + 'It is a generic web comic with the text removed from the speech bubble ' \
        + 'of the last panel.  Give an answer that is generic enough to ' \
        + 'work as funny/quirky text for such an empty speech bubble.'

    # INPUT VALIDATION
    if not _is_last_lash_page(web_driver=web_driver):
        raise RuntimeError('This is not the Last Lash prompt page')

    # ANSWER IT
    # prompt_text = get_prompt(web_driver=web_driver)
    prompt_text = get_last_lash_prompt(web_driver=web_driver)
    if COMIC_LAST_NEEDLE.lower() in prompt_text.lower():
        Logger.debug(f'It appears we have encountered a Comic Last because the "{prompt_text}" '
                     f'is being repaced with "{comic_text}"')
        prompt_text = comic_text
    gen_answer = ai_obj.generate_answer(prompt_text)
    input_field = get_web_element(web_driver, By.ID, 'quiplash-answer-input')

    # SUBMIT IT
    if input_field:
        input_field.send_keys(gen_answer)
        buttons = get_buttons(web_driver)
        for button in buttons:
            if 'SEND'.lower() in button.text.lower() and button.is_enabled():
                button.click()
                clicked_it = True
                break

    # DONE
    if not clicked_it:
        raise RuntimeError('Did not answer the Last Lash prompt')
    Logger.debug(f'Answered Last Lash prompt "{prompt_text}" with: "{gen_answer}"!')


def _answer_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   last_prompt: str, ai_obj: JitbAi) -> str:
    """Generating answers for prompts.

    Args:
        last_prompt: The last prompt that was answered.  Helps this function avoid trying to
            answer the same prompt twice.
        ai_obj: Query object to get AI-generated answers.

    Returns:
        The prompt that was answered as a string.

    Raises:
        RuntimeError: The prompt wasn't answered.
    """
    # LOCAL VARIABLES
    prompt_text = ''     # Input prompt
    answer = ''          # Answer to the prompt
    prompt_input = None  # Web element for the prompt input field
    buttons = []         # Web element for the submit button
    clicked_it = False   # Keep track of whether this prompt was answered or not
    num_loops = 5        # Number of attempts to make for a new prompt

    # INPUT VALIDATION
    if not _is_prompt_page(web_driver):
        raise RuntimeError('This is not a prompt page')

    # WAIT FOR IT
    for _ in range(num_loops):
        try:
            prompt_text = get_prompt(web_driver=web_driver)
            if prompt_text and prompt_text != last_prompt:
                break
            time.sleep(JITB_POLL_RATE)  # Give the prompt a chance to update from the last one
        except RuntimeError as err:
            if err.args[0] == 'This is not a prompt page':
                break  # It was(?) but now it's not...
            else:
                raise err from err

    # ANSWER IT
    answer = ai_obj.generate_answer(prompt=prompt_text)
    prompt_input = get_web_element(web_driver, By.ID, 'quiplash-answer-input')
    if prompt_input:
        prompt_input.send_keys(answer)
        buttons = get_buttons(web_driver)
        for button in buttons:
            if 'SEND'.lower() in button.text.lower() and button.is_enabled():
                button.click()
                clicked_it = True
                break

    # DONE
    if not clicked_it:
        raise RuntimeError('Did not answer the prompt')
    Logger.debug(f'Answered prompt "{prompt_text}" with "{answer}"!')
    return prompt_text


def _is_last_lash_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is the Round 3 Last Lash prompt page.

    One (seemingly) easy way to differentiate between the Last Lash prompt and the Round 1 & 2
    prompts is that you can't Safety Quip on the Last Lash.  This function's logic is:
    If web_driver is a prompt_page and 'SEND SAFETY QUIP' is *not* in the text, it's a
    Last Lash prompt.

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    last_lash_page = False  # Prove this true if you can

    # IS IT?
    if _is_prompt_page(web_driver=web_driver, verify_regular=False) \
            and not _is_prompt_page(web_driver=web_driver, verify_regular=True):
        last_lash_page = True

    # DONE
    return last_lash_page


def _is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    verify_regular: bool = True) -> bool:
    """Determine if this is a prompt page.

    Args:
        web_driver: The web driver to check.
        verify_regular: Optional; If True, will verify the NORMAL_PROMPT_NEEDLE exists in the
            output.

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'state-answer-question'  # The web element value to search for
    prompt_page = False                     # Prove this true
    temp_we = None                          # Temporary web element variable
    temp_text = ''                          # Text from the web element

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text:
            prompt_page = True  # If we made it here, it's a prompt page
            if verify_regular and NORMAL_PROMPT_NEEDLE.lower() not in temp_text.lower():
                prompt_page = False
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return prompt_page


def _is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this a round 1 or 2 vote page.

    Returns:
        True if this is a regular vote screen, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'vote-text'              # The web element value to search for
    vote_page = False                       # Prove this true
    temp_we = None                          # Temporary web element variable
    prompt = 'Which one do you like more?'  # Prompt needles
    temp_text = ''                          # Temp prompt text

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text and prompt.lower() in temp_text.lower():
            vote_page = True  # If we made it here, it's a vote page
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a vote page

    # DONE
    return vote_page


def _validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Validate a web driver."""
    if not web_driver:
        raise TypeError('Web driver can not be of type None')
    if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
        raise TypeError(f'Invalid web_driver data type of {type(web_driver)}')


def _vote_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                 last_prompt: str, ai_obj: JitbAi) -> str:
    """Generate votes for other players prompts.

    Args:
        last_prompt: The last prompt that was answered.  Helps this function avoid trying to
            answer the same prompt twice.

    Returns:
        The prompt that was answered as a string.

    Raises:
        RuntimeError: The prompt wasn't answered.
    """
    # LOCAL VARIABLES
    prompt_text = ''    # Input prompt
    buttons = []        # List of web elements for the buttons
    button = None       # The web element of the button to click
    clicked_it = False  # Keep track of whether this prompt was answered or not
    num_loops = 5       # Number of attempts to wait for a new prompt
    choice_list = []    # List of possible answers
    favorite = ''       # OpenAI's favorite answer
    button_dict = {}    # Sanitized text are the keys and actual button text are the values
    temp_text = ''      # Temp sanitized button text

    # WAIT FOR IT
    for _ in range(num_loops):
        try:
            # prompt_text = get_prompt(web_driver=web_driver)[0]
            prompt_text = get_vote_text(web_driver=web_driver)
            if prompt_text and prompt_text != last_prompt:
                break
            if not _is_vote_page(web_driver):
                prompt_text = ''
                break
            time.sleep(JITB_POLL_RATE)
        except NoSuchElementException:
            prompt_text = ''  # Must have been the last prompt to vote
        except RuntimeError as err:
            if err.args[0] == 'This is not a vote page':
                break  # It was(?) but now it's not...
            else:
                raise err from err

    # ANSWER IT
    if prompt_text and prompt_text != last_prompt:
        buttons = get_sub_buttons(web_driver=web_driver, sub_by=By.ID, sub_value='quiplash-vote')
        # Form the selection list
        for button in buttons:
            if button.text:
                temp_text = button.text.strip('\n')
                button_dict[temp_text] = button.text
                choice_list.append(temp_text)
        # Ask the AI
        favorite = ai_obj.vote_favorite(prompt=prompt_text, answers=choice_list)
        for button in buttons:
            if button and button.text == button_dict[favorite] and button.is_enabled():
                button.click()
                clicked_it = True
                break
    else:
        prompt_text = ''  # Nothing got answered

    # DONE
    if prompt_text and prompt_text != last_prompt and not clicked_it:
        raise RuntimeError('Did not vote an answer')
    if clicked_it:
        temp_text = prompt_text.replace('\n', ' ')
        Logger.debug(f'Voted "{favorite}" for "{temp_text}"!')
    return prompt_text
