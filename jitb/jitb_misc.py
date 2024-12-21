"""Miscellaneous functions used by JITB."""
# Standard
from sys import platform
import os
import re
import unicodedata
import unidecode
# Third Party
# Local
from jitb.jitb_globals import TEMP_DIR_DEF_NIX, TEMP_DIR_DEF_WIN, TEMP_DIR_ENV_VARS
from jitb.jitb_validation import validate_string


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
    return ''.join(char_filter(dirty_str))


def clean_up_string(dirty_string: str, replace_char: str = ' ') -> str:
    """Normalize the characters and replace newlines with replace_char.

    Args:
        dirty_str: A potentially dirty string to normalize and strip.

    Returns:
        A clean version of dirty_str, sans newline characters.
    """
    clean_str = clean_string(dirty_string)
    clean_str = clean_str.replace('\n', replace_char)
    return clean_str


def convert_str_to_int(int_string: str) -> None:
    """Convert the string representation of an integeter to an actual integer.

    Args:
        int_string: The string to convert to an integer.

    Returns:
        An integer derived from int_string on success, None on failed conversion.

    Raises:
        TypeError: Bad data type.
        ValueError: Bad value.
    """
    # LOCAL VARIABLES
    integer = None  # Converted integer from the int_string

    # INPUT VALIDATION
    validate_string(int_string, 'int_string', may_be_empty=False)

    # CONVERT IT
    try:
        integer = int(clean_up_string(dirty_string=int_string, replace_char=''))
    except ValueError:
        pass  # Let it go and just return None

    # DONE
    return integer


def determine_tmp_dir() -> str:
    """Determine the temporary directory in which to store --debug log files.

    Attempts to resolve the temp directory name in the following priority:
    1. TMPDIR environment variable
    2. TEMP environment variable
    3. TEMPDIR environment variable
    4. TMP environment variable
    5. Hard-coded last resort:
        - /tmp for *nix
        - C:\\Temp for Windows

    Returns:
        A string representing the temporary directory to use for the debug log files.
    """
    # LOCAL VARIABLES
    tmp_dir = _read_env_vars(TEMP_DIR_ENV_VARS)  # Temporary directory

    # VALIDATE
    if not tmp_dir:
        if platform.lower() in ('cygwin', 'darwin', 'linux', 'linux2'):
            tmp_dir = TEMP_DIR_DEF_NIX
        elif platform.lower() == 'win32':
            tmp_dir = TEMP_DIR_DEF_WIN
        else:
            raise RuntimeError('Unable to locate environment variables '
                               f'({", ".join(TEMP_DIR_ENV_VARS)}) or determine host OS from '
                               f'"{platform}" to ascertain the temporary directory.')

    # DONE
    return tmp_dir


def _read_env_var(env_var: str) -> str:
    """Read an environment variable and return the value read.

    Args:
        env_var: An environment variable to read.

    Raises:
        None.  KeyErrors are ignored and all other exceptions result in an empty string.

    Returns:
        A string containing the value read.  Returns an empty string if no value was read
        or an exception occurred.
    """
    # LOCAL VARIABLES
    env_value = ''  # The value read from env_var

    # INPUT VALIDATION
    try:
        env_value = os.environ[env_var]
    except (KeyError, TypeError, ValueError):
        pass  # Must not exist

    # DONE
    return env_value


def _read_env_vars(env_vars: list) -> str:
    """Read each environment variable from the list, returning the first value read.

    Args:
        env_vars: A list of environment variables to attempt to read.

    Raises:
        None.  KeyErrors are ignored and all other exceptions result in an empty string.

    Returns:
        A string containing the first value read from the list.  Returns an empty string
        if no values were read or an exception occurred.
    """
    # LOCAL VARIABLES
    env_value = ''  # The first value read from a valid env_vars list entry

    # INPUT VALIDATION
    if isinstance(env_vars, list):
        for env_var in env_vars:
            env_value = _read_env_var(env_var)
            if env_value:
                break  # Found one!

    # DONE
    return env_value
