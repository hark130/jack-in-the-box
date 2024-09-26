"""Defines the pagkage's enum of identifiable Jackbox Games pages."""

# Standard
from enum import auto, Enum
# Third Party
# Local


class JbgPageIds(Enum):
    """Standardizes references to identifiable Jackbox Games page ids.

    Use these values as return values, dictionary keys, etc.
    """
    UNKNOWN = 0          # Who knows... transition page maybe?
    LOGIN = auto()       # Standard jackbox.tv login page
    AVATAR = auto()      # Standard jackbox.tv 'select an avatar' page
    ANSWER = auto()      # Answer a prompt
    VOTE = auto()        # Vote other answers to a prompt
    Q2_LAST = auto()     # Quiplash 2 Last Lash prompt
    Q3_THRIP = auto()    # Quiplash 3 Thriplash prompt
    JB_CATCH = auto()    # Joke Boat catchphrase selection
    JB_TOPIC = auto()    # Joke Boat write joke topics
    JB_PERFORM = auto()  # Joke Boat 'your turn' perform page
