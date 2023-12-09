"""Defines the entry-point function for this package."""
# Standard
import sys
# Third Party
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import selenium
# Local
from jitb.jitb_args import parse_args
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
    # driver = None   # Webdriver for the Jackbox Games website

    # DO IT
    (room_code, username) = parse_args()
    # print(f'ROOM CODE: {room_code}')  # DEBUGGING
    # print(f'USERNAME: {username}')  # DEBUGGING
    try:
        play_the_game(room_code=room_code, username=username)
        # driver = join_room(room_code=room_code, username=username)
        # select_character(driver)
        # # TO DO: DON'T DO NOW... WAIT FOR GAME TO START (by waiting for char selection to go away)
        # answer_prompts(driver)
        # vote_answers(driver)
        # input()  # DEBUGGING
        # print(f'POST-INPUT PAGE SOURCE:\n{driver.page_source}')  # DEBUGGING
    except (KeyboardInterrupt, NoSuchElementException, RuntimeError, TimeoutException) as err:
        # if driver:
        #     print(f'SOURCE: {driver.page_source}')  # DEBUGGING
        _print_exception(err)
        exit_code = 1

    # DONE
    # input()  # DEBUGGING
    # if driver:
    #     driver.close()
    return exit_code


def _print_exception(error: Exception) -> None:
    """Print an exception message to stderr."""
    print(repr(error), file=sys.stderr)
