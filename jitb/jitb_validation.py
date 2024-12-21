"""Defines standard validation for the package."""

# Standard
# Third Party
import selenium
# Local


def validate_bool(value: str, name: str) -> None:
    """Validates boolean values on behalf of this module.

    Args:
        value: The variable to check.
        name: The name of the original arugment being validated (used in exception messages).
    """
    if not isinstance(value, bool):
        raise TypeError(f'The {name} value must be a string instead of type {type(value)}')


def validate_element_type(element_type: str) -> None:
    """Validate element_type arguments on behalf of this module."""
    validate_string(element_type, 'element_type', may_be_empty=False)


def validate_string(string: str, name: str, may_be_empty: bool = False) -> None:
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


def validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Validate a web driver."""
    if not web_driver:
        raise TypeError('Web driver can not be of type None')
    if not isinstance(web_driver, selenium.webdriver.chrome.webdriver.WebDriver):
        raise TypeError(f'Invalid web_driver data type of {type(web_driver)}')
