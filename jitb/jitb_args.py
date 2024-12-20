"""Parse the command line arguments on behalf of the package."""
# Standard
import argparse
import os
# Third Party
# Local
from jitb.jitb_argvals import ArgVals
from jitb.jitb_globals import JITB_ARG_CMDS_AUTO, JITB_ARG_CMDS_MAN, TEMP_DIR_ENV_VARS
from jitb.jitb_misc import determine_tmp_dir
from jitb.jitb_website import JITB_SUPPORTED_GAMES


def parse_args() -> ArgVals:
    """Parse the command line arguments.

    Returns:
        A ArgVals data class containing all parsed values.
    """
    jitb_games = list(JITB_SUPPORTED_GAMES.keys())  # JITB supported games
    jitb_games.sort()
    debug_log = os.path.join(determine_tmp_dir(), 'jitb_YYYYMMDD_HHMMSS-#.log')
    parser = argparse.ArgumentParser(prog='jitb',
                                     description='Jack in the Box (JITB): Connecting Jackbox '
                                                 'Games to the OpenAI API.  JITB currently '
                                                 f'supports: {", ".join(jitb_games)}.')
    subparsers = parser.add_subparsers(dest='command', help='Login support: automatic or manual')
    manual_parser = subparsers.add_parser(JITB_ARG_CMDS_MAN[0], aliases=JITB_ARG_CMDS_MAN[1:],
                                          help='Human interaction is required to login '
                                          '(e.g., Twitch-enabled login)')
    auto_parser = subparsers.add_parser(JITB_ARG_CMDS_AUTO[0], aliases=JITB_ARG_CMDS_AUTO[1:],
                                        help='JITB will automatically login')
    auto_parser.add_argument('-r', '--room', action='store', help='The Jackbox Games room code',
                             required=True)
    auto_parser.add_argument('-u', '--user', action='store', help='The Jackbox Games name',
                             required=True)
    parser.add_argument('-d', '--debug', action='store_true',
                        help=f'Log debug messages to {debug_log} (Change the dir with '
                             f'the {TEMP_DIR_ENV_VARS[0]} environment variable)',
                        required=False)
    args = parser.parse_args()

    # DONE
    return ArgVals(args.command, args.debug, room_code=args.room, username=args.user)
