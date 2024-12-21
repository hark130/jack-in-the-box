"""The package's interface to OpenAI's API."""
# Standard
from collections import OrderedDict
from string import punctuation
from typing import Final, List
import os
import re
import random
import string
import sys
# Third Party
from hobo.validation import validate_list, validate_string, validate_type
from openai import OpenAI
# Local
from jitb.jitb_globals import DEFAULT_SYSTEM_CONTENT, OPENAI_KEY_ENV_VAR
from jitb.jitb_logger import Logger
from jitb.jitb_misc import clean_up_string
from jitb.jitb_validation import validate_pos_int


# Minimum number of underscores to be considered a fill-in-the-blank
MIN_FITB_LEN: Final[int] = 4                  # Minimum fill-in-the-blank underscores
BASE_MSG_CONTENT_KEY: Final[str] = 'content'  # Key value for JitbAi base messages


class JitbAi:
    """Implements the interface to the OpenAI API."""

    def __init__(self, model: str = 'gpt-4o-mini', temperature: float = 1.0) -> None:
        """Class ctor.

        Args:
            model: Optional; OpenAI model to use.  See: https://platform.openai.com/docs/models
            temperature: Optional; What sampling temperature to use, between 0.0 and 2.0. Higher
                values like 0.8 will make the output more random, while lower values like 0.2
                will make it more focused and deterministic.
        """
        self._client = None            # OpenAI() object
        self._model = model            # OpenAI model
        self._base_temp = temperature  # Temperature (see: help(OpenAI().chat.completions.create))
        self._base_messages = [
            {'role': 'system', BASE_MSG_CONTENT_KEY: DEFAULT_SYSTEM_CONTENT},
        ]
        # Content message indications the OpenAI did not answer a query
        self._failure_content = [
            "As an AI language model, I am committed to maintaining a respectful and "
            + "inclusive environment. I cannot endorse or participate in generating content "
            + "that is offensive, explicit, or inappropriate. If you have any other prompt or "
            + "topic you'd like me to help with, I'd be more than happy to assist you.",
            "I can't comply with this request.",
            "I'm unable to assist with that request.",
            "I'm sorry, I can't assist with that.",
            "Sorry, but I can't generate that story for you.",
        ]

    def __del__(self) -> None:
        """Ensure the OpenAi object is closed."""
        self.tear_down()

    def setup(self) -> None:
        """Validate everything but prepare just once."""
        # LOCAL VARIABLES
        api_key = os.environ.get(OPENAI_KEY_ENV_VAR)  # OpenAi API key
        if not api_key:
            raise RuntimeError('Be sure to export your OpenAI API key into the '
                               f'{OPENAI_KEY_ENV_VAR} environment variable')

        # VALIDATION
        self._validate_attributes()

        # SETUP
        if not self._client:
            self._client = OpenAI(api_key=api_key)

    def tear_down(self) -> None:
        """Shut it all down."""
        if self._client:
            self._client.close()
            self._client = None

    def change_system_content(self, new_content: str) -> None:
        """Overrides the default role:sytem content:_____ communicated to the OpenAI API.

        Args:
            new_content: New 'content' entry.
        """
        # INPUT VALIDATION
        validate_string(new_content, 'new_content', can_be_empty=True)

        # CHANGE IT
        self._base_messages[0][BASE_MSG_CONTENT_KEY] = new_content

    def create_content(self, messages: List, add_base_msgs: bool = True,
                       max_tokens: int = 50) -> str:
        """Communicate with OpenAI using the API.

        Args:
            messages: A list of string to pass to the OpenAi API.
            add_base_mesgs: Optional; If True, prepend messages with self._base_messages.

        Returns:
            The message content from the first choice.
        """
        local_msgs = messages  # Local copy of messages
        if add_base_msgs:
            local_msgs = self._base_messages + messages
        # chat.completion endpoint
        completion = self._client.chat.completions.create(model=self._model, messages=local_msgs,
                                                          max_tokens=max_tokens,
                                                          temperature=self._base_temp)
        # Strip all leading and trailing newlines
        answer = re.sub(r'^\n+|\n+$', '', completion.choices[0].message.content)

        # DONE
        return answer

    def generate_answer(self, prompt: str, length_limit: int = 45,
                        min_len: int = MIN_FITB_LEN) -> str:
        """Prompt OpenAI to generate an answer for the given prompt.

        Args:
            prompt: Prompt to give the AI to generate an answer for.
            length_limit: Optional; Maximum length of the answer.
            min_len: Optional; Min length of repeating undescores to be considered a fitb prompt.

        Returns:
            The generated answer as a string.
        """
        # LOCAL VARIABLES
        answer = ''    # Answer to the provided prompt
        messages = []  # Local copy of messages to update with actual query
        # Base prompt to prompt OpenAI to generate a single answer to a prompt
        content = f'Provide a humorous response within {length_limit} characters ' \
                  + f'characters for this prompt: "{prompt}".'

        # CLASS VALIDATION
        self.setup()

        # GENERATE IT
        if '_' * min_len in prompt:
            content = content + '  The prompt has a fill-in-the-blank placeholder so ensure ' \
                      + 'your answer makes sense grammatically.  Do not restate any part of ' \
                      + 'the orignal prompt in your answer.'
        messages.append({'role': 'user', 'content': content})
        answer = self.create_content(messages=messages)
        answer = polish_answer(prompt=prompt, answer=answer, length_limit=length_limit)

        # DONE
        return answer

    def generate_thriplash(self, prompt: str, length_limit: int = 30,
                           min_len: int = MIN_FITB_LEN) -> List[str]:
        """Prompt OpenAI to generate three separate answers for the given Thriplash prompt.

        Args:
            prompt: Prompt to give the AI to generate an answer for.
            length_limit: Optional; Maximum length of the answer.
            min_len: Optional; Min length of repeating undescores to be considered a fitb prompt.

        Returns:
            A list of length 3 which contains three strings.  One or more of the three strings
            may be empty.
        """
        # LOCAL VARIABLES
        raw_answer = ''  # Answer to the provided prompt
        answers = []     # Parse the raw answer into a list of length 3
        messages = []    # Local copy of messages to update with actual query
        # Base prompt to prompt OpenAI to generate a single answer to a prompt
        content = f'Answer the following Quiplash 3 Thriplash prompt: "{prompt}".  ' \
                  + f'Each individual funny answer should be less than {length_limit} ' \
                  + 'characters and should be on its own line.'

        # CLASS VALIDATION
        self.setup()

        # GENERATE IT
        # Generate
        if '_' * min_len in prompt:
            content = content + '  The prompt has some fill-in-the-blank placeholders so ensure ' \
                      + 'your answers make sense grammatically.  Do not restate any part of ' \
                      + 'the orignal prompt in your answer.'
        messages.append({'role': 'user', 'content': content})
        raw_answer = self.create_content(messages=messages)
        answers = [answer for answer in raw_answer.split('\n') if answer]
        # Validate results
        if not answers:
            raise RuntimeError(f'OpenAI did *not* generate content for {prompt}')
        if len(answers) < 3:
            for _ in range(3 - len(answers)):
                answers.append('')
        elif len(answers) > 3:
            Logger.debug(f'OpenAI generated more than just three lines here {answers}')
            answers = self._extract_thriplash_answer(answers=answers, length_limit=length_limit)
        # Polish the format
        answers = self._polish_thriplash_answers(answers=answers, length_limit=length_limit)

        # DONE
        return answers

    def vote_favorite(self, prompt: str, answers: list) -> str:
        """Prompt OpenAI to choose a favorite answer for the prompt from a list of options.

        Args:
            prompt: The original prompt.
            answers: A non-empty list of answers, as strings, to choose from.

        Returns:
            One of the answers entries.
        """
        # LOCAL VARIABLES
        favorite = ''                # Favorite from the answers list
        messages = []                # Local copy of messages to update with actual query
        choice_dict = OrderedDict()  # Ordered dictionary of choices
        choices = ''                 # Human-readable list formed from choice_dict
        # Base prompt to prompt OpenAI to generate a single answer to a prompt
        content = 'I am going to give you some answers for the Jackbox Games prompt ' \
                  + f'"{prompt}".  Pick the funniest answer from the choice list I give you.  ' \
                  + 'Your comma-separated choice list is: {}.  ' \
                  + 'Choose an answer from the choice list but only give me the letter.  ' \
                  + 'Do not create new content.  Do not create any additional answers.  ' \
                  + 'Do not create any new choices.  ' \
                  + 'Do not choose a letter that was not in your choice list.'

        # CLASS VALIDATION
        self.setup()

        # SETUP
        for answer in answers:
            choice_dict[chr(answers.index(answer) + 65)] = answer
        choices = ', '.join([key + '. ' + val.strip('\n') for (key, val) in choice_dict.items()])
        content = content.format(choices)

        # VOTE IT
        messages.append({'role': 'user', 'content': content})
        answer = self.create_content(messages=messages)
        favorite = self._extract_favorite(answer, choice_dict)

        # DONE
        return favorite

    def _extract_favorite(self, answer: str, choices: dict) -> str:
        """Extract a favorite from created content.

        Extract an answer from created content given a dictionary of available choices.  Will
        randomize a selection from the dictionary values on any failure.

        Args:
            answer: Content created by OpenAI.
            choices: A dictionary of available choices.  The keys represent shorthand
                identification

        Returns:
            One of the values from the choices dictionary.
        """
        # LOCAL VARIABLES
        favorite = ''  # The favorite chosen from among the choices values

        # INPUT VALIDATION
        if self._failed_request(answer):
            favorite = _randomize_choice(choices=choices)
            Logger.debug(f'OpenAI failed with {answer} so {favorite} was chosen randomly')
        # EXTRACT IT
        elif answer in choices.keys():
            favorite = choices[answer]  # Sometimes OpenAI follows instructions
            Logger.debug(f'OpenAI followed instructions and {favorite} was chosen')
        elif len(answer) != len(list(choices.keys())[0]) and answer[0] in choices.keys():
            favorite = choices[answer[0]]  # Sometimes OpenAI likes to add words
            Logger.debug(f'OpenAI added words but we extracted {favorite} from {answer}')
        else:
            # Did OpenAI give a response that wasn't a choice without failing the request?!
            favorite = _randomize_choice(choices=choices)
            Logger.debug(f'OpenAI went crazy with {answer} so {favorite} was chosen randomly')

        # DONE
        return favorite

    def _extract_thriplash_answer(self, answers: list, length_limit: int) -> list:
        """Extract just three meaningful thriplash answers when the AI got the assignmnet wrong.

        Some Thriplash prompts result in the AI providing three (or more) numbered lists of three
        answers.

        Args:
            answers: List of AI-generated Thriplash responses, as non-empty strings, that were
                split by newline.
            length_limit: The maximum length for each string in the return value list.

        Returns:
            A list of three strings.
        """
        # LOCAL VARIABLES
        new_answers = []   # New answers generated from provided answers
        temp_answers = []  # Holding variable while we polish up answers some

        # EXTRACT IT
        # Polish what we have
        # A. truncate to 3 so we don't anger _p_t_a(), B. ignore length limits since the first
        # list index probably holds all three of our answers.
        temp_answers = self._polish_thriplash_answers(answers=answers[:3], length_limit=sys.maxsize)
        # Find a candidate
        for temp_answer in temp_answers:
            if temp_answer and len(temp_answer.split(',')) == 3:
                new_answers = self._polish_thriplash_answers(answers=temp_answer.split(','),
                                                             length_limit=length_limit)
                break  # We're taking the first able-bodied candidate. Stop looking further.

        # DONE
        return new_answers

    def _failed_request(self, content: str) -> bool:
        """Check OpenAI's response content for evidence of failure.

        Args:
            content: Response from OpenAI.

        Returns:
            True if there was any indication that OpenAI could not comply with the request.
        """
        # LOCAL VARIABLES
        failed = False  # Found an indication of failure

        # DID IT FAIL?
        for fail_message in self._failure_content:
            if _match_phrase(fail_message, content):
                failed = True
                break

        # DONE
        return failed

    def _polish_thriplash_answers(self, answers: list, length_limit: int) -> list:
        """Polish the Thriplash answers in the list.

        Quotes, numbering, and bulleting will be removed.  The list length will be padded with
        empty strings if the length is less than three.

        Args:
            answers: List of one (minimum) to three (maximum) strings to polish.  Strings can be
                empty.
            length_limit: The maximum length for each string in the return value list.

        Returns:
            A list of three strings.
        """
        # LOCAL VARIABLES
        old_answer = ''        # Temp string to keep track of what an answer used to look like
        new_answers = answers  # Shiny, newly polished strings

        # INPUT VALIDATION
        validate_list(answers, 'answers', can_be_empty=False)
        if len(answers) > 3 or not answers:
            raise ValueError('answers list is the wrong size')
        for answer in answers:
            validate_string(answer, 'answers list entry')

        # POLISH IT
        # Polish the format
        for index, _ in enumerate(new_answers):
            # Chew on this index until it comes out clean
            while True:
                old_answer = new_answers[index]
                new_answers[index] = re.sub(r'^"|"$', '', new_answers[index])  # Quotes
                new_answers[index] = re.sub(r'^\d+\.\s+', '', new_answers[index])  # Numbering
                new_answers[index] = re.sub(r'^-', '', new_answers[index])  # Bulleting
                new_answers[index] = re.sub(r'^\s+', '', new_answers[index])  # Leading whitespace
                if new_answers[index] == old_answer:
                    break  # No change. We're done.
            # Final length check (because the completions endpoint keeps adding quotes and numbers)
            if len(new_answers[index]) > length_limit:
                new_answers[index] = new_answers[index][:length_limit]  # Truncate it

        # PAD IT
        while len(new_answers) < 3:
            new_answers.append('')

        # DONE
        return new_answers

    def _validate_attributes(self) -> None:
        """Validate internal attributes."""
        # Temperature
        if not isinstance(self._base_temp, int) and not isinstance(self._base_temp, float):
            raise TypeError(f'Invalid temperature type of {type(self._base_temp)}')
        if self._base_temp < 0.0 or self._base_temp > 2.0:
            raise ValueError(f'Invalid temperature of {self._base_temp} (must be between 0 and 2)')


