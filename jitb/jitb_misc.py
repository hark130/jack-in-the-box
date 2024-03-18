"""Miscellaneous functions used by JITB."""
# Standard
import re
import unicodedata
import unidecode
# Third Party
# Local


def char_filter(dirty_str: str):
    """Filter the characters in dirty_str."""
    latin = re.compile('[a-zA-Z]+')
    for char in unicodedata.normalize('NFC', dirty_str):
        decoded = unidecode.unidecode(char)
        if latin.match(decoded):
            yield char
        else:
            yield decoded


def clean_string(dirty_str: str) -> str:
    """Normalize the characters in dirty_str.

    Args:
        dirty_str: A potentially dirty string to normalize.

    Returns:
        A clean version of dirty_str.
    """
    return "".join(char_filter(dirty_str))


def clean_up_string(dirty_string: str) -> str:
    """Normalize the characters and replace newlines with spaces.

    Args:
        dirty_str: A potentially dirty string to normalize and strip.

    Returns:
        A clean version of dirty_str, sans newline characters.
    """
    clean_str = clean_string(dirty_string)
    clean_str = clean_str.replace('\n', ' ')
    return clean_str
