"""Parse the command line arguments on behalf of the package."""
# Standard
import argparse
import os
# Third Party
# Local
from jitb.jitb_globals import TEMP_DIR_ENV_VARS
from jitb.jitb_misc import determine_tmp_dir


def parse_args() -> tuple:
    """Parse the command line arguments.

    Returns:
        A tuple containing the (room_code, username, debug).
    """
    debug_log = os.path.join(determine_tmp_dir(), 'jitb_YYYYMMDD_HHMMSS-#.log')
    parser = argparse.ArgumentParser(prog='jitb',
                                     description='Jack in the Box (JITB): Connecting Jackbox '
                                                 'Games to the OpenAI API.')
    parser.add_argument('-r', '--room', action='store', help='The Jackbox Games room code',
                        required=True)
    parser.add_argument('-u', '--user', action='store', help='The Jackbox Games name',
                        required=True)
    parser.add_argument('-d', '--debug', action='store_true',
                        help=f'Log debug messages to {debug_log} (Change the dir with '
                             f'the {TEMP_DIR_ENV_VARS[0]} environment variable)',
                        required=False)
    args = parser.parse_args()

    # DONE
    return tuple((args.room, args.user, args.debug))
