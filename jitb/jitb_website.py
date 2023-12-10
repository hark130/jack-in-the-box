"""Defines web-based functionality for the package."""
# Standard
from typing import Final, List
import random
import time
# Third Party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import selenium
# Local
from jitb.jitb_globals import JBG_QUIP3_CHAR_NAMES, JbgQuip3IntPages
from jitb.jitb_openai import JitbAi


# List of observed errors reported by Jackbox Games html
ERROR_LIST: Final[List] = ['Room not found']


def answer_prompts(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   ai_obj: JitbAi) -> None:
    """Generating answers for prompts."""
    # LOCAL VARIABLES
    prompt_text = ''      # Input prompt

    # ANSWER THE PROMPTS
    for _ in range(2):
        prompt_text = _answer_prompt(web_driver, last_prompt=prompt_text, ai_obj=ai_obj)


def answer_thriplash(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                     ai_obj: JitbAi) -> None:
    """Generate answers for the Thriplash (Round 3) prompt."""
    # LOCAL VARIABLES
    prompt_text = ''    # Input prompt
    input_fields = []   # List of web elements for the three input fields
    buttons = []        # List of button web elements
    clicked_it = False  # Keep track of whether this prompt was answered or not

    # INPUT VALIDATION
    if not _is_thrip_prompt_page(web_driver):
        raise RuntimeError('This is not the Thriplash prompt page')

    # ANSWER IT
    prompt_text = _get_prompt(web_driver=web_driver)
    print('AI QUESTION\nGive me three funny answers for the following Quiplash 3 '
          f'Thriplash prompt {prompt_text}')  # DEBUGGING
    # print(f'THRIPLASH PROMPT: {prompt_text}')  # DEBUGGING
    input_fields = web_driver.find_elements(By.ID, 'input-text-textarea')
    # print(f'FOUND {len(input_fields)} INPUT FIELDS')  # DEBUGGING
    # for input_field in input_fields:
    #     print(f'INPUT FIELD: {input_field.text}')  # DEBUGGING

    # SUBMIT IT
    for input_field in input_fields:
        # print(f'INPUT FIELD: {input_field.text}')  # DEBUGGING
        input_field.send_keys(str(random.random()))
    buttons = web_driver.find_elements(By.XPATH, '//button')
    # print(f'FOUND {len(buttons)} THRIPLASH ANSWER BUTTONS')  # DEBUGGING
    for button in buttons:
        if button.text.lower() == 'SUBMIT'.lower() and button.is_enabled():
            # print(f'TEXT: {button.text}')  # DEBUGGING
            button.click()
            clicked_it = True
            break

    # DONE
    if not clicked_it:
        raise RuntimeError('Did not answer the Thriplash prompt')
    print(f'ANSWERED {prompt_text} with random input!')  # DEBUGGING


def join_room(room_code: str, username: str) -> selenium.webdriver.chrome.webdriver.WebDriver:
    """Join a https://jackbox.tv/ game with room_code and username.

    Args:
        room_code:  The room code to join.
        username:  The screen name to use during the game.

    Returns:
        The webdriver object on success.
    """
    # LOCAL VARIABLES
    driver = webdriver.Chrome()  # Webdriver object

    # JOIN IT
    driver.implicitly_wait(2)
    driver.get('https://jackbox.tv/')
    # print(driver.page_source)  # DEBUGGING
    room_code_box = driver.find_element(By.ID, 'roomcode')
    room_code_box.send_keys(room_code)
    _verify_room_code(driver)
    username_box = driver.find_element(By.ID, 'username')
    username_box.send_keys(username)
    _check_for_error(driver)
    play_button = driver.find_element(By.ID, 'button-join')
    play_button.click()
    _check_for_error(driver)

    # DONE
    return driver


def play_the_game(room_code: str, username: str, ai_obj: JitbAi) -> None:
    """Dynamically respond to the flow of the game."""
    # LOCAL VARIABLES
    web_driver = join_room(room_code=room_code, username=username)  # Webdriver for Jackbox Games
    last_page = JbgQuip3IntPages.UNKNOWN                            # The previous JBG page
    curr_page = JbgQuip3IntPages.UNKNOWN                            # Current JBG page

    # PLAY IT
    try:
        while True:
            curr_page = _what_page_is_this(web_driver)
            if curr_page == JbgQuip3IntPages.LOGIN:
                pass  # Wait for the page to change because we already logged in
            elif curr_page == JbgQuip3IntPages.AVATAR and curr_page != last_page:
                select_character(web_driver=web_driver)  # Just select once
            elif curr_page == JbgQuip3IntPages.ANSWER and curr_page != last_page:
                answer_prompts(web_driver=web_driver, ai_obj=ai_obj)
            elif curr_page == JbgQuip3IntPages.VOTE and curr_page != last_page:
                vote_answers(web_driver=web_driver, ai_obj=ai_obj)
            elif curr_page == JbgQuip3IntPages.THRIP_ANSWER and curr_page != last_page:
                answer_thriplash(web_driver=web_driver, ai_obj=ai_obj)
            else:
                time.sleep(1)  # Zzzzz...
            last_page = curr_page
    finally:
        if web_driver:
            web_driver.close()


