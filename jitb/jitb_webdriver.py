"""Defines common use webdriver functionality for the package.

The functions defined in this module represent common functionality utilized by the classes
defined in the jitb.jbgames module.
"""


# Standard
# Third Party
from selenium.webdriver.common.by import By
# Local
from jitb.jitb_selenium import get_web_element_text


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
            finally:
                break

    # DONE
    return clicked_it


def get_button_choices(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> Dict[str:str]:
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


def get_char_limit(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   element_name: str, element_type: selenium.webdriver.common.by.By,) -> int:
    """Get the character limit for an input field.

    Searches web_driver for element_name using element_type and attemtps to convert the value
    to an integer.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., charRemaining).
        element_type: The prompt's element type (e.g., By.CLASS_NAME).
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

    # TESTING
    # test_value = get_web_element_text(web_driver=web_driver, by_arg=By.CLASS_NAME,
    #                                   value='charRemaining')

    # DONE
    return char_limit


def get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
               element_name: str, element_type: selenium.webdriver.common.by.By,
               prompt_clues: List[str] = None) -> str:
    """Get the raw prompt text from the element_name web element using the By type of element_type.

    If non-standard characters are an issue, use a clean_*() function from jitb_misc.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., prompt).
        element_type: The prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        prompt_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used by is_prompt_page() to positively identify web_driver as
            one of your specific prompt page examples.
            E.g., ['Write a definition', 'Write a synonym', 'Write a sentence']

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
                          element_type=element_type, prompt_clues=prompt_clues):
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

    # DONE
    return prompt_text


def get_vote_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                  element_name: str, element_type: selenium.webdriver.common.by.By,
                  vote_clues: List[str] = None) -> str:
    """Get the raw vote text from the element_name web element using the By type of element_type.

    If non-standard characters are an issue, use a clean_*() function from jitb_misc.

    Args:
        web_driver: The web driver to get the vote prompt from.
        element_name: The vote prompt's element name (e.g., prompt).
        element_type: The vote prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        vote_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used by is_vote_page() to positively identify web_driver as
            one of your specific vote page examples.
            E.g., ['Vote your favorite definition', 'Vote your favorite synonym']

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
    if not is_vote_page(web_driver, check_needles=check_needles):
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

    # DONE
    return vote_text


def is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   element_name: str, element_type: selenium.webdriver.common.by.By,
                   prompt_clues: List[str] = None) -> bool:
    """Determine if web_driver is a prompt page.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., prompt).
        element_type: The prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        prompt_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used to positively identify web_driver as
            one of your specific prompt page examples.
            E.g., ['Write a definition', 'Write a synonym', 'Write a sentence']

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    prompt_page = False  # Prove this true

    # INPUT VALIDATION handled by _is_page()

    # IS IT?
    prompt_page = _is_page(web_driver=web_driver, element_name=element_name,
                           element_type=element_type, clues=prompt_clues)

    # DONE
    return prompt_page


def is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                 element_name: str, element_type: selenium.webdriver.common.by.By,
                 vote_clues: List[str] = None) -> bool:
    """Determine if web_driver is a vote page.

    Args:
        web_driver: The web driver to get the prompt from.
        element_name: The prompt's element name (e.g., prompt).
        element_type: The prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        vote_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used to positively identify web_driver as
            one of your specific vote page examples.
            E.g., ['Vote your favorite definition', 'Vote your favorite synonym']

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    vote_page = False  # Prove this true

    # INPUT VALIDATION handled by _is_page()

    # IS IT?
    vote_page = _is_page(web_driver=web_driver, element_name=element_name,
                         element_type=element_type, clues=prompt_clues)

    # DONE
    return vote_page


def vote_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                element_name: str, element_type: selenium.webdriver.common.by.By,
                last_prompt: str, ai_obj: JitbAi, vote_clues: List[str] = None) -> str:
    """Generate votes for other players prompts.

    Args:
        web_driver: The web driver to get the vote prompt from.
        element_name: The vote prompt's element name (e.g., prompt).
        element_type: The vote prompt's element type (e.g., By.ID).
            See: help(selenium.webdriver.common.by.By).
        vote_clues: Optional; A list of strings expected to be associated with element_name.
            These clues will be used by is_vote_page() to positively identify web_driver as
            one of your specific vote page examples.
            E.g., ['Vote your favorite definition', 'Vote your favorite synonym']

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

    # INPUT VALIDATION
    # All other arguments validated by calls to other module functions
    _validate_string(string=last_prompt, name='last_prompt', may_be_empty=True)
    if not isinstance(ai_obj, JitbAi):
        raise TypeError(f'Invalid type of {type(ai_obj)} for ai_obj argument')

    # WAIT FOR IT
    for _ in range(num_loops):
        try:
            prompt_text = get_vote_text(web_driver=web_driver, element_name=element_name,
                                        element_type=element_type, vote_clues=vote_clues)
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
        choice_list = [button for button in button_dict.keys() if button]
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
        Logger.debug(f'Chose "{favorite}" for "{prompt_text.replace('\n', ' ')}"!')
    return prompt_text


def write_an_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    element_name: str, element_type: selenium.webdriver.common.by.By,
                    submit_text: str) -> bool:
    """Standardize the way keys are sent to text fields.

    Args:
        web_driver: The webdriver object to interact with.
        element_name: The field's element name (e.g., input-text-textarea).
        element_type: The field's element type (e.g., By.ID).
        submit_text: The text to enter into field_str.

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
             element_name: str, element_type: selenium.webdriver.common.by.By,
             clues: List[str] = None) -> bool:
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
    _validate_prompt_clues(prompt_clues=clues)

    # IS IT?
    try:
        temp_text = get_web_element_text(web_driver=web_driver, by_arg=element_type,
                                         value=element_name)
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


def _validate_element_type(element_type: selenium.webdriver.common.by.By) -> None:
    """Validate element_type arguments on behalf of this module."""
    if not isinstance(element_type, selenium.webdriver.common.by.By):
        raise TypeError(f'The element_type data type of {type(element_type)} is invalid')


def _validate_prompt_clues(prompt_clues: List[str] = None) -> None:
    """Validate prompt_clues arguments on behalf of this module.

    Args:
        prompt_clues: May be None.  May also be an empty list.  However, any entry in the list
            must be a non-empty string.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid value.
    """
    if isinstance(prompt_clues, list):
        for prompt_clue in prompt_clues:
            _validate_string(prompt_clue, 'prompt_clues list entry', may_be_empty=False)
    elif prompt_clues:
        raise TypeError(f'Invalid data type for prompt_clues: {prompt_clues} '
                        f'(Type: {type(prompt_clues)})')


def _validate_string(string: str, name: str, may_be_empty: bool = False) -> None:
    """Validates strings on behalf of this module.

    Args:
        string: The value of the string to check.
        name: The name of the original arugment being validated (used in exception messages).
        may_be_empty: Optional; If True, string may not be empty.
    """
    if not isinstance(string, str):
        raise TypeError(f'The {name} value must be a string instead of type {type(string)}')
    elif not string and not may_be_empty:
        raise ValueError(f'The {name} may not be empty')


def _validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Validate a web driver."""
    if not web_driver:
        raise TypeError('Web driver can not be of type None')
    if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
        raise TypeError(f'Invalid web_driver data type of {type(web_driver)}')
