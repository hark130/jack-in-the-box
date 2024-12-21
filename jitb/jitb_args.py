"""Parse the command line arguments on behalf of the package."""
# Standard
from typing import Any
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
    # LOCAL VARIABLES
    room_arg_name = 'room'                          # The proper name of the room code argument
    user_arg_name = 'user'                          # The proper name of the username argument
    room_code = None                                # Parsed room value (may be None)
    username = None                                 # Parsed username (may be None)
    jitb_games = list(JITB_SUPPORTED_GAMES.keys())  # JITB supported games
    parser = None                                   # ArgumentParser object
    subparsers = None                               # Subparsers
    manual_parser = None                            # The 'manual' command subparser
    auto_parser = None                              # The 'automatic' command subparser
    args = None                                     # Parsed argument Namespace
    # Debug log location
    debug_log = os.path.join(determine_tmp_dir(), 'jitb_YYYYMMDD_HHMMSS-#.log')

    # SETUP
    jitb_games.sort()
    parser = argparse.ArgumentParser(prog='jitb',
                                     description='Jack in the Box (JITB): Connecting Jackbox '
                                                 'Games to the OpenAI API.  JITB currently '
                                                 f'supports: {", ".join(jitb_games)}.')
    subparsers = parser.add_subparsers(dest='command', help='Login support: automatic or manual')
    manual_parser = subparsers.add_parser(JITB_ARG_CMDS_MAN[0], aliases=JITB_ARG_CMDS_MAN[1:],
                                          help='Human interaction is required to login '
                                          '(e.g., Twitch-enabled login)')
    manual_parser.add_argument(f'-{room_arg_name[0]}', f'--{room_arg_name}', action='store',
                               help='The Jackbox Games room code', required=True)
    auto_parser = subparsers.add_parser(JITB_ARG_CMDS_AUTO[0], aliases=JITB_ARG_CMDS_AUTO[1:],
                                        help='JITB will automatically login')
    auto_parser.add_argument(f'-{room_arg_name[0]}', f'--{room_arg_name}', action='store',
                             help='The Jackbox Games room code', required=True)
    auto_parser.add_argument(f'-{user_arg_name[0]}', f'--{user_arg_name}', action='store',
                             help='The Jackbox Games username', required=True)
    parser.add_argument('-d', '--debug', action='store_true',
                        help=f'Log debug messages to {debug_log} (Change the dir with '
                             f'the {TEMP_DIR_ENV_VARS[0]} environment variable)',
                        required=False)

    # PARSE IT
    args = parser.parse_args()
    room_code = _get_eafp_attr(args, room_arg_name)  # Get the room code
    username = _get_eafp_attr(args, user_arg_name)  # Get the username

    # DONE
    return ArgVals(args.command, args.debug, room_code=room_code, username=username)


def _get_eafp_attr(args: argparse.Namespace, attr: str) -> Any:
    """Safely retrieve values from a Namespace (if they exist)."""
    # LOCAL VARIABLES
    value = None  # Retrieved value

    # GET IT
    try:
        value = getattr(args, attr)
    except AttributeError:
        pass  # Easier to ask for forgiveness than permission (EAFP)

    # DONE
    return value
