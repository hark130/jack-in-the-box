"""Defines global constants for the package."""
# Standard
from enum import Enum
from typing import Final, List
# Third Party
# Local


# List of Character accessible names for the Jackbox Games Quiplash 3 avatars
# buttons = test.find_elements(By.XPATH, '//button')
# print(buttons[0].accessible_name)
JBG_QUIP3_CHAR_NAMES: Final[List] = ['Purple', 'Blue', 'Teal', 'Green', 'Yellow', 'Orange',
                                     'Red', 'Pink', 'Star', 'Triclops', 'Kitten', 'Coffin',
                                     'Cactus', 'Moon', 'Tear', 'Poop']


class JBG_QUIP3_INT_PAGES(Enum):
    UNKNOWN = 0       # Who knows... transition page maybe?
    LOGIN = 1         # Login
    AVATAR = 2        # Select an avatar
    ANSWER = 3        # Answer the prompt in Round 1/2
    VOTE = 4          # Vote in Round 1/2
    THRIP_ANSWER = 5  # Answer the Thriplash
    # THRIP_VOTE = 6    # Vote for the Thriplash