def polish_answer(prompt: str, answer: str, length_limit: int, original_answer: str = None) -> str:
    """Polishes AI answers to improve the quality of responses.

    This function recursively performs the following until no other changes are necessary:
        1. Normalizes the encoding of the prompt to avoid encoding-shenanigans
        2. Removes leading and trailing quotes
        3. Removes overlap between the prompt and answer
        4. Removes trailing punctuation (in certain situations)
        5. Ensures the answer is no longer than length_limit

    Args:
        prompt: The original prompt.
        answer: The AI-generated answer.
        length_limit: Upper end limit for the length of the answer.
        original_answer: Optional; Keep track of the original through all the recursion.  If you
            *must* include a value for this argument, choose the same value as answer.

    Returns:
        An answer, which may or may not be modified.

    Raises:
        TypeError: Bad data type.
        ValueError: Bad value.
    """
    # LOCAL VARIABLES
    clean_prompt = ''    # Normalized verseion of prompt
    new_answer = answer  # A polished up version of answer
    final_run = False    # Final call in the recursive call stack

    # INPUT VALIDATION
    validate_string(prompt, 'prompt')
    validate_string(answer, 'answer')
    validate_type(length_limit, 'length_limit', int)
    if length_limit < 1:
        raise ValueError(f'The length_limit must be a positive number instead of {length_limit}')
    if original_answer:
        validate_string(original_answer, 'original_answer')
    else:
        original_answer = answer  # This is the first call

    # POLISH IT
    clean_prompt = clean_up_string(prompt)
    new_answer = clean_up_string(answer)
    if clean_prompt != prompt:
        Logger.debug(f'Successfully cleaned "{prompt}" to "{clean_prompt}"')
    if new_answer != answer:
        Logger.debug(f'Successfully cleaned "{answer}" to "{new_answer}"')
    # 1. Removes leading and trailing quotes
    new_answer = re.sub(r'^"|"$', '', new_answer)  # Strip leading and trailing quotes
    # 2. Removes overlap between the prompt and answer
    new_answer = remove_answer_overlap(prompt=clean_prompt, answer=new_answer)
    # 3. Removes trailing punctuation (in certain situations)
    new_answer = remove_punctuation(prompt=clean_prompt, answer=new_answer)
    # Save truncation for last
    if new_answer != answer:
        new_answer = polish_answer(prompt=clean_prompt, answer=new_answer,
                                   length_limit=length_limit, original_answer=original_answer)
    else:
        final_run = True
    # 4. Ensures the answer is no longer than length_limit
    if len(new_answer) > length_limit:
        new_answer = new_answer[:length_limit]

    # DONE
    if new_answer != original_answer and final_run:
        Logger.debug(f'Polished "{new_answer}" from "{original_answer}" for this: "{clean_prompt}"')
    return new_answer


