"""Defines the package's Jackbox Games Quiplash 2 class."""

# Standard
from typing import Final, List
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
from jitb.jitb_webdriver import (click_a_button, get_prompt, get_char_limit_attr, get_vote_text,
                                 is_prompt_page, is_vote_page, vote_answers, write_an_answer)


DEFAULT_CHAR_LIMIT: Final[int] = 45  # Default maximum character limit


class JbgQ2(JbgAbc):
    """Jackbox Games (JBG) Quiplash 2 (Q2) class."""

    # Methods are listed in expected 'call order'.
    def __init__(self, ai_obj: JitbAi, username: str) -> None:
        """JbgQ2 ctor.

        Args:
            ai_obj:  OpenAI API interface to use in this game.
            username:  The screen name used in this game.
        """
        ai_obj.change_system_content('You are a witty person trying to win the Jackbox Game '
                                     'Quiplash 2')
        super().__init__(ai_obj=ai_obj, username=username)
        self._prompt_clues = None  # Prompt page clues
        self._last_lash_clues = None  # Thriplash page clues
        # Vote page clues
        self._vote_clues = ['Which one do you like more?', 'Now award your silver medal',
                            'And hand out a bronze medal to your third favorite']
        # Helps differentiate between regular prompts and the Round 3 'Last Lash' prompt
        self._normal_prompt_clues = ['SEND SAFETY QUIP']  # This does not appears on the Last Lash
        # A 'needle' to help differentiate a Comic Lash from the other Round 3 'Last Last' examples.
        self._comic_lash_clues = ['   SEND']  # Only the Comic Last Lash seems to get this

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
        self._answer_last_lash(web_driver=web_driver)

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
        if not self.is_vote_page(web_driver=web_driver):
            raise RuntimeError('This is not a voting page.')

        # VOTE IT
        while True:
            if not self.is_vote_page(web_driver):
                break
            prompt_text = vote_answers(web_driver=web_driver, last_prompt=prompt_text,
                                       ai_obj=self._ai_obj, element_name='vote-text',
                                       element_type=By.ID, vote_clues=self._vote_clues,
                                       clean_string=True)
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
        elif self.is_prompt_page(web_driver=web_driver):
            current_page = JbgPageIds.ANSWER
        elif self.is_last_lash_page(web_driver=web_driver):
            current_page = JbgPageIds.Q2_LAST
        elif self._is_login_page(web_driver=web_driver):
            current_page = JbgPageIds.LOGIN

        # DONE
        if current_page != JbgPageIds.UNKNOWN:
            Logger.debug(f'This is a(n) {current_page.name} page!')
        return current_page

    # Public Methods (alphabetical order)
    def get_char_limit(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> int:
        """Wraps jitb_webdriver.get_char_limit_attr with game-specific details."""
        # LOCAL VARIABLES
        char_limit = None                   # Character limit for the prompt
        field_id = 'quiplash-answer-input'  # By.ID name of the input field
        attr_name = 'maxlength'             # The attribute name to fetch from the field_id element

        # GET LIMIT
        # Get Web Element
        char_limit = get_char_limit_attr(web_driver=web_driver, element_name=field_id,
                                         attr_name=attr_name, element_type=By.ID)
        print(f'THE CHAR LIMIT FOR THIS PAGE IS: {char_limit}')
        # Did it work?  If not, use the default.
        if char_limit is None:
            char_limit = DEFAULT_CHAR_LIMIT

        # DONE
        return char_limit

    def get_prompt(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   prompt_clues: List[str] = None, clean_string: bool = True) -> str:
        """Wraps jitb_webdriver.get_prompt with game-specific details.

        Returns:
            The prompt split into a list by newlines.
        """
        return get_prompt(web_driver=web_driver, element_name='question-text', element_type=By.ID,
                          prompt_clues=prompt_clues, clean_string=clean_string)

    def get_last_lash_prompt(self,
                             web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
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
        prompt_text = ''                  # The prompt's text as a string
        prompt_list = []                  # Use this to cleanup the text

        # INPUT VALIDATION
        prompt_text = get_prompt(web_driver=web_driver, element_name='state-answer-question',
                                 element_type=By.ID, prompt_clues=self._last_lash_clues)

        # CLEAN IT UP
        prompt_list = prompt_text.split('\n')[:2]  # Testing shows we only care about the first two
        prompt_text = ' '.join(prompt_list)  # Put it back together into one string

        # DONE
        return prompt_text

    def get_vote_text(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                      vote_clues: List[str] = None, clean_string: bool = True) -> str:
        """Wraps jitb_webdriver.get_vote_text with game-specific details.

        Returns:
            The prompt split into a list by newlines.
        """
        return get_vote_text(web_driver=web_driver, element_name='state-vote', element_type=By.ID,
                             vote_clues=vote_clues, clean_string=clean_string)

    def is_last_lash_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Determine if this is the Round 3 Last Lash prompt page.

        One (seemingly) easy way to differentiate between the Last Lash prompt and the Round 1 & 2
        prompts is that you can't Safety Quip on the Last Lash.  This function's logic is:
        If web_driver is a prompt_page and 'SEND SAFETY QUIP' is *not* in the text, it's a
        Last Lash prompt.

        Returns:
            True if this is a regular prompt screen, False otherwise.
        """
        # LOCAL VARIABLES
        element_name = 'state-answer-question'  # The web element value to search for
        last_lash_page = False                  # Prove this true if you can

        # IS IT?
        if is_prompt_page(web_driver=web_driver, element_name=element_name, element_type=By.ID,
                          prompt_clues=self._prompt_clues, clean_string=False) and not \
           is_prompt_page(web_driver=web_driver, element_name=element_name, element_type=By.ID,
                          prompt_clues=self._normal_prompt_clues, clean_string=False):
            last_lash_page = True

        # DONE
        return last_lash_page

    def is_prompt_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Determine if this is a round 1 or 2 prompt page.

        Returns:
            True if this is a regular prompt screen, False otherwise.
        """
        # LOCAL VARIABLES
        element_name = 'state-answer-question'  # The web element value to search for
        prompt_page = False                     # Prove this true

        # IS IT?
        if is_prompt_page(web_driver=web_driver, element_name=element_name, element_type=By.ID,
                          prompt_clues=self._prompt_clues, clean_string=False) and \
            is_prompt_page(web_driver=web_driver, element_name=element_name, element_type=By.ID,
                           prompt_clues=self._normal_prompt_clues, clean_string=False):
            prompt_page = True

        # DONE
        return prompt_page

    def is_vote_page(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
        """Determine if this is this a round 1 or 2 vote page.

        Returns:
            True if this is a regular vote screen, False otherwise.
        """
        return is_vote_page(web_driver=web_driver, element_name='vote-text', element_type=By.ID,
                            vote_clues=self._vote_clues, clean_string=False)

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
            clicked_it = click_a_button(web_driver=web_driver, button_str='SEND')

        # DONE
        return clicked_it

    def write_an_answer(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                        submit_text: str) -> bool:
        """Wraps jitb_webdriver.write_an_answer with game-specific details."""
        return write_an_answer(web_driver=web_driver, submit_text=submit_text,
                               element_name='quiplash-answer-input', element_type=By.ID)

    # Private Methods (alphabetical order)
    def _answer_last_lash(self, web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
        """Generate an answer for the Last Lash (Round 3) prompt."""
        # LOCAL VARIABLES
        prompt_text = ''    # Input prompt
        answer = ''         # Answer generated by OpenAI
        clicked_it = False  # Keep track of whether this prompt was answered or not
        # Replacement prompt when a Comic Lash is detected
        comic_text = 'The other players are being shown a picture you can not see. ' \
            + 'It is a generic web comic with the text removed from the speech bubble ' \
            + 'of the last panel.  Give an answer that is generic enough to ' \
            + 'work as funny/quirky text for such an empty speech bubble.'

        # INPUT VALIDATION
        if not self.is_last_lash_page(web_driver=web_driver):
            raise RuntimeError('This is not the Last Lash prompt page')

        # ANSWER IT
        # prompt_text = get_prompt(web_driver=web_driver)
        prompt_text = self.get_last_lash_prompt(web_driver=web_driver)
        if self._comic_lash_clues[0].lower() in prompt_text.lower():
            Logger.debug(f'It appears we have encountered a Comic Last because the "{prompt_text}" '
                         f'is being repaced with "{comic_text}"')
            prompt_text = comic_text
        answer = self.generate_ai_answer(prompt_text, ai_obj=self._ai_obj,
                                         length_limit=self.get_char_limit(web_driver=web_driver))
        clicked_it = self.submit_an_answer(web_driver=web_driver, submit_text=answer)

        # DONE
        if not clicked_it:
            raise RuntimeError('Did not answer the Last Lash prompt')
        Logger.debug(f'Answered Last Lash prompt "{prompt_text}" with: "{answer}"!')

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
