"""Common functionality for Selenium web drivers and web elements."""

# Standard
from typing import Any, Final, List
# Third Party
from hobo.validation import validate_string, validate_type
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jitb_logger import Logger
from jitb.jitb_misc import convert_str_to_int
from jitb.jitb_validation import validate_web_driver


DEFAULT_BUTTON_BY: Final[str] = By.XPATH        # We find buttons by XPath, by default.
DEFAULT_BUTTON_VALUE: Final[str] = './/button'  # XPath value to find buttons.


def get_buttons(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) \
        -> List[selenium.webdriver.remote.webelement.WebElement]:
    """Get a list of all the button type elements from web_driver starting at the root XPath.

    Args:
        web_driver: Selenium web driver to search for buttons.

    Returns:
        A list of all button WebElements on success.  An empty list if none were found.
    """
    # LOCAL VARIABLES
    button_by = DEFAULT_BUTTON_BY        # Use the XPath to find all the button web elements
    button_value = DEFAULT_BUTTON_VALUE  # XPath value to find all the buttons
    element_list = []                    # List of all the button web elements

    # INPUT VALIDATION
    _validate_wd_input(web_driver=web_driver, by_arg=button_by, value=button_value)

    # GET IT
    element_list = _get_elements(web_thing=web_driver, by_arg=button_by, value=button_value)

    # DONE
    return element_list


def get_sub_buttons(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    sub_by: str = By.ID, sub_value: str = None) \
        -> List[selenium.webdriver.remote.webelement.WebElement]:
    """Get a list of all the button type elements from web_driver starting at a web element.

    Some of these web pages have hidden and/or disabled buttons hidden on the page.
    This function will first get the sub-web element indicated by sub_by and sub_value.  Then,
    it will start searching for the button type elements there.  That way, you can better target
    the buttons you're looking for.

    Args:
        web_driver: Selenium web driver to search for buttons.
        sub_by: Optional; See: help(selenium.webdriver.common.by.By).
        sub_value: Optional; Value of the by_arg-type of web element.

    Returns:
        A list of the button WebElements found at the sub-web element on success.
        An empty list if none were found.
    """
    # LOCAL VARIABLES
    button_by = DEFAULT_BUTTON_BY        # Use the XPath to find all the button web elements
    button_value = DEFAULT_BUTTON_VALUE  # XPath value to find all the buttons
    sub_element = None                   # Element found with sub_by and sub_value
    element_list = []                    # List of all the button web elements

    # INPUT VALIDATION
    _validate_wd_input(web_driver=web_driver, by_arg=sub_by, value=sub_value)

    # GET IT
    # Get the sub web element
    sub_element = _get_element(web_thing=web_driver, by_arg=sub_by, value=sub_value)
    # Get the buttons
    if sub_element:
        element_list = _get_elements(web_thing=sub_element, by_arg=button_by, value=button_value)

    # DONE
    return element_list


