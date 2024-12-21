"""Defines global constants for the package."""
# Standard
from typing import Final, List
# Third Party
# Local

# Default {'role': 'system', 'content': DEFAULT_SYSTEM_CONTENT}
DEFAULT_SYSTEM_CONTENT: Final[str] = 'You are a funny person trying to win Jackbox Games.'

# Argument parser supported "commands"
JITB_ARG_CMDS_AUTO: Final[List[str]] = ['automatic', 'auto']              # Auto commands
JITB_ARG_CMDS_MAN: Final[List[str]] = ['manual', 'man']                   # Man commands
JITB_ARG_CMDS: Final[List[str]] = JITB_ARG_CMDS_AUTO + JITB_ARG_CMDS_MAN  # All commands
JITB_POLL_RATE: Final[float] = 0.5  # Rate, in seconds, JITB will parse page content

# List of Character accessible names for the Jackbox Games Quiplash 3 avatars
# buttons = test.find_elements(By.XPATH, '//button')
JBG_QUIP3_CHAR_NAMES: Final[List] = ['Purple', 'Blue', 'Teal', 'Green', 'Yellow', 'Orange',
                                     'Red', 'Pink', 'Star', 'Triclops', 'Kitten', 'Coffin',
                                     'Cactus', 'Moon', 'Tear', 'Poop']

# Environment variable to get the OpenAI API key from.
OPENAI_KEY_ENV_VAR: Final[str] = 'OPENAI_API_KEY'

# Temporary directory constants
TEMP_DIR_DEF_NIX: Final[str] = '/tmp'      # Last resort for a *nix temp dir
TEMP_DIR_DEF_WIN: Final[str] = 'C:\\Temp'  # Last resort for a Windows temp dir
# Environment variables to investigate for a user-defined temp directory to store debug logs
TEMP_DIR_ENV_VARS: Final[List[str]] = ['TMPDIR', 'TEMP', 'TEMPDIR', 'TMP']  # Ordered