def remove_answer_overlap(prompt: str, answer: str, min_len: int = MIN_FITB_LEN) -> str:
    """Remove any overlap between the prompt and answer for fill-in-the-blank prompts.

    OpenAI response don't do a good job of following instructions for the fill-in-the-blank
    prompts so we're going to help them.  This function will not change an answer for a prompt
    that does *not* include a fill-in-the-blank.

    Args:
        prompt: The original prompt.
        answer: The AI-generated answer.
        min_len: Optional; Minimum length of repeating undescores to be considered a fitb prompt.

    Returns:
        The answer to the prompt, modified or not.

    Raises:
        TypeError: Bad data type.
        ValueError: Empty string.
    """
    # LOCAL VARIABLES
    opening = ''         # Portion of the prompt preceding the blank
    closing = ''         # Portion of the prompt following the blank
    new_answer = answer  # Trimmed up version of answer
    broken_prompt = []   # Pieces/parts of the prompt
    regex_pattern = r''  # Use this regex split the prompt

    # INPUT VALIDATION
    validate_string(prompt, 'prompt')
    validate_string(answer, 'answer')
    validate_pos_int(min_len, 'min_len')

    # SPLIT IT
    # Matches on any min_len number of underscores anywhere
    regex_pattern = r'_{%d,}' % min_len  # pylint: disable = consider-using-f-string)
    broken_prompt = re.split(regex_pattern, prompt)

    # REMOVE OVERLAP
    if len(broken_prompt) == 2:
        opening = broken_prompt[0]   # Prompt substring before the blank
        closing = broken_prompt[1]   # Prompt substring after the blank
        opening = _get_leading_overlap(opening.lower(), answer.lower())  # Opening & answer overlap
        closing = _get_trailing_overlap(closing.lower(), answer.lower())  # Closing & answer overlap
        if opening:
            try:
                # Slice off leading overlap
                new_answer = new_answer[new_answer.lower().index(opening.lower()) + len(opening):]
            except ValueError as err:
                Logger.debug('remove_answer_overlap() failed slicing the opening overlap of '
                             + f'"{opening}" off of the current working answer of '
                             + f'"{new_answer}" with {repr(err)}!')
        if closing:
            try:
                # Slice off trailing overlap
                new_answer = new_answer[:new_answer.lower().index(closing.lower())]
            except ValueError as err:
                Logger.debug('remove_answer_overlap() failed slicing the trailing overlap of '
                             + f'"{closing}" off of the current working answer of '
                             + f'"{new_answer}" with {repr(err)}!')

    # DONE
    if new_answer != answer:
        Logger.debug(f'Trimmed "{new_answer}" from "{answer}" by removing overlap with '
                     f'this prompt: "{prompt}"')
    return new_answer


