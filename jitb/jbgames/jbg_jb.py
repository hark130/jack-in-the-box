"""Defines the package's Jackbox Games Joke Boat class."""

# Standard
from string import digits, punctuation, whitespace
from typing import Dict, Final, List
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
        self._prepopulate_joke_topic_dict()

        # PLAY
        if self._last_page != self._current_page:
            if self._current_page == JbgPageIds.VOTE:
                self.vote_answers(web_driver=web_driver)
            elif self._current_page == JbgPageIds.JB_TOPIC:
                self.enter_vote_topics(web_driver=web_driver)
            elif self._current_page == JbgPageIds.ANSWER:
                self.answer_prompts(web_driver=web_driver)
            elif self._current_page == JbgPageIds.JB_PERFORM:
                pass  # TO DO: DON'T DO NOW
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
        """Choose the catchphrase for the game."""
        # LOCAL VARIABLES
        prompt_text = ''  # Input prompt

        # INPUT VALIDATION
        if not _is_catchphrase_page(web_driver=web_driver):
            raise RuntimeError('This is not the catchphrase page')

        # CHOOSE IT
        prompt_text = _vote_answer(web_driver=web_driver, last_prompt=prompt_text,
                                   ai_obj=self._ai_obj, check_needles=False)

    def enter_vote_topics(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Enter some topics until you can't anymore."""
        # LOCAL VARIABLES
        answer = ''                                                                # AI answer
        prompt_text = ''                                                           # Input prompt
        new_text = ''                                                              # Modified text
        haystack_text = 'Write as many topics as you can.'                         # Replace this
        temp_key = ''                                                              # Answer dict key
        # With this
        replacement_text = 'Give me a comma separated list of 10 of these words and no other ' \
                           + 'words.  Be sure the words have comedic potential:'

        # ENTER AS MANY TOPICS AS YOU CAN
        self._prepopulate_joke_topic_dict()  # Check at least one more time
        while _is_joke_topic_page(web_driver=web_driver):
            # GET PROMPT
            prompt_text = get_prompt(web_driver=web_driver, check_needles=False)
            new_text = prompt_text.replace(haystack_text, replacement_text)
            Logger.debug(f'Enter vote topics just modified "{prompt_text}" to read "{new_text}"')
            temp_key = prompt_text.split('\n')[1]
            # ANSWER IT
            if temp_key not in self._joke_topic_dict or not self._joke_topic_dict[temp_key]:
                Logger.debug(f'{temp_key} was requested as a vote topic but not present')
                self._generate_bulk_topics(prompt=new_text, key=temp_key)
                time.sleep(JITB_POLL_RATE * 5)  # Let the page get updated
            prompt_input = get_web_element(web_driver, By.ID, 'input-text-textarea')
            if prompt_input:
                answer = self._joke_topic_dict[temp_key].pop()
                prompt_input.send_keys(answer)
                buttons = get_buttons(web_driver)
                for button in buttons:
                    if 'SUBMIT'.lower() in button.text.lower() and button.is_enabled():
                        button.click()
                        clicked_it = True
                        Logger.debug(f'Submitted topic "{answer}"!')
                        break
            time.sleep(JITB_POLL_RATE)  # Give the page a chance to update

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer any vote topics')

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
        answer = self.generate_ai_answer(prompt=prompt_text, ai_obj=self._ai_obj)
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

    def _generate_bulk_topics(self, prompt: str, key: str) -> None:
        """Generate bulk answers for the prompt and add them to the original dict.

        Assumes the prompt matches the format of a joke topic prompt.  Will retrieve the dict
        key from after the newline.  Adds topics to self._joke_topic_dict.

        Args:
            prompt: The prompt to give the AI.
            key: The key to use in the dictionary.

        Returns:
            An updated dictionary.
        """
        # LOCAL VARIABLES
        # AI generated answer
        ai_answer = self.generate_ai_answer(prompt=prompt, ai_obj=self._ai_obj,
                                            length_limit=200)
        strip_string = digits + punctuation + whitespace  # Strip these characters from list entries
        # answers = ai_answer.split('\n')   # Answers
        # Answer to add to the dictionary
        answers = [entry.rstrip(strip_string).lstrip(strip_string) for entry in 
                   ai_answer.split('\n') if entry]

        # STORE IT
        Logger.debug(f'JitbAi generated "{answers}" as bulk topics for the key "{key}"')
        # print(f'JUST GENERATED CONTENT FOR {key}')  # DEBUGGING
        # print(f'ANSWERS: {answers}')  # DEBUGGING
        # print(f'NEW DICT BEFORE: {new_dict}')  # DEBUGGING
        if key in self._joke_topic_dict:
            self._joke_topic_dict[key].extend(answers)
        else:
            self._joke_topic_dict[key] = answers
        # print(f'NEW DICT AFTER:  {new_dict}')  # DEBUGGING

    def _prepopulate_joke_topic_dict(self) -> None:
        """Prepopulate self._joke_topic_dict with joke topic answers."""
        # LOCAL VARIABLES
        num_entries = 5  # Number of initial entries per key
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
        prompt = f'Give me {num_entries} examples of ' \
                 + '{} without commentary, explanation, embellishment, or definition ' \
                 + ' separated by newline characters (\n).'
                 # + 'An example of a well-formatted response would be ' \
                 # + '"answer1\nanswer2\nanswer3\nanswer4\nanswer5"' \
        strip_string = punctuation + whitespace  # Strip these characters from list entries
        answer1 = ''     # First half of the answer for the prompt
        answer2 = ''     # Second half of the answer for the prompt
        csl_list = []    # List of comma-separated strings to parse into the dict
        temp_value = ''  # Cleanup the raw string
        temp_list = []   # The entries need to be cleaned up before stored in the dictionary

        if not self._joke_topic_init:
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
            for joke_topic in KNOWN_JOKE_TOPICS:
                # temp_value = self.generate_ai_answer(prompt=prompt.format(joke_topic),
                #                                      ai_obj=self._ai_obj, length_limit=1000)
                self._generate_bulk_topics(prompt=prompt.format(joke_topic), key=joke_topic)
                # print(f'JitbAi pregenerated "{temp_value}" for "{joke_topic}"')
                # temp_list = temp_value.split(',')
                # temp_list = [entry.rstrip(strip_string).lstrip(strip_string) for entry in 
                #              temp_list if entry]
                # self._joke_topic_dict[joke_topic] = temp_list
                time.sleep(12)  # OpenAI gets unhappy if you spam it

            # DONE
            print(f'PREPOPULATED DICT:\n{self._joke_topic_dict}')  # DEBUGGING
            self._joke_topic_init = True  # It's initialized now



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
        Logger.debug(f'Chose "{favorite}" for "{temp_text}"!')
    return prompt_text
# pylint: enable = too-many-branches
