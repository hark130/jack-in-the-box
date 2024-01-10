"""Defines global constants for the package."""
# Standard
from enum import Enum
from typing import Final, List
# Third Party
# Local

JITB_POLL_RATE: Final[float] = 0.5  # Rate, in seconds, JITB will parse page content
# List of Jackbox Games that JITB supports
JITB_SUPPORTED_GAMES: Final[List[str]] = ['Quiplash 3']

# Environment variable to get the OpenAI API key from.
OPENAI_KEY_ENV_VAR: Final[str] = 'OPENAI_API_KEY'

# List of Character accessible names for the Jackbox Games Quiplash 3 avatars
# buttons = test.find_elements(By.XPATH, '//button')
JBG_QUIP3_CHAR_NAMES: Final[List] = ['Purple', 'Blue', 'Teal', 'Green', 'Yellow', 'Orange',
                                     'Red', 'Pink', 'Star', 'Triclops', 'Kitten', 'Coffin',
                                     'Cactus', 'Moon', 'Tear', 'Poop']


class JbgQuip3IntPages(Enum):
    """Defines a set of Jackbox Games Quiplash 3 interactive pages."""
    UNKNOWN = 0       # Who knows... transition page maybe?
    LOGIN = 1         # Login
    AVATAR = 2        # Select an avatar
    ANSWER = 3        # Answer the prompt in Round 1/2
    VOTE = 4          # Vote in Round 1/2
    THRIP_ANSWER = 5  # Answer the Thriplash
