"""Defines common use webdriver functionality for the package.

The functions defined in this module represent common functionality utilized by the classes
defined in the jitb.jbgames module.
"""


# Standard
from typing import Dict, List
import time
# Third Party
from selenium.common.exceptions import (ElementNotInteractableException, NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jitb_globals import JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_misc import clean_up_string
from jitb.jitb_openai import JitbAi
from jitb.jitb_selenium import (get_buttons, get_web_element, get_web_element_int,
                                get_web_element_text)


# Public Module Functions
def click_a_button(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
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
            break

    # DONE
    return clicked_it


def get_button_choices(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> Dict[str, str]:
    """Get a list of all the button text fields from web_driver starting at the root XPath.

    Args:
        web_driver: Selenium web driver to search for buttons.

    Returns:
        A dictionary of all button text fields on success.  Each dict key is the sanitized button
        name but the value is the actual button name.  Returns an empty dict if none were found.
    """
    # LOCAL VARIABLES
    button_elements = []  # List of button web elements extracted from web_driver
    enabled_buttons = []  # List of enabled button web elements extracted from button_elements
    button_choices = {}   # Dictionary of button_names:button_text extracted from enabled_buttons

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)

    # GET CHOICES
    # Get Buttons
    button_elements = get_buttons(web_driver=web_driver)
    # Only Choose Enabled Buttons
    enabled_buttons = [button for button in button_elements if button.is_enabled()]
    # Extract Text
    for enabled_button in enabled_buttons:
        if enabled_button.text:
            temp_text = enabled_button.text.strip('\n')
            button_choices[temp_text] = enabled_button.text

    # DONE
    return button_choices


def get_char_limit(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   element_name: str, element_type: str = By.CLASS_NAME) -> int:
    """Get the character limit for an input field.

    Searches web_driver for element_name using element_type and attempts to convert the value
    to an integer.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., charRemaining).
        element_type: Optional; The prompt's element type (e.g., By.CLASS_NAME).
            See: help(selenium.webdriver.common.by.By).

    Returns:
        The integer value for element_name as read from web_driver.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid value.
    """
    # LOCAL VARIABLES
    char_limit = None  # Character limit read from the input prompt

    # INPUT VALIDATION handled by get_web_element_int()

    # GET LIMIT
    char_limit = get_web_element_int(web_driver=web_driver, by_arg=element_type, value=element_name)

    # DONE
    return char_limit


def get_char_limit_attr(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                        element_name: str, attr_name: str, element_type: str = By.ID) -> int:
    """Get the character limit for an input field from its attribute.

    Searches web_driver for element_name using element_type, reads the given attribute,
    and attempts to convert the value to an integer.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., quiplash-answer-input).
        attr_name: The attribute name to read from element name (e.g., maxlength).
        element_type: Optional; The field's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).

    Returns:
        The integer value for element_name's attr_name attribute as read from web_driver on succes,
        None on failure.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid value.
    """
    # LOCAL VARIABLES
    web_element = None  # The web element to read the attribute from
    attr_string = None  # The attribute string read from web_element
    char_limit = None   # Character limit read from the input prompt

    # INPUT VALIDATION handled by get_web_element_int()

    # GET IT
    # Get Web Element
    web_element = get_web_element(web_driver=web_driver, by_arg=element_type, value=element_name)
    # Get Attribute
    if web_element:
        attr_string = web_element.get_attribute(attr_name)

    # GET LIMIT
    if attr_string:
        char_limit = convert_str_to_int(attr_string)

    # DONE
    return char_limit


def get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
               element_name: str, element_type: str = By.ID,
               prompt_clues: List[str] = None, clean_string: bool = False) -> str:
    """Get the raw prompt text from the element_name web element using the By type of element_type.

    If non-standard characters are an issue, use a clean_*() function from jitb_misc.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., prompt).
        element_type: Optional; The prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        prompt_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used by is_prompt_page() to positively identify web_driver as
            one of your specific prompt page examples.
            E.g., ['Write a definition', 'Write a synonym', 'Write a sentence']
        clean_string: Optional; Call clean_up_string() on the text prior to vote_clue-evaluation.
            (Sometimes, the strings have non-standard characters in them.)

    Returns:
        The prompt text for element_name as read from web_driver.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a prompt page.
        TypeError: Bad data type.
        ValueError: Invalid value.
    """
    # LOCAL VARIABLES
    prompt_text = ''  # element_name's text as a string

    # INPUT VALIDATION
    if not is_prompt_page(web_driver=web_driver, element_name=element_name,
                          element_type=element_type, prompt_clues=prompt_clues,
                          clean_string=clean_string):
        raise RuntimeError('This is not a prompt page')

    # GET IT
    try:
        prompt_text = get_web_element_text(web_driver=web_driver, by_arg=element_type,
                                           value=element_name)
    except (RuntimeError, TypeError, ValueError) as err:
        raise RuntimeError(f'The call to get_web_element_text() for the {element_name} element '
                           f'value failed with {repr(err)}') from err
    else:
        if prompt_text is None:
            raise RuntimeError(f'Unable to locate the {element_name} element value')
        if not prompt_text:
            raise RuntimeError(f'Did not detect any text using the {element_name} element value')
        if clean_string:
            prompt_text = clean_up_string(dirty_string=prompt_text)

    # DONE
    return prompt_text


def get_vote_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                  element_name: str, element_type: str = By.ID,
                  vote_clues: List[str] = None, clean_string: bool = False) -> str:
    """Get the raw vote text from the element_name web element using the By type of element_type.

    If non-standard characters are an issue, use a clean_*() function from jitb_misc.

    Args:
        web_driver: The web driver to get the vote prompt from.
        element_name: The vote prompt's element name (e.g., prompt).
        element_type: Optional; The vote prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        vote_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used by is_vote_page() to positively identify web_driver as
            one of your specific vote page examples.
            E.g., ['Vote your favorite definition', 'Vote your favorite synonym']
        clean_string: Optional; Call clean_up_string() on the text prior to vote_clue-evaluation.
            (Sometimes, the strings have non-standard characters in them.)

    Returns:
        The vote text for element_name as read from web_driver.

    Raises:
        RuntimeError: No prompts found or web_driver isn't a vote page.
        TypeError: Bad data type.
        ValueError: Invalid value.
    """
    # LOCAL VARIABLES
    vote_text = ''  # The full vote prompt

    # INPUT VALIDATION
    if not is_vote_page(web_driver=web_driver, element_name=element_name,
                        element_type=element_type, vote_clues=vote_clues,
                        clean_string=clean_string):
        raise RuntimeError('This is not a vote page')

    # GET THEM
    try:
        vote_text = get_web_element_text(web_driver=web_driver, by_arg=element_type,
                                         value=element_name)
    except (RuntimeError, TypeError, ValueError) as err:
        raise RuntimeError(f'The call to get_web_element_text() for the {element_name} element '
                           f'value failed with {repr(err)}') from err
    else:
        if vote_text is None:
            raise RuntimeError(f'Unable to locate the {element_name} element value')
        if not vote_text:
            raise RuntimeError(f'Did not detect any text using the {element_name} element value')
        if clean_string:
            vote_text = clean_up_string(dirty_string=vote_text)

    # DONE
    return vote_text


