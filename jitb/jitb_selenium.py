"""Common functionality for Selenium web drivers and web elements."""

# Standard
from typing import Any, Final
import time
# Third Party
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jitb_logger import Logger


def get_sub_element(web_element: selenium.webdriver.remote.webelement.WebElement,
                    by: str = By.ID, value: str = None) \
    -> selenium.webdriver.remote.webelement.WebElement:
    """Get an element from a web element.

    Sometimes you have to get specifically discrete when searching for IDs.

    Args:
        web_driver: Selenium web driver to search for an element.
        by: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by-type of web element.

    Returns:
        A WebElement if found, None otherwise.
    """
    # LOCAL VARIABLES
    element = None  # Found selenium.webdriver.remote.webelement.WebElement

    # INPUT VALIDATION
    _validate_we_input(web_element=web_element, by=by, value=value)

    # GET IT
    try:
        element = _get_element(web_thing=web_element, by=by, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_element() getting {by}:{value} raised {repr(err)}!')

    # DONE
    return element


def get_web_element(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                    by: str = By.ID, value: str = None) \
    -> selenium.webdriver.remote.webelement.WebElement:
    """Get the value element, of type by, from web_driver.

    Args:
        web_driver: Selenium web driver to search for an element.
        by: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by-type of web element.

    Returns:
        A WebElement if found, None otherwise.
    """
    # LOCAL VARIABLES
    element = None  # Found selenium.webdriver.remote.webelement.WebElement

    # INPUT VALIDATION
    _validate_wd_input(web_driver=web_driver, by=by, value=value)

    # GET IT
    try:
        element = _get_element(web_thing=web_driver, by=by, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_web_element() getting {by}:{value} raised {repr(err)}!')

    # DONE
    return element


def get_web_element_text(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                         by: str ='id', value: str = None) -> str:
    """Extract the text from the value element, of type by, from web_driver.

    Args:
        web_driver: Selenium web driver to search for an element.
        by: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by-type of web element.

    Returns:
        A string, which could be empty, if found.  None otherwise.
    """
    # LOCAL VARIABLES
    element = None  # Found selenium.webdriver.remote.webelement.WebElement
    elem_text = ''  # Text extracted from element

    # INPUT VALIDATION handled by get_web_element()

    # GET IT
    try:
        element = get_web_element(web_driver=web_driver, by=by, value=value)
    except (NoSuchElementException, StaleElementReferenceException) as err:
        Logger.debug(f'get_web_element_text() getting {by}:{value} raised {repr(err)}!')
    else:
        elem_text = element.text

    # DONE
    return elem_text


def _get_element(web_thing: Any, by: str = By.ID, value: str = None) \
    -> selenium.webdriver.remote.webelement.WebElement:
    """Find an element, in web_thing, if the find_element method exists.

    Does not validate input other than verifying web_thing.find_element() exists.

    Args:
        web_thing: Basically, any object that has a find_element method.  This private function
            was written with the Selenium WebDriver and WebElement in mind.
        by: Optional; See: help(selenium.webdriver.common.by.By).
        value: Optional; Value of the by-type of web element.

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
                element = get_it(by=by, value=value)
            except (NoSuchElementException, StaleElementReferenceException) as err:
                Logger.debug(f'Getting element {by}:{value} raised {repr(err)}!')

    # DONE
    return element


def _validate_common_args(by: str = By.ID, value: str = None) -> None:
    """Validate the cross-section of this module's API functions."""
    # INPUT VALIDATION
    # by
    if not isinstance(by, str):
        raise TypeError(f'Invalid data type of {type(by)} for the by')
    if not hasattr(By, by.upper()):
        raise ValueError(f'Invalid by value of {by}.  Use By value from '
                         'the selenium.webdriver.common.by module')
    # value
    if not isinstance(value, str) and value is not None:
        raise TypeError(f'Invalid data type of {type(value)} for the value')


def _validate_wd_input(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                       by: str = By.ID, value: str = None) -> None:
    """Validate the input on behalf of API functions in this module."""
    # INPUT VALIDATION
    # web_driver
    if not web_driver:
        raise TypeError('Web driver may not be None')
    if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
        raise TypeError(f'Invalid data type of {type(web_driver)} for the web_driver')
    _validate_common_args(by=by, value=value)


def _validate_we_input(web_element: selenium.webdriver.remote.webelement.WebElement,
                       by: str = By.ID, value: str = None) -> None:
    """Validate the input on behalf of API functions in this module."""
    # INPUT VALIDATION
    # web_element
    if not web_element:
        raise TypeError('Web element may not be None')
    if not isinstance(web_element, selenium.webdriver.remote.webelement.WebElement):
        raise TypeError(f'Invalid data type of {type(web_element)} for the web_element')
    _validate_common_args(by=by, value=value)
