"""Parse the command line arguments on behalf of the package."""
# Standard
import argparse
# Third Party
# Local
from jitb.jitb_logger import Logger


def parse_args() -> tuple:
    """Parse the command line arguments and return the room code and username.

    Sets the logger to DEBUG level if debug command line argument is provided.

    Returns:
        A tuple containing the (room_code, username).
    """
    parser = argparse.ArgumentParser(prog='Jack in the Box',
                                     description='Connecting Jackbox Games to the OpenAI API')
    parser.add_argument('-r', '--room', action='store', help='The Jackbox Games room code',
                        required=True)
    parser.add_argument('-u', '--user', action='store', help='The Jackbox Games name',
                        required=True)
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Log debug messages to /tmp/jitb_YYYYMMDD_HHMMSS.log', required=False)
    args = parser.parse_args()

    # SETUP LOG
    Logger.initialize(debugging=args.debug)

    # DONE
    return tuple((args.room, args.user))
