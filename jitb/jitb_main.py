"""Defines the entry-point function for this package."""
# Standard
# Third Party
# Local
from jitb.jitb_args import parse_args
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_website import play_the_game


# pylint: disable = broad-except
def main() -> int:
    """Entry point function.

    Returns:
        0 on success, 1 for failure.
    """
    # LOCAL VARIABLES
    exit_code = 0   # 0 for success, 1 for failure.
    room_code = ''  # Jackbox Games room code
    username = ''   # Jackbox Games username
    debug = False   # Debug command line argument
    client = None   # JitbAi object

    # DO IT
    (room_code, username, debug) = parse_args()
    try:
        Logger.initialize(debugging=debug)
        client = JitbAi(temperature=1.0)
        client.setup()
        play_the_game(room_code=room_code, username=username, ai_obj=client)
    except Exception as err:
        _print_exception(err)
        exit_code = 1
    finally:
        Logger.shutdown()
        if debug:
            input('[DEBUG] Game is over.  If there is an Exception, consider saving the log and '
                  'webpage for testing.  Press [Enter] to exit.')
        client.tear_down()

    # DONE
    return exit_code
# pylint: enable = broad-except


def _print_exception(error: Exception) -> None:
    """Print an exception message to stderr."""
    Logger.error(repr(error))
