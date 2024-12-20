"""Defines the ArgVals data class used by the argument parser to communicate values."""

# Standard
from dataclasses import dataclass, field
# Third Party
# Local


@dataclass
class ArgVals:
    """Return value of the JITB argument parser."""
    command: str
    debug: bool
    room_code: str = field(default=None)  # Not used for all commands
    username: str = field(default=None)   # Not used for all commands