def is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   element_name: str, element_type: str = By.ID,
                   prompt_clues: List[str] = None, clean_string: bool = False) -> bool:
    """Determine if web_driver is a prompt page.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., prompt).
        element_type: Optional; The prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        prompt_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used to positively identify web_driver as
            one of your specific prompt page examples.
            E.g., ['Write a definition', 'Write a synonym', 'Write a sentence']
        clean_string: Optional; Call clean_up_string() on the text prior to vote_clue-evaluation.
            (Sometimes, the strings have non-standard characters in them.)

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    prompt_page = False  # Prove this true

    # INPUT VALIDATION handled by _is_page()

    # IS IT?
    prompt_page = _is_page(web_driver=web_driver, element_name=element_name,
                           element_type=element_type, clues=prompt_clues, clean_string=clean_string)

    # DONE
    return prompt_page


def is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                 element_name: str, element_type: str = By.ID,
                 vote_clues: List[str] = None, clean_string: bool = False) -> bool:
    """Determine if web_driver is a vote page.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., prompt).
        element_type: Optional; The prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        vote_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used to positively identify web_driver as
            one of your specific vote page examples.
            E.g., ['Vote your favorite definition', 'Vote your favorite synonym']
        clean_string: Optional; Call clean_up_string() on the text prior to vote_clue-evaluation.
            (Sometimes, the strings have non-standard characters in them.)

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    vote_page = False  # Prove this true

    # INPUT VALIDATION handled by _is_page()

    # IS IT?
    vote_page = _is_page(web_driver=web_driver, element_name=element_name,
                         element_type=element_type, clues=vote_clues, clean_string=clean_string)

    # DONE
    return vote_page


