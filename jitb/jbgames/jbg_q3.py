"""Defines the package's Jackbox Games Quiplash 3 class."""

# Standard
import random
import time
# Third Party
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import JbgAbc
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_globals import JBG_QUIP3_CHAR_NAMES, JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi


class JbgQ3(JbgAbc):
    """Jackbox Games (JBG) Quiplash 3 (Q3) class."""

    char_names = JBG_QUIP3_CHAR_NAMES  # Quiplash 3 avatar names

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
            if self._current_page == JbgPageIds.LOGIN:
                pass  # Wait for the page to change because the caller already logged in
            elif self._current_page == JbgPageIds.AVATAR and not self._avatar_chosen:
                self.select_character(web_driver=web_driver)
                self._avatar_chosen = True
            elif self._current_page == JbgPageIds.ANSWER:
                self.answer_prompts(web_driver=web_driver)
            elif self._current_page == JbgPageIds.VOTE:
                self.vote_answers(web_driver=web_driver)
            elif self._current_page == JbgPageIds.Q3_THRIP:
                self.answer_thriplash(web_driver=web_driver)

    def select_character(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Randomize an avatar selection from the available list.

        Args:
            web_driver: The webdriver object to interact with.

        Raises:
            RuntimeError: An error message was found in the HTML, this isn't the character
                selection page, or a character selection failed.
        """
        # LOCAL VARIABLES
        button_list = []     # List of web elements for the avatars
        button_entry = None  # Web element for a button
        max_loops = 20       # Maximum number of infinite loops
        clicked_it = False   # Ensure a button was pressed.

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)
        if not _is_char_selection_page(web_driver):
            raise RuntimeError('This is not the character selection page.')

        # SELECT IT
        button_list = web_driver.find_elements(By.XPATH, '//button')
        for _ in range(max_loops):
            button_entry = random.choice(button_list)
            if button_entry.accessible_name in self.char_names and button_entry.is_enabled():
                button_entry.click()
                clicked_it = True
                break

        # DONE
        if not clicked_it:
            raise RuntimeError('The JbgQ3.select_character() method failed to make a selection.')

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
            prompt_text = self._answer_prompt(web_driver=web_driver, last_prompt=prompt_text)

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
        """
        # LOCAL VARIABLES
        current_page = JbgPageIds.UNKNOWN  # What type of page is this?

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # DETERMINE PAGE
        if self._is_login_page(web_driver=web_driver):
            current_page = JbgPageIds.LOGIN
        elif _is_char_selection_page(web_driver=web_driver):
            current_page = JbgPageIds.AVATAR
        elif _is_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif _is_vote_page(web_driver=web_driver):
            current_page = JbgPageIds.VOTE
        elif _is_thrip_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.Q3_THRIP

        # DONE
        return current_page

    # Public Methods (alphabetical order)
    def answer_thriplash(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read Quiplash 3 Thriplash prompt from web_driver, ask the AI, and submit the answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # ANSWER THRIPLASH
        _answer_thriplash(web_driver=web_driver, ai_obj=self._ai_obj)

    def validate_status(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Validates the web_driver and internal attributes."""
        self._check_web_driver(web_driver=web_driver)
        self._validate_core_attributes()

    # Private Methods (alphabetical order)
    def _answer_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
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
            prompt_text = _get_prompt(web_driver)[1]
            if prompt_text and prompt_text != last_prompt:
                break
            time.sleep(JITB_POLL_RATE)  # Give the prompt a chance to update from the last one

        # ANSWER IT
        answer = self.generate_ai_answer(prompt=prompt_text, ai_obj=self._ai_obj)
        prompt_input = web_driver.find_element(By.ID, 'input-text-textarea')
        prompt_input.send_keys(answer)
        buttons = web_driver.find_elements(By.XPATH, '//button')
        for button in buttons:
            if button.text.lower() == 'SUBMIT'.lower() and button.is_enabled():
                button.click()
                clicked_it = True
                break

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer the prompt')
        Logger.debug(f'ANSWERED {prompt_text} with {answer}!')
        return prompt_text


# Private Functions (alphabetical order)
def _answer_thriplash(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                      ai_obj: JitbAi) -> None:
    """Generate answers for the Thriplash (Round 3) prompt."""
    # LOCAL VARIABLES
    prompt_text = ''    # Input prompt
    input_fields = []   # List of web elements for the three input fields
    buttons = []        # List of button web elements
    clicked_it = False  # Keep track of whether this prompt was answered or not
    gen_answers = []    # Answers generated by OpenAI
    temp_answers = []   # Temp list to reverse and then pop from

    # INPUT VALIDATION
    if not _is_thrip_prompt_page(web_driver):
        raise RuntimeError('This is not the Thriplash prompt page')

    # ANSWER IT
    prompt_text = _get_prompt(web_driver=web_driver)[-1]
    gen_answers = ai_obj.generate_thriplash(prompt_text)
    temp_answers = gen_answers[::-1]  # Reverse it so they can be pop()d
    input_fields = web_driver.find_elements(By.ID, 'input-text-textarea')

    # SUBMIT IT
    for input_field in input_fields:
        input_field.send_keys(temp_answers.pop())
    buttons = web_driver.find_elements(By.XPATH, '//button')
    for button in buttons:
        if button.text.lower() == 'SUBMIT'.lower() and button.is_enabled():
            button.click()
            clicked_it = True
            break

    # DONE
    if not clicked_it:
        raise RuntimeError('Did not answer the Thriplash prompt')
    Logger.debug(f'ANSWERED THRIPLASH {prompt_text} with: {", ".join(gen_answers)}!')


def _get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> list:
    """Wait for the prompt element id to show and then return.

    Returns:
        The game prompt, split by newline, into a list.
    """
    # LOCAL VARIABLES
    prompt_text = []  # The prompt's text split by newline

    # WAIT FOR IT
    element = web_driver.find_element(By.ID, 'prompt')
    prompt_text = element.text.split('\n')

    # DONE
    if not prompt_text:
        raise RuntimeError('Did not detect any prompts')
    return prompt_text


def _is_char_selection_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this the character selection screen.

    Returns:
        True if this is the 'Select your character' screen, False otherwise.
    """
    # LOCAL VARIABLES
    char_selection = False  # Prove this true
    prompt = None           # Web Element for the characters prompt

    # IS IT?
    try:
        prompt = web_driver.find_element(By.ID, 'charactersPrompt')
        if 'Select your character'.lower() in prompt.text.lower():
            char_selection = True
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not the character selection page

    # DONE
    return char_selection


def _is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this a round 1 or 2 prompt page.

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    prompt_page = False                           # Prove this true
    temp_we = None                                # Temporary web element variable
    prompts = ['Prompt 1 of 2', 'Prompt 2 of 2']  # Prompt needles

    # IS IT?
    try:
        temp_we = web_driver.find_element(By.ID, 'prompt')
        for prompt in prompts:
            if temp_we.text.startswith(prompt):
                prompt_page = True  # If we made it here, it's a prompt page
                break
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return prompt_page


def _is_thrip_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is the Thriplash (Round 3) prompt page.

    Returns:
        True if this is the Thriplash (Round 3) prompt page, False otherwise.
    """
    # LOCAL VARIABLES
    prompt_page = False      # Prove this true
    temp_we = None           # Temporary web element variable
    prompt = 'Final prompt'  # Prompt needle

    # IS IT?
    try:
        temp_we = web_driver.find_element(By.ID, 'prompt')
        if temp_we.text.lower().startswith(prompt.lower()):
            prompt_page = True  # If we made it here, it's a prompt page
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a Thriplash prompt page

    # DONE
    return prompt_page


def _is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this a round 1 or 2 vote page.

    Returns:
        True if this is a regular vote screen, False otherwise.
    """
    # LOCAL VARIABLES
    vote_page = False                  # Prove this true
    temp_we = None                     # Temporary web element variable
    prompt = 'Vote for your favorite'  # Prompt needles

    # IS IT?
    try:
        temp_we = web_driver.find_element(By.ID, 'prompt')
        if prompt.lower() in temp_we.text.lower():
            vote_page = True  # If we made it here, it's a vote page
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a vote page

    # DONE
    return vote_page


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
    num_loops = 5       # Number of attempts to make for a new prompt
    choice_list = []    # List of possible answers
    favorite = ''       # OpenAI's favorite answer
    button_dict = {}    # Sanitized text are the keys and actual button text are the values
    temp_text = ''      # Temp sanitized button text

    # WAIT FOR IT
    for _ in range(num_loops):
        try:
            prompt_text = _get_prompt(web_driver)[0]
            if prompt_text and prompt_text != last_prompt:
                break
            if not _is_vote_page(web_driver):
                prompt_text = ''
                break
            time.sleep(JITB_POLL_RATE)
        except NoSuchElementException:
            prompt_text = ''  # Must have been the last prompt to vote

    # ANSWER IT
    if prompt_text and prompt_text != last_prompt:
        buttons = web_driver.find_elements(By.XPATH, '//button')
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
    if button:
        Logger.debug(f'VOTED {favorite} for {prompt_text}!')
    return prompt_text
