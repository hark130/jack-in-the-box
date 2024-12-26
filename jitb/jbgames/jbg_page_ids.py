"""Defines the pagkage's enum of identifiable Jackbox Games pages."""

# Standard
from enum import auto, Enum
# Third Party
# Local


class JbgPageIds(Enum):
    """Standardizes references to identifiable Jackbox Games page ids.

    Use these values as return values, dictionary keys, etc.
    """
    # Common Use
    UNKNOWN = 0              # Who knows... transition page maybe?
    ANSWER = auto()          # Answer a prompt
    AVATAR = auto()          # Standard jackbox.tv 'select an avatar' page
    LOGIN = auto()           # Standard jackbox.tv login page
    VOTE = auto()            # Vote other answers to a prompt
    # Game-Specific
    BR_FAULT = auto()        # Whose fault was it?
    BR_DESCRIBE = auto()     # Blather Round 'Describe _____' page
    BR_SECRET = auto()       # Blather Round Choose Secret Prompt page
    DICT_WAIT_LIKE = auto()  # Dictionarium waiting page with likes
    JB_CATCH = auto()        # Joke Boat catchphrase selection
    JB_TOPIC = auto()        # Joke Boat write joke topics
    JB_PERFORM = auto()      # Joke Boat 'your turn' perform page
    Q2_LAST = auto()         # Quiplash 2 Last Lash prompt
    Q3_THRIP = auto()        # Quiplash 3 Thriplash prompt