# pylint: disable = too-many-arguments
def vote_answers(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                 last_prompt: str, ai_obj: JitbAi,
                 element_name: str, element_type: str = By.ID, vote_clues: List[str] = None,
                 clean_string: bool = False) -> str:
    """Generate votes for other players prompts.

    Args:
        web_driver: The web driver to get the vote prompt from.
        last_prompt: The last prompt that was answered.  Helps this function avoid trying to
            answer the same prompt twice.
        ai_obj: The JitbAi object to use.
        element_name: The vote prompt's element name (e.g., prompt).
        element_type: Optional; The vote prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        vote_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used by is_vote_page() to positively identify web_driver as
            one of your specific vote page examples.
            E.g., ['Vote your favorite definition', 'Vote your favorite synonym']
        clean_string: Optional; Call clean_up_string() on the text prior to vote_clue-evaluation.
            (Sometimes, the strings have non-standard characters in them.)

    Returns:
        The prompt that was answered as a string.

    Raises:
        RuntimeError: The prompt wasn't answered.
    """
    # LOCAL VARIABLES
    prompt_text = ''    # Input prompt
    clicked_it = False  # Keep track of whether this prompt was answered or not
    num_loops = 5       # Number of attempts to wait for a new prompt
    choice_list = []    # List of possible answers
    favorite = ''       # OpenAI's favorite answer
    button_dict = {}    # Sanitized text are the keys and actual button text are the values
    temp_text = ''      # Temp veriable

    # INPUT VALIDATION
    # All other arguments validated by calls to other module functions
    _validate_string(string=last_prompt, name='last_prompt', may_be_empty=True)
    if not isinstance(ai_obj, JitbAi):
        raise TypeError(f'Invalid type of {type(ai_obj)} for ai_obj argument')

    # WAIT FOR IT
    for _ in range(num_loops):
        try:
            prompt_text = get_vote_text(web_driver=web_driver, element_name=element_name,
                                        element_type=element_type, vote_clues=vote_clues,
                                        clean_string=clean_string)
            if prompt_text and prompt_text != last_prompt:
                break  # Found a new one... let's vote it
            if not is_vote_page(web_driver=web_driver, element_name=element_name,
                                element_type=element_type, vote_clues=vote_clues):
                prompt_text = ''  # This isn't a vote page
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
        button_dict = get_button_choices(web_driver=web_driver)
        if button_dict:
            choice_list = [button for button, _ in button_dict.items() if button]
            # Ask the AI
            favorite = ai_obj.vote_favorite(prompt=prompt_text, answers=choice_list)
            # Click it
            clicked_it = click_a_button(web_driver=web_driver, button_str=button_dict[favorite])
    else:
        prompt_text = ''  # Nothing got answered

    # DONE
    if prompt_text and prompt_text != last_prompt and not clicked_it:
        raise RuntimeError('Did not vote an answer')
    if clicked_it:
        temp_text = prompt_text.replace('\n', ' ')
        Logger.debug(f'Chose "{favorite}" for "{temp_text}"!')
    return prompt_text
# pylint: enable = too-many-arguments