def get_sub_element(web_element: selenium.webdriver.remote.webelement.WebElement,
                    by_arg: str = By.ID, value: str = None) \
        -> selenium.webdriver.remote.webelement.WebElement:
    """Get an element from a web element.

    Sometimes you have to get specifically discrete when searching for IDs.

    Args:
        web_driver: Selenium web driver to search for an element.
        by_arg: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by_arg-type of web element.

    Returns:
        A WebElement if found, None otherwise.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid by_arg value.
    """
    # LOCAL VARIABLES
    element = None  # Found selenium.webdriver.remote.webelement.WebElement

    # INPUT VALIDATION
    _validate_we_input(web_element=web_element, by_arg=by_arg, value=value)

    # GET IT
    try:
        element = _get_element(web_thing=web_element, by_arg=by_arg, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_sub_element() getting {by_arg}:{value} raised {repr(err)}!')

    # DONE
    return element


def get_web_element(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    by_arg: str = By.ID, value: str = None) \
        -> selenium.webdriver.remote.webelement.WebElement:
    """Get the value element, of type by_arg, from web_driver.

    Args:
        web_driver: Selenium web driver to search for an element.
        by_arg: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by_arg-type of web element.

    Returns:
        A WebElement if found, None otherwise.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid by_arg value.
    """
    # LOCAL VARIABLES
    element = None  # Found selenium.webdriver.remote.webelement.WebElement

    # INPUT VALIDATION
    _validate_wd_input(web_driver=web_driver, by_arg=by_arg, value=value)

    # GET IT
    try:
        element = _get_element(web_thing=web_driver, by_arg=by_arg, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_web_element() getting {by_arg}:{value} raised {repr(err)}!')

    # DONE
    return element


def get_web_element_int(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                        by_arg: str = By.ID, value: str = None) -> int:
    """Convert the text from the value element, of type by_arg, from web_driver to an int.

    Take care to investigate the return value as 'not None' in case the return value is zero (0).

    Args:
        web_driver: Selenium web driver to search for an element.
        by_arg: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by_arg-type of web element.

    Returns:
        An integer converted from the string, if found.  If a string isn't found or the
        conversion fails, return None.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid by_arg value.
    """
    # LOCAL VARIABLES
    elem_text = None  # Text extracted from element
    elem_int = None   # Integer converted from elem_text

    # INPUT VALIDATION handled by get_web_element_text()

    # GET IT
    try:
        elem_text = get_web_element_text(web_driver=web_driver, by_arg=by_arg, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_web_element_int() getting {by_arg}:{value} raised {repr(err)}!')
    else:
        if elem_text:
            elem_int = convert_str_to_int(elem_text)
            if elem_int is None:
                Logger.debug(f'get_web_element_int() failed to convert {elem_text} to an int')

    # DONE
    return elem_int


def get_web_element_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                         by_arg: str = By.ID, value: str = None) -> str:
    """Extract the text from the value element, of type by_arg, from web_driver.

    Args:
        web_driver: Selenium web driver to search for an element.
        by_arg: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by_arg-type of web element.

    Returns:
        A string, which could be empty, if found.  None otherwise.

    Raises:
        TypeError: Bad data type.
        ValueError: Invalid by_arg value.
    """
    # LOCAL VARIABLES
    element = None    # Found selenium.webdriver.remote.webelement.WebElement
    elem_text = None  # Text extracted from element

    # INPUT VALIDATION handled by get_web_element()

    # GET IT
    try:
        element = get_web_element(web_driver=web_driver, by_arg=by_arg, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_web_element_text() getting {by_arg}:{value} raised {repr(err)}!')
    else:
        if element:
            elem_text = element.text

    # DONE
    return elem_text


def _get_element(web_thing: Any, by_arg: str = By.ID, value: str = None) \
        -> selenium.webdriver.remote.webelement.WebElement:
    """Find an element, in web_thing, if the find_element method exists.

    Does not validate input other than verifying web_thing.find_element() exists.

    Args:
        web_thing: Basically, any object that has a find_element method.  This private function
            was written with the Selenium WebDriver and WebElement in mind.
        by_arg: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by_arg-type of web element.

    Returns:
        A WebElement if found, None otherwise.
    """
    # LOCAL VARIABLES
    element = None              # Found selenium.webdriver.remote.webelement.WebElement
    attr_name = 'find_element'  # The attribute in question
    get_it = None               # Found attribute

    # INPUT VALIDATION
    if web_thing and hasattr(web_thing, attr_name):
        get_it = getattr(web_thing, attr_name)
        if callable(get_it):
            try:
                element = get_it(by=by_arg, value=value)
            except NoSuchElementException:
                pass  # Too verbose in the debug log
            except StaleElementReferenceException as err:
                Logger.debug(f'_get_element() {by_arg}:{value} raised {repr(err)}!')

    # DONE
    return element


def _get_elements(web_thing: Any, by_arg: str = By.ID, value: str = None) \
        -> List[selenium.webdriver.remote.webelement.WebElement]:
    """Find an element, in web_thing, if the find_elements method exists.

    Does not validate input other than verifying web_thing.find_elements() exists.

    Args:
        web_thing: Basically, any object that has a find_element method.  This private function
            was written with the Selenium WebDriver and WebElement in mind.
        by_arg: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by_arg-type of web element.

    Returns:
        A list of any WebElements found, empty list otherwise.
    """
    # LOCAL VARIABLES
    elements = []                # Found selenium.webdriver.remote.webelement.WebElement
    attr_name = 'find_elements'  # The attribute in question
    get_it = None                # Found attribute

    # INPUT VALIDATION
    if web_thing and hasattr(web_thing, attr_name):
        get_it = getattr(web_thing, attr_name)
        if callable(get_it):
            try:
                elements = get_it(by=by_arg, value=value)
            except (NoSuchElementException, StaleElementReferenceException) as err:
                Logger.debug(f'_get_elements() {by_arg}:{value} raised {repr(err)}!')
    else:
        Logger.debug(f'_get_elements() reports the web thing had no attr {attr_name}!')

    # DONE
    return elements


def _validate_common_args(by_arg: str, value: str) -> None:
    """Validate the cross-section of this module's API functions."""
    # INPUT VALIDATION
    # by_arg
    validate_string(by_arg, 'by_arg', can_be_empty=False)
    if not hasattr(By, by_arg.replace(' ', '_').upper()):
        raise ValueError(f'Invalid by_arg value of {by_arg}.  Use By value from '
                         'the selenium.webdriver.common.by module')
    # value
    if value is not None:
        validate_string(value, 'value', can_be_empty=True)


def _validate_wd_input(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                       by_arg: str, value: str) -> None:
    """Validate the input on behalf of API functions in this module."""
    # INPUT VALIDATION
    # web_driver
    validate_web_driver(web_driver=web_driver)
    _validate_common_args(by_arg=by_arg, value=value)


def _validate_we_input(web_element: selenium.webdriver.remote.webelement.WebElement,
                       by_arg: str, value: str) -> None:
    """Validate the input on behalf of API functions in this module."""
    # INPUT VALIDATION
    # web_element
    validate_type(web_element, 'web_element', selenium.webdriver.remote.webelement.WebElement)
    _validate_common_args(by_arg=by_arg, value=value)
