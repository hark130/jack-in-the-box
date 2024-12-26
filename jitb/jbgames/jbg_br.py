"""Defines the package's Jackbox Games Blather 'Round class."""

# Standard
from typing import Final, List, Tuple
import string
import time
# Third Party
from hobo.validation import validate_list, validate_string
from selenium.common.exceptions import (ElementNotInteractableException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import JbgAbc
from jitb.jbgames.jbg_page_ids import JbgPageIds
from jitb.jitb_globals import JITB_FITB_STR, JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_selenium import get_web_element, get_web_elements
from jitb.jitb_webdriver import (click_a_button, get_char_limit, get_prompt, is_prompt_page,
                                 vote_answers, write_an_answer)
from jitb.jitb_validation import validate_pos_int


DEFAULT_CHAR_LIMIT: Final[int] = 40  # Default maximum character limit


# pylint: disable = too-many-instance-attributes, too-many-public-methods
class JbgBr(JbgAbc):
    """Jackbox Games (JBG) Blather 'Round (Br) class."""

    # Methods are listed in expected 'call order'.
    def __init__(self, ai_obj: JitbAi, username: str) -> None:
        """JbgBr ctor.

        Args:
            ai_obj:  OpenAI API interface to use in this game.
            username:  The screen name used in this game.
        """
        # Hints the page is on the Blather 'Round-specific "assign blame" page
        self._blame_clues = ['Do you think that you should']
        # Pass these values as prompt_clues arguments to jitb_webdriver functions
        self._describe_clues = ['Describe ']
        # Pass these values as vote_clues arguments to jitb_webdriver functions
        self._guess_clues = ['What story', 'What person', 'What thing', 'What place']
        # Hints the page is on the Blather 'Round-specific "secret prompt" page
        self._secret_clues = ['Choose your secret prompt']
        # Exclude these button names from selecting secret prompts
        self._exclude = ['Get 3 New Prompts', 'Skip']
        # Wrong guesses for another player's secret prompt
        self._wrong_guesses = []
        # Previous descriptions for this player's secret prompt
        self._prev_descr = []
        # Update AI system: content message
        ai_obj.change_system_content('You are a smart person trying to win the Jackbox Game '
                                     "Blather 'Round. Do not add extra context "
                                     'and not not add extraneous commentary '
                                     'when choosing words or guessing answers. '
                                     'Respond with as few words as possible.')
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
            Logger.debug(f'Now viewing a(n) {self._current_page.name} page!')
            if self._current_page == JbgPageIds.ANSWER:
                self._wrong_guesses.clear()  # Empty the list
                self.answer_prompts(web_driver=web_driver, timeout=10)
            elif self._current_page == JbgPageIds.BR_DESCRIBE:
                self._prev_descr.clear()  # Empty the list
                self.vote_answers(web_driver=web_driver)
            elif self._current_page == JbgPageIds.BR_SECRET:
                self.choose_secret(web_driver=web_driver)
            elif self._current_page == JbgPageIds.BR_FAULT:
                self.assign_blame(web_driver=web_driver)
        elif self._current_page == JbgPageIds.BR_DESCRIBE:
            self.vote_answers(web_driver=web_driver)  # Always try to describe a prompt

    def select_character(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Randomize an avatar selection from the available list.

        Args:
            web_driver: The webdriver object to interact with.

        Raises:
            NotImplementedError: Blather 'Round does not allow players to choose avatars.
        """
        raise NotImplementedError("Blather 'Round does not allow players to choose avatars")

    def answer_prompts(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                       timeout: int = 10) -> None:
        """Read prompts from the web_driver, ask the AI, and submit the AI's answers.

        Args:
            web_driver: The webdriver object to interact with.
            timeout: Optional; Number of concurrent UNKNOWN pages before breaking the loop.
                Why?  We could provide a plethora of guesses before the time runs out.  The first
                indication someone has guessed the secret prompt is an exceptionally long
                'waiting' (AKA JbgPagIds.UNKNOWN) page.
        """
        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)
        validate_pos_int(timeout, 'timeout')
        if not self.is_guess_page(web_driver=web_driver):
            raise RuntimeError("This is not a Blather 'Round guess page")

        # ANSWER THEM
        self.answer_prompt(web_driver=web_driver, timeout=timeout)

    def vote_answers(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Read the describe prompt, lists of choices, ask the AI, and submit the answer.

        If this weren't an abstract method to be overridden then it would have been named
        describe_prompt() or something similar.

        Args:
            web_driver: The webdriver object to interact with.
        """
        # LOCAL VARIABLES
        prompt_text = ''  # The prompt text
        last_prompt = ''  # The last prompt
        answer = ''       # JitbAi's answer to the prompt text
        num_unk = 0       # Number of concurrent UNKNOWN pages
        timeout = 10      # Number of non-vote pages before we give up

        # INPUT VALIDATION
        self.validate_status(web_driver=web_driver)

        # VOTE IT
        while num_unk < timeout:
            try:
                last_prompt = prompt_text  # Save the last prompt
                prompt_text = ''  # Reset reused variable
                prompt_text = self.get_describe_prompt(web_driver=web_driver)
                if prompt_text and prompt_text != last_prompt:
                    Logger.debug(f'Got a new "describe" prompt: {prompt_text}')
                    # Ask the AI
                    answer = self._ask_openai(prompt_text)
                    Logger.debug(f'JitbAi answered "{prompt_text}" with "{answer}"')
                    if answer:
                        # Click the buttons
                        if self.click_describe_buttons(web_driver=web_driver, answer=answer):
                            num_unk = 0  # We answered one so reset the count
                            time.sleep(9)  # Don't spam the game
                        else:
                            num_unk += 1  # Something failed
            except RuntimeError:
                num_unk += 1
            except (ElementNotInteractableException, StaleElementReferenceException) as err:
                Logger.error(f'Failed to vote answers with {repr(err)}')
                break  # Something went wrong so let's just leave this loop
            else:
                if not prompt_text or prompt_text == last_prompt:
                    num_unk += 1  # Nothing got answered
            time.sleep(JITB_POLL_RATE)  # Give the page a second to update
        Logger.debug('Done describing the secret prompt')

    def id_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> JbgPageIds:
        """Determine what type of Jackbox Games webpage web_driver is.

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
        if self.is_guess_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif self.is_describe_page(web_driver=web_driver):
            current_page = JbgPageIds.BR_DESCRIBE
        elif self.is_secret_page(web_driver=web_driver):
            current_page = JbgPageIds.BR_SECRET
        elif self.is_blame_page(web_driver=web_driver):
            current_page = JbgPageIds.BR_FAULT
        elif self._is_login_page(web_driver=web_driver):
            current_page = JbgPageIds.LOGIN

        # DONE
        return current_page

    # Public Methods (alphabetical order)
    def answer_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                      timeout: int) -> None:
        """Generating AI answers to guess the secret prompts of others.

        Does not validate input.

        Args:
            web_driver: The webdriver object to interact with.
            timeout: Number of concurrent UNKNOWN pages before breaking the loop.

        Raises:
            RuntimeError: The prompt wasn't answered.
        """
        # LOCAL VARIABLES
        prompt_text = None  # Input prompt
        answer = ''         # Answer to the prompt
        clicked_it = False  # Keep track of whether this prompt was answered or not
        num_unk = 0         # Number of concurrent UNKNOWN pages

        # WAIT FOR IT
        while num_unk < timeout:
            if answer:
                self._wrong_guesses.append(answer)  # If we're here, the answer was wrong
            try:
                prompt_text = self.get_guess_prompt(web_driver=web_driver)
                if prompt_text:
                    num_unk = 0  # Reset the counter
                    answer = self.generate_ai_answer(prompt_text, self._ai_obj,
                                                     self.get_char_limit(web_driver=web_driver))
                    Logger.debug(f'Answered prompt "{prompt_text}" with "{answer}"!')
                    if self.submit_an_answer(web_driver=web_driver, submit_text=answer):
                        clicked_it = True  # As long as we submitted at least one answer, it's fine
                        time.sleep(10)  # Don't spam the game
                else:
                    num_unk += 1
                    time.sleep(JITB_POLL_RATE)
            except RuntimeError:
                num_unk += 1
                time.sleep(JITB_POLL_RATE)

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer the prompt')

    def assign_blame(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Let the AI decide who is at fault."""
        # LOCAL VARAIBLES
        element_name = 'prompt'  # The element name to get

        # INPUT VALIDATION
        if self.is_blame_page(web_driver=web_driver):
            # ASSIGN IT
            try:
                vote_answers(web_driver=web_driver, last_prompt='', ai_obj=self._ai_obj,
                             element_name=element_name, element_type=By.ID,
                             vote_clues=self._blame_clues, clean_string=True, exclude=None)
            except RuntimeError as err:
                Logger.debug(f'Failed to assign blame with {repr(err)} but continuing on')

    def choose_secret(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Ask the AI to choose a secret prompt.

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
            try:
                prompt_text = vote_answers(web_driver=web_driver, last_prompt=prompt_text,
                                           ai_obj=self._ai_obj, element_name=element_name,
                                           element_type=By.ID, vote_clues=self._secret_clues,
                                           clean_string=True, exclude=self._exclude)
                Logger.debug(f'Answered prompt "{prompt_text}"')
            except (ElementNotInteractableException, RuntimeError,
                    StaleElementReferenceException) as err:
                Logger.error(f'Failed to vote answers with {repr(err)}')
                break  # Something went wrong so let's just leave this loop
            if not prompt_text:
                break  # Nothing got answered

    def click_describe_buttons(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                               answer: str) -> bool:
        """Translate JitbAi's describe answer into buttons clicked.

        Args:
            web_driver: The webdriver object to interact with.
            answer: A single button to click (e.g., 'sticky') or a comma-separated list of two
                buttons to click (e.g., 'fun, family')

        Returns
            True if all buttons were successfully clicked, false otherwise.
        """
        # LOCAL VARIABLES
        clicked_them = True      # Prove this wrong
        button_list = None       # List of buttons to click
        submit_text = 'Submit'   # The text of the Submit button
        extracted_sentence = ''  # Completed sentence to store in previous descriptions

        # INPUT VALIDATION
        self.validate_describe_page(web_driver=web_driver)
        validate_string(answer, 'answer', can_be_empty=False)

        # CLICK THEM
        # Parse the answer
        button_list = [_strip_quotes(button_text) for button_text in answer.split(', ') if
                       isinstance(button_text, str)]
        # Start clicking buttons
        for button_entry in button_list:
            if not click_a_button(web_driver=web_driver, button_str=button_entry):
                clicked_them = False  # Didn't click one
                Logger.error(f'Failed to click the "{button_entry}" button')
        # Submit
        if clicked_them:
            extracted_sentence = _extract_sentence(web_driver=web_driver)
            if extracted_sentence:
                self._prev_descr.append(extracted_sentence)  # Store it
                if click_a_button(web_driver=web_driver, button_str=submit_text):
                    Logger.debug(f'Submitted the description with the "{submit_text}" button')
                else:
                    Logger.debug('Failed, but will try again, to submit the description with the '
                                 f'"{submit_text}" button')
                    time.sleep(JITB_POLL_RATE)  # Give the page a second to update
                    # Give it one last shot
                    clicked_them = click_a_button(web_driver=web_driver, button_str=submit_text)

        # DONE
        if not clicked_them:
            Logger.error('Failed to click the describe buttons')
            # Try to skip this page
            if click_a_button(web_driver=web_driver, button_str='Skip'):
                Logger.debug('Skipping this page')
        return clicked_them

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

    def get_context(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
        """Fetch historical reference hidden in Blather 'Round's html to give the AI context.

        Returns:
            The extracted context as a string on success, None on failure.
        """
        # LOCAL VARIABLES
        context = None              # Gameplay context extracted from the HTML
        text_desc_element = None    # Text descriptions web element
        tag_list = None             # List of paragraph tags from text descriptions
        html_list = None            # Extracted innerHTML from the paragraph tags
        needle = 'is presenting a'  # Indicates the beginning of the context

        # GET IT
        # 1. Find the 'textDescriptions' web element
        text_desc_element = get_web_element(web_driver=web_driver, by_arg=By.ID,
                                            value='textDescriptions')
        # 2. Find all of the 'p' TAG_NAME web elements
        if text_desc_element is not None:
            tag_list = text_desc_element.find_elements(By.TAG_NAME, 'p')
        # 3. Extract the innerHTML attributes into a list
        if tag_list:
            html_list = [tag_html.get_attribute('innerHTML') for tag_html in tag_list]
        # 4. Find the final "is presenting a" entry
        if html_list:
            for i in range(len(html_list) - 1, -1, -1):
                if needle.lower() in html_list[i].lower():
                    html_list = html_list[i:]  # Slice out preceding entries
                    html_list[0] = _cleanup_context(html_list[0])  # Cleanup the first line
                    break  # Found it
        # 5. Slice it, and everything that follows, into a string
        if html_list:
            html_list = [_add_missing_punctuation(html_string) for html_string in html_list]
            context = ' '.join(html_list)
            Logger.debug(f'Extracted the following context: {context}')

        # DONE
        return context

    def get_describe_buttons(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) \
            -> Tuple[str, str]:
        """Read the text of the 'describe' page buttons into two comma-separated string lists.

        Tuple index zero (0) should always be defined but index one (1) may be None if there
        was only one list of buttons.

        Returns:
            The extracted button lists in a tuple on success, None of failure.

        Raises:
            RuntimeError: web_driver is not a describe page.
        """
        # LOCAL VARIABLES
        first_list = None        # Text of the buttons on the left
        second_list = None       # Text of the buttons on the right
        describe_buttons = None  # Tuple of the button lists

        # INPUT VALIDATION
        self.validate_describe_page(web_driver=web_driver)

        # GET BUTTONS
        choices_web_element = get_web_elements(web_driver=web_driver, by_arg=By.CLASS_NAME,
                                               value='choices')
        if choices_web_element:
            first_list = _convert_button_text(choices_web_element[0])
        if len(choices_web_element) > 1:
            second_list = _convert_button_text(choices_web_element[1])

        # DONE
        if first_list:
            describe_buttons = tuple((first_list, second_list))
        return describe_buttons

    def get_describe_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
        """Fetches a full 'describe' prompt, button lists included, from web_driver.

        Returns:
            The extracted describe prompt as a string on success, None of failure.

        Raises:
            RuntimeError: web_driver is not a describe page.
        """
        # LOCAL VARIABLES
        prompt = ''               # Describe your secret prompt
        full_prompt = None        # Prompt, sentence, and button choices
        sentence = ''             # The blanky blank sentence to fill in
        buttons_left = None       # List of buttons on the left
        buttons_right = None      # List of buttons on the right

        # INPUT VALIDATION
        self.validate_describe_page(web_driver=web_driver)

        # GET IT
        prompt = self.get_prompt(web_driver=web_driver, clues=self._describe_clues)
        prompt = prompt.capitalize()
        if prompt:
            sentence = _extract_sentence(web_driver=web_driver)
            try:
                (buttons_left, buttons_right) = self.get_describe_buttons(web_driver=web_driver)

                # FORM IT
                full_prompt = _construct_full_describe_prompt(prompt, sentence, buttons_left,
                                                              buttons_right, self._prev_descr)
            except TypeError as err:
                Logger.error(f'"Get describe prompt" encountered a type error of {repr(err)}')

        # DONE
        return full_prompt

    def get_guess_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
        """Fetches a full 'guess' prompt, previous context included, from web_driver.

        Returns:
            The extracted guess prompt as a string on success, None on failure.

        Raises:
            RuntimeError: web_driver is not on a guess page.
        """
        # LOCAL VARIABLES
        context = ''        # Text description with current context
        prompt = ''         # Actual guess prompt, "What _____ is _____ describing?"
        full_prompt = None  # Context and prompt
        bad_guesses = ''    # Let the AI know it's already guessed wrong

        # VALIDATION
        if not self.is_guess_page(web_driver=web_driver):
            raise RuntimeError("This is not a Blather 'Round guess page")

        # GET IT
        context = self.get_context(web_driver=web_driver)
        if context:
            prompt = self.get_prompt(web_driver=web_driver, clues=self._guess_clues)
            if prompt:
                if self._wrong_guesses:
                    bad_guesses = ' The following guesses were already made and are wrong: ' \
                                  + f'{", ".join(self._wrong_guesses)}.'
                prompt = prompt.capitalize()  # It comes through lowercase for some reason.
                full_prompt = context + bad_guesses + ' Answer the following in one or two ' \
                    + 'words without adding adjectives or adverbs... ' + prompt

        # DONE
        return full_prompt

    def get_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   clues: List[str] = None) -> str:
        """Wraps jitb_webdriver.get_prompt with game-specific details.

        Args:
            web_driver: The webdriver object to interact with.
            clues: Optional; Context clues to help positively identify the right prompt.  If None,
                uses self._guess_clues as a default.
        """
        if clues is None:
            clues = self._guess_clues
        return get_prompt(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                          prompt_clues=clues, clean_string=True)

    def is_blame_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_prompt_page with game-specific details to assign blame."""
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._blame_clues)

    def is_describe_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_prompt_page with game-specific details to describe a secret."""
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._describe_clues)

    def is_guess_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_prompt_page with game-specific details to guess a prompt."""
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._guess_clues)

    def is_secret_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Wraps jitb_webdirver.is_prompt_page with game-specific details to choose a secret."""
        return is_prompt_page(web_driver=web_driver, element_name='prompt', element_type=By.ID,
                              prompt_clues=self._secret_clues)

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

    def validate_describe_page(self,
                               web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Assert that web_driver is a 'describe' page."""
        if not self.is_describe_page(web_driver=web_driver):
            raise RuntimeError("This is not a Blather 'Round describe page")

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

    def _ask_openai(self, question: str) -> str:
        """Ask the JitbAi object a direct question.

        This method of communication flies in the face of everything previous because we're not
        asking for a funny answer.  We're asking some highly engineered prompts.
        """
        # LOCAL VARIABLES
        messages = []  # Local copy of messages to update with actual query
        answer = None  # JitbAi's response

        # INPUT VALIDATION
        validate_string(question, 'question', can_be_empty=False)

        # ASK IT
        messages.append({'role': 'user', 'content': question})
        answer = self._ai_obj.create_content(messages=messages)

        # DONE
        return answer


def _add_missing_punctuation(raw_str: str, mark: str = '.') -> str:
    """Add a missing punctuation mark to raw_str."""
    if raw_str[-1] not in string.punctuation:
        raw_str = raw_str + mark
    return raw_str


def _cleanup_context(context: str) -> str:
    """Adds context, punctuation and some explanation as to the category."""
    # LOCAL VARIABLES
    new_context = ''             # Cleaned up version of context
    new_preface = 'The player '  # Add this to the beginning
    cleanup_dict = {
        'is presenting a: story': 'is giving clues about the name of a well-known story '
                                  'which could be a book, a movie, etc.',
        'is presenting a: person': 'is giving clues about a specific unique person '
                                   'who could be fictional, real, pop-culture icon, alien, etc.',
        'is presenting a: place': 'is giving clues about a specific, well-known place, real '
                                  'or fictional, that exists in media or the real world.',
        'is presenting a: thing': 'is giving clues about a well-known thing, real or fictional, '
                                  'which could be an object, concept, material, animal, etc.'
    }

    # INPUT VALIDATION
    validate_string(context, 'context', can_be_empty=False)

    # CLEAN IT UP
    new_context = new_preface + context.capitalize()
    for key, value in cleanup_dict.items():
        if key in new_context:
            new_context = new_context.replace(key, value)
            break  # Got one

    # DONE
    return new_context


def _construct_full_describe_prompt(prompt: str, sentence: str, buttons_left: List[str],
                                    buttons_right: List[str] = None,
                                    prev_descr: List[str] = None) -> str:
    """Form the full describe prompt based on extracted data.

    Args:
        prompt: E.g., "Describe detective pikachu"
        sentence: E.g., "It's a story about a _____ _____." (may have one or two blanks)
        buttons_left: ['not', 'tall', 'incredible', 'bad', 'gooey', 'nice', 'boring', 'bright',
                       'recent']
        buttons_right: Optional; Not necessary if sentence only has one blank.
            E.g., ['human', 'place', 'thing', 'circumstance', 'obstacle',
                   'character', 'adventure', 'power', 'duo']
        prev_descr: Optional; Previous descriptions that were already provided.

    Returns:
        A fully formed, AI-engineered, prompt that should be fool-proof (if that's even possible).

    Raises:
        RuntimeError: Detected a mismatch in the number of JITB_FITB_STR and defined button lists.
        TypeError: Bad data type.
        ValueError: Invalid value (e.g., sentence is missing JITB_FITB_STRs).
    """
    # LOCAL VARIABLES
    count = 0           # Number of JITB_FITB_STR found in sentence
    full_prompt = None  # Constructed prompt
    previous = ''       # Dynamically formulated previous descriptions
    # Use this format string if there are any previous descriptions
    prev_format = 'You have already provided the following descriptions: {previous}.'
    # Use this format string if there is one fill-in-the-blank entry in sentence
    single_list = 'Fill in the blank of this sentence by choosing one word from the provided ' \
                  + 'list and providing your answer in this exact format: "word_from_list". ' \
                  + 'Sentence: "{prompt} by filling in the blank of ' \
                  + 'this sentence: {sentence}" {previous} List of choices: {buttons_left}. ' \
                  + 'Provide your answer in this exact format: "word_from_list". ' \
                  + 'For example: "{b_l_choice_1}".'
    # Use this format string if there are two fill-in-the-blank entries in sentence
    double_list = 'Fill in the blanks of this sentence by choosing one word from each list and ' \
                  + 'providing your answer in the format "word_from_first_list, ' \
                  + 'word_from_second_list". Sentence: "{prompt} by filling in the blanks of ' \
                  + 'this sentence: {sentence}" {previous} List for the first blank: ' \
                  + f'{buttons_left}. List for the second blank: {buttons_right}. Provide your ' \
                  + 'answer in this exact format: "word_from_first_list, word_from_second_list". ' \
                  + 'For example: "{b_l_choice_1}, {b_r_choice_1}" or ' \
                  + '"{b_l_choice_2}, {b_r_choice_2}".'

    # INPUT VALIDATION
    validate_string(prompt, 'prompt', can_be_empty=False)
    validate_string(sentence, 'sentence', can_be_empty=False)
    validate_list(buttons_left, 'buttons_left', can_be_empty=False)
    for left_button in buttons_left:
        validate_string(left_button, 'buttons_left entry', can_be_empty=False)
    if buttons_right:
        validate_list(buttons_right, 'buttons_right', can_be_empty=False)
        for right_button in buttons_right:
            validate_string(right_button, 'buttons_right entry', can_be_empty=False)
    if prev_descr:
        validate_list(prev_descr, 'prev_descr', can_be_empty=False)
        for previous in prev_descr:
            validate_string(previous, 'prev_descr entry', can_be_empty=False)
        previous = prev_format.format(previous=', '.join(prev_descr))

    # CONSTRUCT IT
    # Validate the fill-in-the-blanks match the defined button lists
    count = sentence.count(JITB_FITB_STR)
    # NOTE: I removed Exception-based reporting in lieu of race-conditions in which a prompt
    # was partially answered or the game was paused (which means the 'submit' click never
    # completes).
    if 1 == count:
        full_prompt = single_list.format(prompt=prompt.capitalize(), sentence=sentence.capitalize(),
                                         previous=previous, buttons_left=buttons_left,
                                         b_l_choice_1=buttons_left[0])
    elif 2 == count:
        full_prompt = double_list.format(prompt=prompt.capitalize(), sentence=sentence.capitalize(),
                                         previous=previous, buttons_left=buttons_left,
                                         buttons_right=buttons_right,
                                         b_l_choice_1=buttons_left[0],
                                         b_r_choice_1=buttons_right[-1],
                                         b_l_choice_2=buttons_left[-1],
                                         b_r_choice_2=buttons_right[0])
    elif count > 2:
        raise ValueError(f'The sentence argument "{sentence}" has too many {JITB_FITB_STR}s')

    # DONE
    return full_prompt


def _convert_button_text(button_elem: selenium.webdriver.remote.webelement.WebElement) -> List[str]:
    """Convert the text of a 'describe' page button element into a list of strings."""
    return button_elem.text.split('\n')


def _extract_sentence(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
    """"""
    # LOCAL VARIABLES
    sentence = ''  # Extracted sentence
    # The sentence web element
    sentence_web_elem = get_web_element(web_driver=web_driver, by_arg=By.CLASS_NAME,
                                        value='sentence-words')

    # EXTRACT IT
    if sentence_web_elem:
        sentence = _reformat_sentence(sentence_web_elem)

    # DONE
    return sentence


def _reformat_sentence(sentence_elem: selenium.webdriver.remote.webelement.WebElement) -> str:
    """Extract the 'describe' sentence from its web element."""
    # LOCAL VARIABLES
    blank_strs = ['blanky', 'blank', 'something']  # String literals Blather 'Round uses for blanks
    sentence = None                                # The extracted sentence

    # EXTRACT IT
    sentence = sentence_elem.text.replace('\n', ' ')  # The extracted sentence
    for blank_str in blank_strs:
        if blank_str in sentence:
            sentence = sentence.replace(blank_str, JITB_FITB_STR)
    sentence = sentence.capitalize()

    # DONE
    return sentence


def _strip_quotes(quote: str) -> str:
    """Strip matched leading and trailing quotes from a string."""
    # LOCAL VARIABLES
    new_quote = quote        # Newly cleaned up quote
    quote_list = ['"', "'"]  # Quotes to remove

    # INPUT VALIDATION
    validate_string(quote, 'quote', can_be_empty=True)

    # STRIP IT
    if quote:
        for quote_entry in quote_list:
            if new_quote.startswith(quote_entry) and new_quote.endswith(quote_entry):
                new_quote = new_quote[:-1].replace(quote_entry, '', 1)
        if new_quote != quote:
            new_quote = _strip_quotes(quote=new_quote)

    # DONE
    return new_quote
