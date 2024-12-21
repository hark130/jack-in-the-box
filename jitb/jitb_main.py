"""Defines the entry-point function for this package."""
# Standard
import sys
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
    exit_code = 0    # 0 for success, 1 for failure.
    client = None    # JitbAi object
    arg_vals = None  # ArgVals object

    # DO IT
    arg_vals = parse_args()
    try:
        Logger.initialize(debugging=arg_vals.debug)
        client = JitbAi(temperature=1.0)
        client.setup()
        play_the_game(room_code=arg_vals.room_code, username=arg_vals.username, ai_obj=client)
    except Exception as err:
        _print_exception(err)
        exit_code = 1
    finally:
        Logger.shutdown()
        if arg_vals.debug:
            input('[DEBUG] Game is over.  If there is an Exception, consider saving the log and '
                  'webpage for testing.  Press [Enter] to exit.')
        if client:
            client.tear_down()

    # DONE
    return exit_code
# pylint: enable = broad-except


def _print_exception(error: Exception) -> None:
    """Print an exception message to stderr."""
    try:
        Logger.error(repr(error))
    except RuntimeError:
        # Failed arg parsing can result in a failure to initialize the logger
        print(repr(error), file=sys.stderr, flush=True)  # Just print it to stderr