def select_character(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Randomize an avatar selection from the available list.

    Raises:
        RuntimeError: An error message was found in the HTML or this isn't the character selection
            page.
    """
    # LOCAL VARIABLES
    button_list = []     # List of web elements for the avatars
    button_entry = None  # Web element for a button
    max_loops = 20       # Maximum number of infinite loops

    # INPUT VALIDATION
    time.sleep(1)  # TO DO: DON'T DO NOW... REPLACE THIS TASTEFUL SLEEP WITH REAL CODE
    if not _is_char_selection_page(web_driver):
        raise RuntimeError('This is not the character selection page.')

    # SELECT IT
    button_list = web_driver.find_elements(By.XPATH, '//button')
    for _ in range(max_loops):
        button_entry = random.choice(button_list)
        if button_entry.accessible_name in JBG_QUIP3_CHAR_NAMES and button_entry.is_enabled():
            button_entry.click()
            break


def vote_answers(web_driver: selenium.webdriver.chrome.webdriver.WebDriver, ai_obj: JitbAi) -> None:
    """Vote all the other answers."""
    # LOCAL VARIABLES
    prompt_text = ''  # The prompt text

    # INPUT VALIDATION
    if not _is_vote_page(web_driver):
        raise RuntimeError('This is not a voting page.')

    # VOTE IT
    while True:
        prompt_text = _vote_answer(web_driver, last_prompt=prompt_text, ai_obj=ai_obj)
        if not prompt_text:
            break
        if not _is_vote_page(web_driver):
            break


def _answer_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                   last_prompt: str, ai_obj: JitbAi) -> str:
    """Generating answers for prompts.

    Args:
        last_prompt: The last prompt that was answered.  Helps this function avoid trying to
            answer the same prompt twice.
        ai_obj: Query object to get AI-generated answers.

    Returns:
        The prompt that was answered as a string.

    Raises:
        RuntimeError: The prompt wasn't answered.
    """
    # LOCAL VARIABLES
    prompt_text = ''     # Input prompt
    answer = ''          # Answer to the prompt
    prompt_input = None  # Web element for the prompt input field
    buttons = []         # Web element for the submit button
    clicked_it = False   # Keep track of whether this prompt was answered or not
    num_loops = 5        # Number of attempts to make for a new prompt

    # INPUT VALIDATION
    if not _is_prompt_page(web_driver):
        raise RuntimeError('This is not a prompt page')

    # WAIT FOR IT
    for _ in range(num_loops):
        prompt_text = _get_prompt(web_driver)[1]
        if prompt_text and prompt_text != last_prompt:
            break
        time.sleep(1)

    # ANSWER IT
    # TO DO: DON'T DO NOW... GET ANSWER FROM THE OPENAI API... 45 max characters
    # print(f'AI QUESTION\nGive me a funny answer for the Quiplash 3 prompt {prompt_text}')  # DEBUGGING
    # answer = str(random.random())  # PLACEHOLDER
    answer = ai_obj.generate_answer(prompt=prompt_text)
    prompt_input = web_driver.find_element(By.ID, 'input-text-textarea')
    prompt_input.send_keys(answer)
    buttons = web_driver.find_elements(By.XPATH, '//button')
    for button in buttons:
        # print(f'DIR: {dir(button)}')  # DEBUGGING
        if button.text.lower() == 'SUBMIT'.lower() and button.is_enabled():
            # print(f'TEXT: {button.text}')  # DEBUGGING
            button.click()
            clicked_it = True
            break

    # DONE
    if not clicked_it:
        raise RuntimeError('Did not answer the prompt')
    print(f'ANSWERED {prompt_text} with {answer}!')  # DEBUGGING
    return prompt_text


def _check_for_error(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Check the driver's page source for known errors.

    Raises:
        RuntimeError: An error message was found in the HTML or the room was disconnected.
    """
    # LOCAL VARIABLES
    temp_we = None  # Temp web element object

    # CHECK IT
    # <span data-v-47cae0dc="" class="status">Room not found</span>
    if web_driver:
        # Check for errors
        for error in ERROR_LIST:
            # print(f'PAGE SOURCE;\n{web_driver.page_source}')  # DEBUGGING
            if error in web_driver.page_source:
                # print(f'ERROR: {error}')  # DEBUGGING
                raise RuntimeError(error)
        # Verify not disconnected
        try:
            temp_we = web_driver.find_element(By.ID, 'swal2-title')
            # print(f'TEMP WE: {temp_we.text}')  # DEBUGGING
        except NoSuchElementException:
            pass  # It's good that we didn't find it
        else:
            if temp_we.text.lower().startswith('Disconnected'.lower()):
                raise RuntimeError('The room was disconnected')


def _get_prompt(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> list:
    """Wait for the prompt element id to show and then return.

    Returns:
        The game prompt, split by newline, into a list.
    """
    # LOCAL VARIABLES
    prompt_text = []  # The prompt's text split by newline

    # INPUT VALIDATION
    # if not _is_prompt_page(web_driver):
    #     raise RuntimeError('This is not a prompt page')

    # WAIT FOR IT
    # wait = WebDriverWait(web_driver, 120)
    # element = wait.until(EC.presence_of_element_located((By.ID, 'prompt')))
    # print(element.text.split('\n'))
    element = web_driver.find_element(By.ID, 'prompt')
    # print(f'PROMPT TEXT {element.text}')  # DEBUGGING
    prompt_text = element.text.split('\n')

    # DONE
    if not prompt_text:
        raise RuntimeError('Did not detect any prompts')
    return prompt_text


def _is_char_selection_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this the character selection screen.

    Returns:
        True if this is the 'Select your character' screen, False otherwise.
    """
    # LOCAL VARIABLES
    char_selection = False  # Prove this true
    prompt = None           # Web Element for the characters prompt

    # IS IT?
    try:
        prompt = web_driver.find_element(By.ID, 'charactersPrompt')
        if 'Select your character'.lower() in prompt.text.lower():
            char_selection = True
    except (NoSuchElementException, TypeError, ValueError):
        pass  # Not the character selection page

    # DONE
    return char_selection


def _is_login_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this the login page.

    Returns:
        True if this is the login screen, False otherwise.
    """
    # LOCAL VARIABLES
    login_page = False  # Prove this true

    # IS IT?
    try:
        web_driver.find_element(By.ID, 'roomcode')
        web_driver.find_element(By.ID, 'username')
        web_driver.find_element(By.ID, 'button-join')
    except (NoSuchElementException, TypeError, ValueError):
        pass  # Not the character selection page
    else:
        login_page = True  # If we made it here, it's the login page

    # DONE
    return login_page


def _is_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this a round 1 or 2 prompt page.

    Returns:
        True if this is a regular prompt screen, False otherwise.
    """
    # LOCAL VARIABLES
    prompt_page = False                           # Prove this true
    temp_we = None                                # Temporary web element variable
    prompts = ['Prompt 1 of 2', 'Prompt 2 of 2']  # Prompt needles

    # IS IT?
    try:
        temp_we = web_driver.find_element(By.ID, 'prompt')
    except (NoSuchElementException, TypeError, ValueError):
        pass  # Not a prompt page
    else:
        for prompt in prompts:
            if temp_we.text.startswith(prompt):
                prompt_page = True  # If we made it here, it's a prompt page
                break

    # DONE
    return prompt_page


def _is_thrip_prompt_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is the Thriplash (Round 3) prompt page.

    Returns:
        True if this is the Thriplash (Round 3) prompt page, False otherwise.
    """
    # LOCAL VARIABLES
    prompt_page = False      # Prove this true
    temp_we = None           # Temporary web element variable
    prompt = 'Final prompt'  # Prompt needle

    # IS IT?
    try:
        temp_we = web_driver.find_element(By.ID, 'prompt')
    except (NoSuchElementException, TypeError, ValueError):
        pass  # Not a Thriplash prompt page
    else:
        # print(f'THRIPT PROMPT TEXT: {temp_we.text}')  # DEBUGGING
        if temp_we.text.lower().startswith(prompt.lower()):
            prompt_page = True  # If we made it here, it's a prompt page

    # DONE
    return prompt_page


def _is_vote_page(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> bool:
    """Determine if this is this a round 1 or 2 vote page.

    Returns:
        True if this is a regular vote screen, False otherwise.
    """
    # LOCAL VARIABLES
    vote_page = False                  # Prove this true
    temp_we = None                     # Temporary web element variable
    prompt = 'Vote for your favorite'  # Prompt needles

    # IS IT?
    try:
        temp_we = web_driver.find_element(By.ID, 'prompt')
    except (NoSuchElementException, TypeError, ValueError):
        pass  # Not a vote page
    else:
        if prompt.lower() in temp_we.text.lower():
            vote_page = True  # If we made it here, it's a vote page

    # DONE
    return vote_page


def _verify_room_code(web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> None:
    """Verify the room was found.

    Raises:
        RuntimeError: An error message was found in the HTML
    """
    # LOCAL VARIABLES
    app_elem = None     # The app class element
    # status_elem = None  # The status class WebElement

    # VERIFY IT
    time.sleep(1)  # TO DO: DON'T DO NOW... REPLACE THIS TASTEFUL SLEEP WITH REAL CODE
    # 1. Check for generic errors
    _check_for_error(web_driver)
    # 2. Find the status element
    if web_driver:
        app_elem = web_driver.find_element(By.CLASS_NAME, 'app')
    # 3. Read the status element
    # print(f'APP ELEM: {app_elem.text}')  # DEBUGGING
    if app_elem.text:
        for error in ERROR_LIST:
            if error.lower() in app_elem.text.lower():
                raise RuntimeError(error)


def _vote_answer(web_driver: selenium.webdriver.chrome.webdriver.WebDriver,
                 last_prompt: str, ai_obj: JitbAi) -> str:
    """Generate votes for other players prompts.

    Args:
        last_prompt: The last prompt that was answered.  Helps this function avoid trying to
            answer the same prompt twice.

    Returns:
        The prompt that was answered as a string.

    Raises:
        RuntimeError: The prompt wasn't answered.
    """
    # LOCAL VARIABLES
    prompt_text = ''    # Input prompt
    buttons = []        # List of web elements for the buttons
    button = None       # The web element of the button to click
    clicked_it = False  # Keep track of whether this prompt was answered or not
    num_loops = 5       # Number of attempts to make for a new prompt
    choice_list = []    # List of possible answers
    favorite = ''       # OpenAI's favorite answer

    # WAIT FOR IT
    for _ in range(num_loops):
        try:
            # print(f'VOTE PROMPTS: {_get_prompt(web_driver)}')  # DEBUGGING
            prompt_text = _get_prompt(web_driver)[0]
            # print(f'PROMPT TEXT: {prompt_text}')  # DEBUGGING
            # print(f'LAST PROMPT: {last_prompt}')  # DEBUGGING
            if prompt_text and prompt_text != last_prompt:
                break
            if not _is_vote_page(web_driver):
                prompt_text = ''
                break
            time.sleep(1)
        except NoSuchElementException:
            prompt_text = ''  # Must have been the last prompt to vote

    # ANSWER IT
    if prompt_text and prompt_text != last_prompt:
        buttons = web_driver.find_elements(By.XPATH, '//button')
        # print(f'Ask the AI ')
        # button = random.choice(buttons)  # TO DO: DON'T DO NOW... GET ANSWER FROM THE OPENAI API...
        # Form the selection list
        for button in buttons:
            if button.text:
                choice_list.append(button.text)
        # print(f'AI QUESTION\n{prompt_text}: {",".join(choice_list)}')  # DEBUGGING
        favorite = ai_obj.vote_favorite(prompt=prompt_text, answers=choice_list)
        for button in buttons:
            if button and button.text == favorite and button.is_enabled():
                button.click()
                # print(f'JUST CLICKED {button.text}')  # DEBUGGING
                clicked_it = True
    else:
        prompt_text = ''  # Nothing got answered

    # DONE
    if prompt_text and prompt_text != last_prompt and not clicked_it:
        raise RuntimeError('Did not vote an answer')
    if button:
        print(f'VOTED {button.text} for {prompt_text}!')  # DEBUGGING
    return prompt_text


def _what_page_is_this(
        web_driver: selenium.webdriver.chrome.webdriver.WebDriver) -> JbgQuip3IntPages:
    """Deterine what page is currently being seen."""
    # LOCAL VARIABLES
    current_page = JbgQuip3IntPages.UNKNOWN  # What type of page is this?

    # INPUT VALIDATION
    _check_for_error(web_driver)

    # DETERMINE PAGE
    if _is_login_page(web_driver):
        current_page = JbgQuip3IntPages.LOGIN
    elif _is_char_selection_page(web_driver):
        current_page = JbgQuip3IntPages.AVATAR
    elif _is_prompt_page(web_driver):
        current_page = JbgQuip3IntPages.ANSWER
    elif _is_vote_page(web_driver):
        current_page = JbgQuip3IntPages.VOTE
    elif _is_thrip_prompt_page(web_driver):
        current_page = JbgQuip3IntPages.THRIP_ANSWER
    # elif _is_thrip_vote_page(web_driver):
    #     current_page = JbgQuip3IntPages.THRIP_VOTE

    # DONE
    print(f'THIS IS THE {current_page} PAGE')  # DEBUGGING
    return current_page