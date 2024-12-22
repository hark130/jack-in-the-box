"""Defines web-based functionality for the package."""
# Standard
from typing import Dict, Final, Tuple
import time
# Third Party
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jbgames.jbg_abc import ERROR_LIST, JbgAbc
from jitb.jbgames.jbg_br import JbgBr
from jitb.jbgames.jbg_dict import JbgDict
from jitb.jbgames.jbg_jb import JbgJb
from jitb.jbgames.jbg_q2 import JbgQ2
from jitb.jbgames.jbg_q3 import JbgQ3
from jitb.jitb_globals import JITB_POLL_RATE
from jitb.jitb_logger import Logger
from jitb.jitb_openai import JitbAi
from jitb.jitb_validation import validate_game

# List of Jackbox Games that JITB supports
JITB_SUPPORTED_GAMES: Final[Dict[str, JbgAbc]] = {"Blather 'Round": JbgBr, 'Dictionarium': JbgDict,
                                                  'Joke Boat': JbgJb, 'Quiplash 2': JbgQ2,
                                                  'Quiplash 3': JbgQ3}


def join_room(room_code: str,
              username: str) -> Tuple[str, selenium.webdriver.chrome.webdriver.WebDriver]:
    """Join a https://jackbox.tv/ game with room_code and username.

    Args:
        room_code:  The room code to join.
        username:  The screen name to use during the game.  May be None for manual logins.

    Returns:
        The a tuple containing the game type (e.g., Quiplash 3) and the webdriver object on success.
    """
    # LOCAL VARIABLES
    driver = webdriver.Chrome()  # Webdriver object
    game = ''                    # Status text of the roomcode

    # JOIN IT
    driver.implicitly_wait(2)
    driver.get('https://jackbox.tv/')
    room_code_box = driver.find_element(By.ID, 'roomcode')
    room_code_box.send_keys(room_code)
    game = _verify_room_code(driver)
    validate_game(game=game, games=JITB_SUPPORTED_GAMES)
    if username:
        username_box = driver.find_element(By.ID, 'username')
        username_box.send_keys(username)
        play_button = driver.find_element(By.ID, 'button-join')
        play_button.click()

    # DONE
    return tuple((game, driver))


def play_the_game(room_code: str, username: str, ai_obj: JitbAi) -> None:
    """Dynamically respond to the flow of the game."""
    # LOCAL VARIABLES
    game = ''          # What Jackbox game is associated with this room code?
    web_driver = None  # Selenium webdriver for Jackbox Games
    jbg_obj = None     # The jitb.jbgames object to handle this game

    # LOGIN
    game, web_driver = join_room(room_code=room_code, username=username)

    # SETUP
    validate_game(game=game, games=JITB_SUPPORTED_GAMES)
    jbg_obj = JITB_SUPPORTED_GAMES[game](ai_obj=ai_obj, username=username)

    # PLAY IT
    try:
        if not username:
            Logger.info(f'It appears you must login to play {game}.  '
                        'JITB will take over once it has detected a login.')
        while True:
            jbg_obj.play(web_driver=web_driver)
            time.sleep(JITB_POLL_RATE)  # Zzzzz...
    finally:
        if web_driver:
            web_driver.close()


def _verify_room_code(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> str:
    """Verify the room was found and return the status.

    Returns:
        The status text (e.g., 'Quiplash 3').

    Raises:
        RuntimeError: An error message was found in the HTML or the status wasn't found.
    """
    # LOCAL VARIABLES
    app_elem = None     # The app class element
    status_text = None  # The status class text

    # VERIFY IT
    time.sleep(1)  # TO DO: DON'T DO NOW... REPLACE THIS TASTEFUL SLEEP WITH REAL CODE
    # 1. Find the status element
    if web_driver:
        app_elem = web_driver.find_element(By.CLASS_NAME, 'app')
    # 2. Look for errors
    if app_elem and app_elem.text:
        for error in ERROR_LIST:
            if error.lower() in app_elem.text.lower():
                raise RuntimeError(error)
    # 3. Read the status text
    status_text = web_driver.find_element(By.CLASS_NAME, 'status').text
    Logger.debug(f'This room code is a {status_text} game')

    # DONE
    return status_text
