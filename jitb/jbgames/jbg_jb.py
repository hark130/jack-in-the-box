"""Defines the package's Jackbox Games Joke Boat class."""

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
from jitb.jitb_openai import JitbAi
from jitb.jitb_selenium import get_buttons, get_web_element, get_web_element_text


# A 'needle' to help identify the catchphrase page
CATCHPHRASE_PROMPT_NEEDLE: Final[str] = 'catchphrase'
# A 'needle' to help identify the joke topic page
JOKE_TOPIC_PROMPT_NEEDLE: Final[str] = 'Write as many topics as you can'
# Known joke topic prompts to use as keys in the dictionary of answers
KNOWN_JOKE_TOPICS: Final[List[str]] = ['A BRAND', 'AN OBJECT', 'A FOOD', 'A LOCATION',
                                       'A PLURAL NOUN', 'AN ANIMAL', 'A PERSON’S NAME']


class JbgJb(JbgAbc):
    """Jackbox Games (JBG) Joke Boat (JB) class."""

    # Methods are listed in expected 'call order'.
    def __init__(self, ai_obj: JitbAi, username: str) -> None:
        """JbgAbc ctor.

        Args:
            ai_obj:  OpenAI API interface to use in this game.
            username:  The screen name used in this game.
        """
        super().__init__(ai_obj=ai_obj, username=username)
        self._joke_topic_dict = {}     # Dictionary of joke topics (see: KNOWN_JOKE_TOPICS)
        self._joke_topic_init = False  # Joke Topic Dict prepopulated
        self._num_requests = 0         # Number of Joke Topic AI requests; Cap it at 3

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
        if not self._joke_topic_init:
            self._populate_joke_topic_dict(num_requests=1)  # Make this 2 when JitbAi has context

        # PLAY
        if self._last_page != self._current_page:
            if self._current_page == JbgPageIds.VOTE:
                self.vote_answers(web_driver=web_driver)
            elif self._current_page == JbgPageIds.JB_TOPIC:
                self.enter_vote_topics(web_driver=web_driver)
            elif self._current_page == JbgPageIds.ANSWER:
                self.answer_prompts(web_driver=web_driver, num_answers=1)
            elif self._current_page == JbgPageIds.JB_PERFORM:
                self.skip_perform(web_driver=web_driver)
            elif self._current_page == JbgPageIds.JB_CATCH:
                self.choose_catchphrase(web_driver=web_driver)

    def select_character(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Randomize an avatar selection from the available list.

        Args:
            web_driver: The webdriver object to interact with.

        Raises:
            NotImplementedError: Joke Boat does not allow players to choose avatars.
        """
        raise NotImplementedError('Joke Boat does not allow players to choose avatars')

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

        Returns:
            The identified page as a JbgPageIds enum.
        """
        # LOCAL VARIABLES
        current_page = JbgPageIds.UNKNOWN  # What type of page is this?

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # DETERMINE PAGE
        if _is_vote_page(web_driver=web_driver):
            current_page = JbgPageIds.VOTE
        elif _is_joke_topic_page(web_driver=web_driver):
            current_page = JbgPageIds.JB_TOPIC
        elif _is_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif _is_perform_page(web_driver=web_driver):
            current_page = JbgPageIds.JB_PERFORM
        elif _is_catchphrase_page(web_driver=web_driver):
            current_page = JbgPageIds.JB_CATCH
        elif self._is_login_page(web_driver=web_driver):
            current_page = JbgPageIds.LOGIN

        # DONE
        if current_page != JbgPageIds.UNKNOWN:
            Logger.debug(f'This is a(n) {current_page.name} page!')
        return current_page

    # Public Methods (alphabetical order)
    def choose_catchphrase(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Choose the catchphrase for the game.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        prompt_text = ''  # Input prompt

        # INPUT VALIDATION
        if not _is_catchphrase_page(web_driver=web_driver):
            raise RuntimeError('This is not the catchphrase page')

        # CHOOSE IT
        prompt_text = _vote_answer(web_driver=web_driver, last_prompt=prompt_text,
                                   ai_obj=self._ai_obj, check_needles=False)

    def enter_vote_topics(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Enter some topics until you can't anymore.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        answer = ''       # AI answer
        prompt_text = ''  # Input prompt
        temp_key = ''     # Answer dict key

        # ENTER AS MANY TOPICS AS YOU CAN
        while _is_joke_topic_page(web_driver=web_driver):
            # RESET TEMP VARIABLES
            answer = ''       # AI answer
            prompt_text = ''  # Input prompt
            temp_key = ''     # Answer dict key
            # GET PROMPT
            prompt_text = get_prompt(web_driver=web_driver, check_needles=False)
            try:
                temp_key = prompt_text.split('\n')[1]
            except IndexError:
                time.sleep(JITB_POLL_RATE)  # Give the page a chance to update
                continue  # We're probably not on a Joke Topic page anymore...
            # ANSWER IT
            if temp_key not in self._joke_topic_dict or not self._joke_topic_dict[temp_key]:
                Logger.debug(f'{temp_key} was requested as a vote topic but not present')
                if not self._gen_vote_topics(key=temp_key):
                    break  # There's no more requests to be had
            prompt_input = get_web_element(web_driver, By.ID, 'input-text-textarea')
            if prompt_input and self._joke_topic_dict[temp_key]:
                answer = self._joke_topic_dict[temp_key].pop()
                prompt_input.send_keys(answer)
                clicked_it = _click_a_button(web_driver=web_driver, button_str='SUBMIT')
            time.sleep(JITB_POLL_RATE)  # Give the page a chance to update

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer any vote topics')

    def skip_perform(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Tell Joke Bote to perform the joke for JITB.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        button_name = 'Perform the joke for me'  # Look for this button
        buttons = []                             # All the buttons from web_driver
        clicked_it = False                       # Was anything clicked?

        # INPUT VALIDATION
        if _is_perform_page(web_driver=web_driver):
            _click_a_button(web_driver=web_driver, button_str=button_name)  # Don't really care

    def validate_status(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Validates the web_driver and internal attributes.

        Args:
            web_driver: The webdriver object to interact with.
        """
        self._check_web_driver(web_driver=web_driver)
        self._validate_core_attributes()

    # Private Methods (alphabetical order)
    def _add_to_joke_topic_dict(self, key: str, value: List[str]) -> None:
        """Safely add key:value to self._joke_topic_dict."""
        print(f'Adding {key} : {value} to self._joke_topic_dict')  # DEBUGGING
        if key in self._joke_topic_dict:
            self._joke_topic_dict[key].extend(value)
        else:
            self._joke_topic_dict[key] = value

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
            try:
                prompt_text = get_prompt(web_driver=web_driver)
                if prompt_text and prompt_text != last_prompt:
                    break
                time.sleep(JITB_POLL_RATE)  # Give the prompt a chance to update from the last one
            except RuntimeError as err:
                if err.args[0] == 'This is not a prompt page':
                    break  # It was(?) but now it's not...
                raise err from err

        # ANSWER IT
        answer = self.generate_ai_answer(prompt=prompt_text, ai_obj=self._ai_obj, length_limit=80)
        prompt_input = get_web_element(web_driver, By.ID, 'input-text-textarea')
        if prompt_input:
            prompt_input.send_keys(answer)
            clicked_it = _click_a_button(web_driver=web_driver, button_str='SUBMIT')

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer the prompt')
        Logger.debug(f'Answered prompt "{prompt_text}" with "{answer}"!')
        return prompt_text

    def _generate_bulk_joke_topics(self, key: str) -> None:
        """Generate bulk joke topic answers for the key and add them to the original dict.

        Adds topics to self._joke_topic_dict[key].

        Args:
            key: The key to use in the dictionary.
        """
        # LOCAL VARIABLES
        list_len = 10  # Number of entries to generate for key
        prompt = f'Give me a comma-separated list of {str(list_len)} new examples of this word ' \
                 + f'and no other words: {key}.  Ensure your listed answers have comedic potential.'
        # AI generated answer
        ai_answer = self.generate_ai_answer(prompt=prompt, ai_obj=self._ai_obj,
                                            length_limit=list_len * 10 * 2)
        answers = _split_and_strip_answers(ai_answer)

        # STORE IT
        Logger.debug(f'JitbAi generated "{answers}" as bulk joke topics for the key "{key}"')
        self._add_to_joke_topic_dict(key=key, value=answers)

    def _gen_vote_topics(self, key: str) -> bool:
        """Generate AI-created vote topics, and add them to the dict, in a dynamic way.

        The real problem is OpenAI doesn't like to be spammed.  Currently model in use restricts
        requests to 3 requests per minute (rpm).  There's an attribute to keep track of the
        number of requests.  Less than 3 requests, call self._generate_bulk_joke_topics().  Last
        request will be to _populate_joke_topic_dict().  The Joke Topic round is only 45 seconds
        so this method will stop attempting to generate Joke Topics after three JitbAi queries.

        Returns:
            True if a topic was generated, false otherise.
        """
        # LOCAL VARIABLE
        made_some = True  # Generated some vote topics

        # self._generate_bulk_joke_topics()
        if self._num_requests < 2:
            self._generate_bulk_joke_topics(key=key)  # Gen 10 answers for key
            self._num_requests += 1
        # self._populate_joke_topic_dict()
        elif self._num_requests == 2:
            self._populate_joke_topic_dict(key=key)  # Gen 1 answer per KNOWN_JOKE_TOPICS
            self._num_requests += 1
        else:
            made_some = False
            Logger.debug(f'Max number of Joke Topic requests have been made: {self._num_requests}')

        # DONE
        return made_some

    def _populate_joke_topic_dict(self, num_requests: int = 1, key: str = None) -> None:
        """Prepopulate self._joke_topic_dict with joke topic answers across the board.

        Args:
            num_requests: Optional; Number of times to request topics from JitbAi.
            key: Optional; Ensure this key is part of KNOWN_JOKE_TOPICS, otherwise lump it in.

        If _generate_bulk_joke_topics() generates many answers about one topic,
        _populate_joke_topic_dict() one answer for each topic.
        """
        # LOCAL VARIABLES
        # Let's see if we can get JitbAi to do what we want.
        base_prompt = 'Give me one example each for each of these in a comma-separaed list: {}'
        joke_topics = KNOWN_JOKE_TOPICS  # List of topics to query JitbAi for
        actual_prompt = ''               # Formatted with the dynamic list of topics
        answers = []                     # AI answer split and stripped into a list
        topic_list = ''                  # Comma-separated list of Joke Topics

        # SETUP
        if key and key.lower() not in [topic.lower() for topic in joke_topics]:
            Logger.debug(f'Be sure to add this key to the list of KNOWN_JOKE_TOPICS: {key}')
            joke_topics.append(key)
        topic_list = ', '.join(joke_topics)
        actual_prompt = base_prompt.format(topic_list)

        # POPULATE IT
        for num_request in range(num_requests):
            # Get topcs from JitbAi
            answer = self.generate_ai_answer(prompt=actual_prompt, ai_obj=self._ai_obj,
                                             length_limit=len(joke_topics) * 10 * 2)
            Logger.debug(f'JitbAi answer "{actual_prompt}" with "{answer}"')
            answers = _split_and_strip_answers(answer)
            # Populate internal dict
            for joke_topic, answer in zip(joke_topics, answers):
                self._add_to_joke_topic_dict(key=joke_topic, value=[answer])

        # DONE
        self._joke_topic_init = True  # It's initialized now


# num_entries = 5  # Number of initial entries per key
# One big prompt to get all the answers at once (to circumvent throttling timeouts)
# prompt = 'Give me a newline delimited list.  Each line of the list should have a ' \
#          + f'comma separated list of {num_entries} words.  Each of the {num_entries} ' \
#          + 'words per line should contain potentially comedic examples of a ' \
#          + 'prompt list I give ' \
#          + 'you.  There should be one ' \
#          + f'line of {num_entries} words dedicated to an entry in the prompt list.  ' \
#          + 'The prompt list is as follows: \n{}'
# prompt = 'Give me a  ' \
#          + f'comma separated list of {num_entries} words.  Each of the {num_entries} ' \
#          + 'words should contain potentially comedic examples of a phrase I give you. ' \
#          + 'Do not restate the phrase in your answer.  The phrase is: \n{}'
# prompt = f'Give me {num_entries} examples of ' \
#          + '{}' \
#          + f'in a list.  Each of the {num_entries} ' \
#          + 'words should have comedic potential yet still be fair examples.  ' \
#          + 'Do not explain your answers.'
# prompt = f'Give me {num_entries} potentially comedic examples of ' \
#          + '{} without explanation, embellishment, or definition. ' \
#          + 'An example of a well-formatted response would be ' \
#          + '"answer1\nanswer2\nanswer3\nanswer4\nanswer5"' \
#          + ''
# prompt = f'Give me {num_entries} potentially comedic examples of ' \
# prompt = f'Give me {num_entries} examples of ' \
#          + '{} without commentary, explanation, embellishment, or definition ' \
#          + ' separated by newline characters (\n).'
#         + 'An example of a well-formatted response would be ' \
#         + '"answer1\nanswer2\nanswer3\nanswer4\nanswer5"' \
# prompt = f'Give me {num_entries} examples of ' \
#          + '{} without commentary, explanation, embellishment, or definition ' \
#          + ' separated by newline characters (\n).'
# strip_string = punctuation + whitespace  # Strip these characters from list entries
# answer1 = ''     # First half of the answer for the prompt
# answer2 = ''     # Second half of the answer for the prompt
# csl_list = []    # List of comma-separated strings to parse into the dict
# temp_value = ''  # Cleanup the raw string
# temp_list = []   # The entries need to be cleaned up before stored in the dictionary

# if not self._joke_topic_init:
# PREPOPULATE IT
# Generate an answer
# answer1 = \
#     self.generate_ai_answer(prompt=prompt.format('\n'.join(KNOWN_JOKE_TOPICS[:3])),
#                             ai_obj=self._ai_obj, length_limit=10000)
# time.sleep(JITB_POLL_RATE)
# answer2 = \
#     self.generate_ai_answer(prompt=prompt.format('\n'.join(KNOWN_JOKE_TOPICS[3:6])),
#                             ai_obj=self._ai_obj, length_limit=10000)
# print(f'ANSWER 1:\n{answer1}')  # DEBUGGING
# print(f'ANSWER 2:\n{answer2}')  # DEBUGGING
# if not answer1 or not answer2:
#     raise RuntimeError(f'JitbAi failed to produce a set of joke topics')
# Logger.debug('JitbAi generated the following to prepopulate the joke topic dict:\n'
#              f'{answer1}\n{answer2}')
# csl_list = answer1.split('\n')[:3]
# csl_list.extend(answer2.split('\n')[:3])
# Validate results
# if len(csl_list) != len(KNOWN_JOKE_TOPICS):
#     raise RuntimeError(f'JitbAi failed to follow instructions.  {len(csl_list)} lines '
#                        f'were provided but {len(KNOWN_JOKE_TOPICS)} were expected')
# Populate dictionary
# for key, value in zip(KNOWN_JOKE_TOPICS, csl_list):
#     temp_value = value
#     if temp_value.upper().startswith(key.upper()):
#         temp_value = temp_value[len(key):]  # JitbAi can't follow instructions
#     if temp_value.startswith(':'):
#         temp_value = temp_value[1:]  # Slice it off
#     temp_list = [entry.rstrip(strip_string).lstrip(strip_string) for entry
#                  in temp_value.split(',')]
#     print(f'FORMED DICT ENTRY: {temp_list}')  # DEBUGGING
#     self._joke_topic_dict[key] = temp_list
# print(f'PREPOPULATED DICT:\n{self._joke_topic_dict}')  # DEBUGGING
# for joke_topic in KNOWN_JOKE_TOPICS:
#     # temp_value = self.generate_ai_answer(prompt=prompt.format(joke_topic),
#     #                                      ai_obj=self._ai_obj, length_limit=1000)
#     self._generate_bulk_joke_topics(prompt=prompt.format(joke_topic), key=joke_topic)
#     # print(f'JitbAi pregenerated "{temp_value}" for "{joke_topic}"')
#     # temp_list = temp_value.split(',')
#     # temp_list = [entry.rstrip(strip_string).lstrip(strip_string) for entry in
#     #              temp_list if entry]
#     # self._joke_topic_dict[joke_topic] = temp_list
#     time.sleep(12)  # OpenAI gets unhappy if you spam it


# Public Functions (alphabetical order)
def get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
               check_needles: bool = True) -> str:
    """Get the prompt text from the question-text web element.

    Do not use this for the Round 3 Last Lash prompt because the Last Lash prompt
    commonly has multiple lines.

    Args:
        web_driver: The web driver to get the prompt from.
        check_needles: Optional; If True, will verify prompt needles are found.

    Returns:
        The game prompt text.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a prompt page.
        TypeError: Bad data type.
        ValueError: Invalid by value.
    """
    # LOCAL VARIABLES
    needle = 'prompt'  # Web element id to find in web_driver
    prompt_text = ''   # The prompt's text as a string

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)
    if not _is_prompt_page(web_driver, check_needles=check_needles):
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


def get_vote_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                  check_needles: bool = True) -> str:
    """Get the vote text from various web elements, assemble them, and return it.

    Args:
        web_driver: The web driver to get the prompt from.
        check_needles: Optional; If True, will verify prompt needles are found.

    Returns:
        The game vote text.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a vote page.
        TypeError: Bad data type.
        ValueError: Invalid by value.
    """
    # LOCAL VARIABLES
    needle = 'prompt'  # Web element to look for
    vote_text = ''     # The full vote prompt

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)
    if not _is_vote_page(web_driver, check_needles=check_needles):
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
def _click_a_button(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    button_str: str) -> bool:
    """Standardize the way buttons are clicked.

    Args:
        web_driver: The webdriver object to interact with.
        button_str: The substring to search for within the button text.

    Returns:
        True if a button was clicked, false otherwise.
    """
    # LOCAL VARIABLES
    buttons = get_buttons(web_driver=web_driver)  # All the buttons from web_driver
    clicked_it = False                            # Return value

    # CLICK IT
    for button in buttons:
        # Find it
        if button_str.lower() in button.text.lower() and button.is_enabled():
            # Click it
            try:
                button.click()
            except ElementNotInteractableException as err:
                Logger.debug(f'Failed to click "{button.text}" with {repr(err)}')
            else:
                clicked_it = True
            finally:
                break

    # DONE
    return clicked_it

def _is_catchphrase_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is a catchphrase page.

    Args:
        web_driver: The web driver to check.

    Returns:
        True if this is a catchphrase page, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'prompt'   # The web element value to search for
    catchphrase_page = False  # Prove this true
    temp_text = ''            # Text from the web element

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text and CATCHPHRASE_PROMPT_NEEDLE.lower() in temp_text.lower():
            catchphrase_page = True  # If we made it here, it's a catchphrase page
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return catchphrase_page


def _is_joke_topic_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is a joke topic page.

    Args:
        web_driver: The web driver to check.

    Returns:
        True if this is a joke topic page, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'prompt'  # The web element value to search for
    joke_topic_page = False  # Prove this true
    temp_text = ''           # Text from the web element

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text and JOKE_TOPIC_PROMPT_NEEDLE.lower() in temp_text.lower():
            joke_topic_page = True  # If we made it here, it's a joke topic page
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return joke_topic_page


def _is_perform_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is a your turn to perform page.

    Args:
        web_driver: The web driver to check.

    Returns:
        True if this is a your turn to perform page, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'prompt'                                     # The element value to search for
    perform_page = False                                        # Prove this true
    temp_text = ''                                              # Text from the web element
    perform_needle = 'It’s your turn. What do you want to do?'  # Indicates a perform page

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text and perform_needle.lower() in temp_text.lower():
            perform_page = True  # If we made it here, it's a prompt page
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return perform_page


def _is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    check_needles: bool = True) -> bool:
    """Determine if this is a prompt page.

    Args:
        web_driver: The web driver to check.
        check_needles: Optional; If True, will verify prompt needles are found.

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'prompt'  # The web element value to search for
    prompt_page = False      # Prove this true
    temp_text = ''           # Text from the web element
    # List of prompt needles from various Joke Boat voting screens
    prompts = ['Write your punchline', 'Write the punchline to this joke']

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text:
            if check_needles:
                for prompt in prompts:
                    if prompt.lower() in temp_text.lower():
                        prompt_page = True  # If we made it here, it's a prompt page
                        break  # Found one.  Stop looking.
            else:
                prompt_page = True  # Far enough
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return prompt_page


def _is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                  check_needles: bool = True) -> bool:
    """Determine if this is this a round 1 or 2 vote page.

    Args:
        web_driver: The web driver to check.
        check_needles: Optional; If True, will verify vote needles are found.

    Returns:
        True if this is a regular vote screen, False otherwise.
    """
    # LOCAL VARIABLES
    element_name = 'prompt'  # The web element value to search for
    vote_page = False        # Prove this true
    temp_text = ''           # Temp prompt text
    # List of prompt needles from various Joke Boat voting screens
    prompts = ['Choose a joke set-up', 'Complete your set-up', 'Pick your favorite joke',
               'Pick the joke you want to compete against']

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver, By.ID, element_name)
        if temp_text:
            if check_needles:
                for prompt in prompts:
                    if prompt.lower() in temp_text.lower():
                        vote_page = True  # If we made it here, it's a vote page
                        break  # Found one.  Stop looking.
            else:
                vote_page = True  # Far enough
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a vote page

    # DONE
    return vote_page


def _split_and_strip_answers(answer: str, delimiter: str = ',') -> List[str]:
    """Split a comma-separated answer into a list of strings stipped of garbage."""
    strip_string = digits + punctuation + whitespace  # Strip these characters from list entries
    # List of split and stripped answers
    answers = [entry.rstrip(strip_string).lstrip(strip_string) for entry in
               answer.split(delimiter) if entry]
    return answers


def _validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Validate a web driver."""
    if not web_driver:
        raise TypeError('Web driver can not be of type None')
    if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
        raise TypeError(f'Invalid web_driver data type of {type(web_driver)}')


# pylint: disable = too-many-branches
def _vote_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                 last_prompt: str, ai_obj: JitbAi, check_needles: bool = True) -> str:
    """Generate votes for other players prompts.

    Args:
        web_driver: The web driver to check.
        last_prompt: The last prompt that was answered.  Helps this function avoid trying to
            answer the same prompt twice.
        ai_obj: The JitbAi object to use.
        check_needles: Optional; If True, will verify vote needles are found.

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
            prompt_text = get_vote_text(web_driver=web_driver, check_needles=check_needles)
            if prompt_text and prompt_text != last_prompt:
                break
            if not _is_vote_page(web_driver, check_needles=check_needles):
                prompt_text = ''
                break
            time.sleep(JITB_POLL_RATE / 2)  # Less sleep, faster voting
        except NoSuchElementException:
            prompt_text = ''  # Must have been the last prompt to vote
        except RuntimeError as err:
            if err.args[0] == 'This is not a vote page':
                break  # It was(?) but now it's not...
            raise err from err

    # ANSWER IT
    if prompt_text and prompt_text != last_prompt:
        # buttons = get_sub_buttons(web_driver=web_driver, sub_by=By.ID, sub_value='quiplash-vote')
        buttons = get_buttons(web_driver=web_driver)
        buttons = [button for button in buttons if button.is_enabled()]
        # Form the selection list
        for button in buttons:
            if button.text:
                temp_text = button.text.strip('\n')
                button_dict[temp_text] = button.text
                choice_list.append(temp_text)
        # Ask the AI
        favorite = ai_obj.vote_favorite(prompt=prompt_text, answers=choice_list)
        # Click it
        clicked_it = _click_a_button(web_driver=web_driver, button_str=button_dict[favorite])
    else:
        prompt_text = ''  # Nothing got answered

    # DONE
    if prompt_text and prompt_text != last_prompt and not clicked_it:
        raise RuntimeError('Did not vote an answer')
    if clicked_it:
        temp_text = prompt_text.replace('\n', ' ')
        Logger.debug(f'Chose "{favorite}" for "{temp_text}"!')
    return prompt_text
# pylint: enable = too-many-branches
