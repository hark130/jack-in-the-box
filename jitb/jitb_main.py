"""Defines the entry-point function for this package."""
# Standard
# Third Party
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# Local
from jitb.jitb_args import parse_args
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_website import play_the_game


def main() -> int:
    """Entry point function.

    Returns:
        0 on success, 1 for failure.
    """
    # LOCAL VARIABLES
    exit_code = 0   # 0 for success, 1 for failure.
    room_code = ''  # Jackbox Games room code
    username = ''   # Jackbox Games username
    client = None   # JitbAi object

    # DO IT
    (room_code, username) = parse_args()
    try:
        client = JitbAi()
        client.setup()
        play_the_game(room_code=room_code, username=username, ai_obj=client)
    except (KeyboardInterrupt, NoSuchElementException, RuntimeError, TimeoutException) as err:
        _print_exception(err)
        exit_code = 1
    finally:
        client.tear_down()

    # DONE
    return exit_code


def _print_exception(error: Exception) -> None:
    """Print an exception message to stderr."""
    Logger.error(repr(error))