def write_an_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    submit_text: str, element_name: str, element_type: str = By.ID) -> bool:
    """Standardize the way keys are sent to text fields.

    Args:
        web_driver: The webdriver object to interact with.
        submit_text: The text to enter into field_str.
        element_name: The field's element name (e.g., input-text-textarea).
        element_type: Optional; The field's element type (e.g., By.ID).

    Returns:
        True if successful, False otherwise.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid by_arg value.
    """
    # LOCAL VARIABLES
    wrote_it = False  # Return value

    # SUBMIT IT
    prompt_input = get_web_element(web_driver=web_driver, by_arg=element_type, value=element_name)
    if prompt_input:
        try:
            prompt_input.send_keys(submit_text)
        except ElementNotInteractableException as err:
            Logger.debug(f'Failed to submit "{submit_text}" into "{element_name}" with {repr(err)}')
        else:
            wrote_it = True
    else:
        Logger.debug(f'Unable to locate "{element_name}" by {element_type}')

    # DONE
    return wrote_it


# Private Module Functions
def _is_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
             element_name: str, element_type: str = By.ID,
             clues: List[str] = None, clean_string: bool = False) -> bool:
    """Determine if web_driver is the page you think it is.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The element name to search for.
        element_type: The way to search for element_name.
            See: help(selenium.webdriver.common.by.By).
        clues: Optional; A list of strings expected to be associated with element_name.
            If defined, these clues will be used to positively identify web_driver as
            one of your specific page examples.
            E.g., ['Write a definition', 'Write a synonym', 'Write a sentence']
        clean_string: Optional; Call clean_up_string() on the text prior to vote_clue-evaluation.
            (Sometimes, the strings have non-standard characters in them.)

    Returns:
        True if this is the screen you think it is, False otherwise.
    """
    # LOCAL VARIABLES
    page = False    # Prove this true
    temp_text = ''  # Text from the web element

    # INPUT VALIDATION
    _validate_web_driver(web_driver=web_driver)
    _validate_string(element_name, 'element_name', may_be_empty=False)
    _validate_element_type(element_type=element_type)
    _validate_clues(clues=clues)
    _validate_bool(clean_string, 'clean_string')

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver=web_driver, by_arg=element_type,
                                         value=element_name)
        if clean_string:
            temp_text = clean_up_string(dirty_string=temp_text)
        if temp_text:
            if isinstance(clues, list):
                for clue in clues:
                    if clue.lower() in temp_text.lower():
                        page = True  # If we made it here, it's a prompt page
                        break  # Found one.  Stop looking.
            else:
                page = True  # Far enough
    except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
        pass  # Not a prompt page

    # DONE
    return page


def _validate_bool(value: str, name: str) -> None:
    """Validates boolean values on behalf of this module.

    Args:
        value: The variable to check.
        name: The name of the original arugment being validated (used in exception messages).
    """
    if not isinstance(value, bool):
        raise TypeError(f'The {name} value must be a string instead of type {type(value)}')


def _validate_clues(clues: List[str] = None) -> None:
    """Validate *_clues arguments on behalf of this module.

    Args:
        clues: May be None.  May also be an empty list.  However, any entry in the list
            must be a non-empty string.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid value.
    """
    if isinstance(clues, list):
        for clue in clues:
            _validate_string(clue, 'clues list entry', may_be_empty=False)
    elif clues:
        raise TypeError(f'Invalid data type for clues: {clues} '
                        f'(Type: {type(clues)})')


def _validate_element_type(element_type: str) -> None:
    """Validate element_type arguments on behalf of this module."""
    _validate_string(element_type, 'element_type', may_be_empty=False)


def _validate_string(string: str, name: str, may_be_empty: bool = False) -> None:
    """Validates strings on behalf of this module.

    Args:
        string: The value of the string to check.
        name: The name of the original arugment being validated (used in exception messages).
        may_be_empty: Optional; If True, string may not be empty.
    """
    if not isinstance(string, str):
        raise TypeError(f'The {name} value must be a string instead of type {type(string)}')
    if not string and not may_be_empty:
        raise ValueError(f'The {name} may not be empty')


def _validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Validate a web driver."""
    if not web_driver:
        raise TypeError('Web driver can not be of type None')
    if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
        raise TypeError(f'Invalid web_driver data type of {type(web_driver)}')