def remove_punctuation(prompt: str, answer: str, min_len: int = MIN_FITB_LEN) -> str:
    """Remove trailing punctuation from answer, depending on the prompt.

    Removes trailing punctuation from answer unless the prompt has a trailing fill-in-the-blank,
    sans prompt punctuation.  Never removes punctuation marks.

    Args:
        prompt: The original prompt.
        answer: The AI-generated answer.
        min_len: Optional; Minimum length of repeating undescores to be considered a fitb prompt.

    Returns:
        The answer to the prompt, modified or not.

    Raises:
        TypeError: Bad data type.
        ValueError: Empty string.
    """
    # LOCAL VARIABLES
    new_answer = answer    # A polished up version of answer
    blank = '_' * min_len  # Fill-in-the-blank substring

    # INPUT VALIDATION
    validate_string(prompt, 'prompt')
    validate_string(answer, 'answer')

    # REMOVE IT
    if not answer.endswith('!') and not prompt.endswith(blank):
        new_answer = new_answer.rstrip(punctuation)

    # DONE
    return new_answer


def _get_leading_overlap(haystack: str, needle: str) -> str:
    """Returns the trailing haystack and leading needle overlap sub-string."""
    overlap = ''  # Overlap between haystack and needle
    for i in range(1, len(needle)):
        if haystack.endswith(needle[:-i]):
            overlap = needle[:-i]
            break
    return overlap


