"""Defines the package's Jackbox Games Joke Boat class."""

# Standard
from string import digits, punctuation, whitespace
from typing import Final, List
import random
import time
# Third Party
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import JbgAbc
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_globals import JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_webdriver import (click_a_button, get_char_limit, get_prompt, is_prompt_page,
                                 is_vote_page, vote_answers, write_an_answer)


DEFAULT_CHAR_LIMIT: Final[int] = 80  # Default maximum character limit
# Known joke topic prompts to use as keys in the dictionary of answers
KNOWN_JOKE_TOPICS: Final[List[str]] = ['A BRAND', 'AN OBJECT', 'A FOOD', 'A LOCATION',
                                       'A PLURAL NOUN', 'AN ANIMAL', 'A PERSON’S NAME']
# Maximum number of Joke Topic requests
MAX_JOKE_TOPIC_REQUESTS: Final[int] = 10


# pylint: disable = too-many-instance-attributes
class JbgJb(JbgAbc):
    """Jackbox Games (JBG) Joke Boat (JB) class."""

    # Methods are listed in expected 'call order'.
    def __init__(self, ai_obj: JitbAi, username: str) -> None:
        """JbgJb ctor.

        Args:
            ai_obj:  OpenAI API interface to use in this game.
            username:  The screen name used in this game.
        """
        ai_obj.change_system_content('You are a witty person trying to win the Jackbox Game '
                                     'Joke Boat')
        super().__init__(ai_obj=ai_obj, username=username)
        self._joke_topic_dict = {}     # Dictionary of joke topics (see: KNOWN_JOKE_TOPICS)
        self._joke_topic_init = False  # Joke Topic Dict prepopulated
        self._num_requests = 0         # Number of Joke Topic AI requests; Capped by module constant
        # A 'needle' to help identify the catchphrase page
        self._chatchphrase_clues = ['catchphrase']
        # A 'needle' to help identify the joke topic page
        self._joke_topic_clues = ['Write as many topics as you can']
        # A 'needle' to help identify the perform page
        self._perform_clues = ['It’s your turn. What do you want to do?']
        # Pass these values as prompt_clues arguments to jitb_webdriver functions
        self._prompt_clues = ['Write your punchline', 'Write the punchline to this joke']
        # Pass these values as vote_clues arguments to jitb_webdriver functions
        self._vote_clues = ['Choose a joke set-up', 'Complete your set-up',
                            'Pick your favorite joke', 'Pick the joke you want to compete against']

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
            if self._last_page == JbgPageIds.JB_TOPIC:
                self._num_requests = 0  # Reset the count in case there's another game
            if self._current_page == JbgPageIds.VOTE:
                self.vote_answers(web_driver=web_driver, vote_clues=self._vote_clues)
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

    def vote_answers(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                     vote_clues: List[str] = None) -> None:
        """Read other answers to a prompt from the web_driver, ask the AI, and submit the answer.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        element_name = 'prompt'  # The element name to get
        prompt_text = ''         # The prompt text

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # VOTE IT
        while True:
            if not self.is_any_vote_page(web_driver=web_driver):
                break
            try:
                prompt_text = vote_answers(web_driver=web_driver, last_prompt=prompt_text,
                                           ai_obj=self._ai_obj, element_name=element_name,
                                           element_type=By.ID, vote_clues=vote_clues,
                                           clean_string=True)
                Logger.debug(f'JbgJb.vote_answers() called vote_answer(element_name={element_name},'
                             f' element_type={By.ID}, vote_clues={vote_clues}, '
                             f'clean_string=True) which returned: {prompt_text}')
            except RuntimeError as err:
                if err.args[0] == f'Unable to locate the {element_name} element value':
                    Logger.debug(f'vote_answers() raised {repr(err)} but it is being ignored')
                    break  # Something went wrong so let's just leave this loop
            if not prompt_text:
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
        elif self.is_joke_topic_page(web_driver=web_driver):
            current_page = JbgPageIds.JB_TOPIC
        elif self.is_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif self.is_perform_page(web_driver=web_driver):
            current_page = JbgPageIds.JB_PERFORM
        elif self.is_catchphrase_page(web_driver=web_driver):
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
        # INPUT VALIDATION
        if not self.is_catchphrase_page(web_driver=web_driver):
            raise RuntimeError('This is not the catchphrase page')

        # CHOOSE IT
        self.vote_answers(web_driver=web_driver, vote_clues=self._chatchphrase_clues)

    def enter_vote_topics(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Enter some topics until you can't anymore.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        answer = ''         # AI answer
        prompt_text = ''    # Input prompt
        temp_key = ''       # Answer dict key
        clicked_it = False  # Button has been clicked

        # ENTER AS MANY TOPICS AS YOU CAN
        while self.is_joke_topic_page(web_driver=web_driver):
            # RESET TEMP VARIABLES
            answer = ''       # AI answer
            prompt_text = ''  # Input prompt
            temp_key = ''     # Answer dict key
            # GET PROMPT
            prompt_text = self.get_prompt(web_driver=web_driver, clean_string=False)
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
            if self._joke_topic_dict[temp_key]:
                answer = self._joke_topic_dict[temp_key].pop()
                clicked_it = self.submit_an_answer(web_driver=web_driver, submit_text=answer)
                if clicked_it:
                    Logger.debug(f'Submitted {answer} for the {prompt_text} joke topic')
                else:
                    Logger.debug(f'Failed to submit {answer} as a joke topic to {prompt_text}')
            else:
                Logger.debug(f'The joke topic dictionary is missing entries for {temp_key}')
            time.sleep(JITB_POLL_RATE)  # Give the page a chance to update

        # DONE
        if not clicked_it and self._num_requests < MAX_JOKE_TOPIC_REQUESTS:
            raise RuntimeError('Did not answer any vote topics')

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

    def get_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   prompt_clues: List[str] = None, clean_string: bool = True) -> str:
        """Wraps jitb_webdriver.get_prompt with game-specific details."""
        return get_prompt(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                          prompt_clues=prompt_clues, clean_string=clean_string)

    def is_any_vote_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_vote_page with game-specific details for vote & catchprhase."""
        return is_vote_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                            vote_clues=self._vote_clues + self._chatchphrase_clues,
                            clean_string=True)

    def is_catchphrase_page(self,
                            web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Determine if this is this a catchphrase page.

        Returns:
            True if this is a choose-a-catchphrase screen, False otherwise.
        """
        return is_vote_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                            vote_clues=self._chatchphrase_clues)

    def is_joke_topic_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_vote_page with game-specific details."""
        return is_vote_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                            vote_clues=self._joke_topic_clues)

    def is_perform_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_vote_page with game-specific details."""
        return is_vote_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                            vote_clues=self._perform_clues)

    def is_prompt_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_prompt_page with game-specific details."""
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._prompt_clues)

    def is_vote_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_vote_page with game-specific details."""
        return is_vote_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                            vote_clues=self._vote_clues, clean_string=True)

    def skip_perform(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Tell Joke Bote to perform the joke for JITB.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        button_name = 'Perform the joke for me'  # Look for this button

        # INPUT VALIDATION
        if self.is_perform_page(web_driver=web_driver):
            click_a_button(web_driver=web_driver, button_str=button_name)  # Don't really care

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
        return write_an_answer(web_driver=web_driver, submit_text=submit_text,
                               element_name='input-text-textarea', element_type=By.ID)

    # Private Methods (alphabetical order)
    def _add_to_joke_topic_dict(self, key: str, value: List[str]) -> None:
        """Safely add key:value to self._joke_topic_dict."""
        Logger.debug(f'Adding {key} : {value} to self._joke_topic_dict')
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
        clicked_it = False   # Keep track of whether this prompt was answered or not
        num_loops = 5        # Number of attempts to make for a new prompt

        # INPUT VALIDATION
        if not self.is_prompt_page(web_driver):
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

    def _generate_bulk_joke_topics(self, key: str) -> None:
        """Generate bulk joke topic answers for the key and add them to the original dict.

        Adds topics to self._joke_topic_dict[key].

        Args:
            key: The key to use in the dictionary.
        """
        # LOCAL VARIABLES
        prompt = ''     # Crafted prompt to pass to JitbAi()
        list_len = 10   # Number of entries to generate for key
        # len_limit = list_len * 10 * 2  # Length limit for query to AI
        temp_key = key  # Gives us a chance to mangle a key, for prompt engineering
        # A list of different "people" types
        people_types = ['Famous', 'Fictional', 'Fairytale', 'Historical', 'Futuristic', 'Cartoon',
                        'Book', 'Movie', 'Comic Book']
        if key.upper().startswith('A BRAND'.upper()):
            prompt = f'Generate a list of {str(list_len)} well-known commercial brands.'
        elif key.upper() == 'A PERSON’S NAME':
            temp_key = f'A {random.choice(people_types).upper()} PERSON’S NAME'
        if not prompt:
            prompt = f'Give me a list of {str(list_len)} new examples of this ' \
                     + f'thing with no other commentary or explanation: {temp_key}.'
        # AI generated answer
        messages = [{'role': 'user', 'content': prompt}]
        answer = self._ai_obj.create_content(messages=messages, add_base_msgs=False,
                                             max_tokens=100)
        answers = _split_and_strip_answers(answer, '\n')

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
        last_request = MAX_JOKE_TOPIC_REQUESTS - 1  # Last request number

        # self._populate_joke_topic_dict()
        if self._num_requests == last_request:
            self._populate_joke_topic_dict(key=key)  # Gen 1 answer per KNOWN_JOKE_TOPICS
            self._num_requests += 1
        # self._generate_bulk_joke_topics()
        elif self._num_requests < last_request:
            self._generate_bulk_joke_topics(key=key)  # Gen 10 answers for key
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
        base_prompt = 'Give me one example each for each of these, with no other commentary ' \
                      + 'or explanation, in a comma-separated list: {}'
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
        for _ in range(num_requests):
            # Get topcs from JitbAi
            answer = self.generate_ai_answer(prompt=actual_prompt, ai_obj=self._ai_obj,
                                             length_limit=len(joke_topics) * 10 * 2)
            Logger.debug(f'JitbAi answered "{actual_prompt}" with "{answer}"')
            answers = _split_and_strip_answers(answer)
            # Populate internal dict
            for joke_topic, answer in zip(joke_topics, answers):
                self._add_to_joke_topic_dict(key=joke_topic, value=[answer])

        # DONE
        self._joke_topic_init = True  # It's initialized now
# pylint: enable = too-many-instance-attributes


# Private Functions (alphabetical order)
def _split_and_strip_answers(answer: str, delimiter: str = ',') -> List[str]:
    """Split a comma-separated answer into a list of strings stipped of garbage."""
    # List of split and stripped answers
    answers = [_strip_answer(entry) for entry in answer.split(delimiter) if entry]
    return answers


def _strip_answer(answer: str) -> str:
    """Strip answer of garbage: digits, punctuation, whitespace, 'a ', and 'an '."""
    # LOCAL VARIABLES
    strip_string = digits + punctuation + whitespace  # Strip these characters from list entries

    # STRIP IT
    new_answer = answer.rstrip(strip_string).lstrip(strip_string)
    if new_answer.lower().startswith('a '.lower()):
        new_answer = new_answer[2:]
    if new_answer.lower().startswith('an '.lower()):
        new_answer = new_answer[3:]

    # DONE
    if new_answer != answer:
        new_answer = _strip_answer(new_answer)  # Keep stripping until it's clean
    return new_answer
