"""Defines standard validation for the package.

See help(hobo.validation) for basic validation functionality.
"""

# Standard
from typing import Any, Dict
# Third Party
from hobo.validation import validate_string, validate_type
import selenium
import selenium.webdriver
# Local


def validate_bool(value: str, name: str) -> None:
    """Validates boolean values on behalf of this module.

    Args:
        value: The variable to check.
        name: The name of the original arugment being validated (used in exception messages).
    """
    validate_type(value, name, bool)


def validate_element_type(element_type: str) -> None:
    """Validate element_type arguments on behalf of this module."""
    validate_string(element_type, 'element_type', can_be_empty=False)


def validate_game(game: str, games: Dict[str, Any]) -> None:
    """Validate the game against the dictionary of support games.

    Why this odd validation?  Why is the value type hint Any?  To avoid circular
    imports.  The expected value type is actually JbgAbc, but that doesn't
    matter here.

    Args:
        game: The game to be checked for support.
        games: A dictionary of games JITB supports.  Only the keys are inspected.

    Raises:
        RuntimeError: This game is not supported.
    """
    # INPUT VALIDATION
    validate_string(game, 'game')
    validate_type(games, 'games', dict)

    # VALIDATE GAME
    if game not in list(games.keys()):
        raise RuntimeError(f'JITB does not yet support {game}')


def validate_pos_int(in_int: int, name: str) -> None:
    """Validate input on behalf of this module's API functions.

    Args:
        in_int: Input to validate.
        name: Name of the original variable to us in crafting the Exception message.

    Raises:
        TypeError: Bad data type.
        ValueError: Integer not positive.
    """
    validate_type(in_int, name, int)
    if in_int < 1:
        raise ValueError(f'{name.capitalize()} must be positive')


def validate_web_driver(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Validate a web driver."""
    validate_type(web_driver, 'web_driver', selenium.webdriver.chrome.webdriver.WebDriver)