def _get_trailing_overlap(haystack: str, needle: str) -> str:
    """Returns the leading haystack and trailing needle overlap sub-string."""
    overlap = ''  # Overlap between haystack and needle
    for i in range(1, len(needle)):
        if haystack.startswith(needle[i:]):
            overlap = needle[i:]
            break
    return overlap


def _match_phrase(needle: str, haystack: str, threshold: float = 0.75) -> bool:
    """Loosely match a needle and a haystack to an established threshold.

    If threshold percent, or more, of needle's words are found in haystack, then it is considered
    a phrase match.

    Args:
        needle: The string to match in haystack.
        haystack: The phrase to match against.
        threshold: Optional; The percentage, as a float, to constitutes a phrase match.

    Returns:
        True if threshold percentage of needle words were found in the haystack, False otherwise.
    """
    # LOCAL VARIABLES
    stripped_needle = ''  # A version of needle with all the punctuation and whitespace stripped out
    word_count = 0        # Number of needle words
    num_found = 0         # Number of needle words found in haystack
    matched = False       # The threshold has been surpassed

    # MATCH IT
    # Strip needle of all punctuation and most whitespace
    for char in needle:
        if char in string.punctuation:
            stripped_needle = stripped_needle + ' '
        elif char in string.whitespace:
            stripped_needle = stripped_needle + ' '
        else:
            stripped_needle = stripped_needle + char
    # Start matching
    for needle_word in stripped_needle.split(' '):
        word_count += 1
        if needle_word in haystack:
            num_found += 1
    # Check the threshold
    if num_found / word_count >= threshold:
        matched = True

    # DONE
    return matched


def _randomize_choice(choices: dict) -> str:
    """Randomize one of the values from choices."""
    return random.choice(list(choices.values()))
