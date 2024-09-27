"""Defines global constants for the package."""
# Standard
from typing import Final, List
# Third Party
# Local

JITB_POLL_RATE: Final[float] = 0.5  # Rate, in seconds, JITB will parse page content

# Environment variable to get the OpenAI API key from.
OPENAI_KEY_ENV_VAR: Final[str] = 'OPENAI_API_KEY'

# List of Character accessible names for the Jackbox Games Quiplash 3 avatars
# buttons = test.find_elements(By.XPATH, '//button')
JBG_QUIP3_CHAR_NAMES: Final[List] = ['Purple', 'Blue', 'Teal', 'Green', 'Yellow', 'Orange',
                                     'Red', 'Pink', 'Star', 'Triclops', 'Kitten', 'Coffin',
                                     'Cactus', 'Moon', 'Tear', 'Poop']

# Default {'role': 'system', 'content': DEFAULT_SYSTEM_CONTENT}
DEFAULT_SYSTEM_CONTENT: Final[str] = 'You are a funny person trying to win Jackbox Games.'
