"""The package's interface to OpenAI's API."""
# Standard
from collections import OrderedDict
import os
import re
import random
import string
# Third Party
from openai import OpenAI
# Local
from jitb.jitb_globals import OPENAI_KEY_ENV_VAR


'''
from jitb.jitb_openai import JitbAi
test = JitbAi()
test.setup()
'''


class JitbAi:
    """Implements the interface to the OpenAI API."""

    def __init__(self, model: str = 'gpt-3.5-turbo') -> None:
        """Class ctor.

        Args:
            model: Optional; OpenAI model to use.  See: https://platform.openai.com/docs/models
        """
        self._client = None    # OpenAI() object
        self._model = model    # OpenAI model
        self._base_temp = 0.0  # Base temperature.  See: help(OpenAI().chat.completions.create)
        self._base_messages = [
            {'role': 'system',
             'content': 'You are a funny person playing Jackbox Games Quiplash 3.'},
            # {'role': 'user', 'content': 'Tell me a funny joke.'}
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

    def setup(self) -> None:
        """Prepare everything just once."""
        # LOCAL VARIABLES
        api_key = os.environ.get(OPENAI_KEY_ENV_VAR)
        if not api_key:
            raise RuntimeError('Be sure to export your OpenAI API key into the '
                               f'{OPENAI_KEY_ENV_VAR} environment variable')

        # SETUP
        if not self._client:
            self._client = OpenAI(api_key=api_key)

    def tear_down(self) -> None:
        """Shut it all down."""
        if self._client:
            self._client.close()
            self._client = None

    def generate_answer(self, prompt: str, length_limit: int = 45) -> str:
        """Prompt OpenAI to generate an answer for the given prompt.

        Returns:
            The generated answer as a string.
        """
        # LOCAL VARIABLES
        answer = ''                     # Answer to the provided prompt
        messages = self._base_messages  # Local copy of messages to update with actual query
        # Base prompt to prompt OpenAI to generate a single answer to a prompt
        content = f'Give me a funny answer, limited to {length_limit} characters, ' \
                  + f'for the Quiplash 3 prompt "{prompt}" without using any previous context.'

        # CLASS VALIDATION
        self.setup()

        # GENERATE IT
        if '____' in prompt:
            content = content + '  The prompt has a fill-in-the-blank placeholder so ensure ' \
                      + 'your answer makes sense grammatically.  Do not restate any part of ' \
                      + 'the orignal prompt in your answer.'
        messages.append({'role': 'user', 'content': content})
        answer = self._create_content(messages=messages)
        answer = re.sub(r'^"|"$', '', answer)  # Strip leading and trailing quotes
        if len(answer) > length_limit:
            print(f'The {answer} was longer than {length_limit} so it got truncated')  # DEBUGGING
            answer = answer[:length_limit]

        # DONE
        return answer

    def generate_thriplash(self, prompt: str, length_limit: int = 30) -> list:
        """Prompt OpenAI to generate three separate answers for the given Thriplash prompt.

        Returns:
            A tuple of length 3 which contains three strings.  One or more of the three strings
            may be empty.
        """
        # LOCAL VARIABLES
        raw_answer = ''                 # Answer to the provided prompt
        answers = []                    # Parse the raw answer into a list of length 3
        messages = self._base_messages  # Local copy of messages to update with actual query
        # Base prompt to prompt OpenAI to generate a single answer to a prompt
        # content = 'Give me three funny answers, separated by newline characters, for the ' \
        #           + f'following Quiplash 3 Thriplash prompt: "{prompt}".  ' \
        #           + f'Each individual funny answer should be less than {length_limit} ' \
        #           + 'characters.'
        content = f'Answer the following Quiplash 3 Thriplash prompt: "{prompt}".  ' \
                  + f'Each individual funny answer should be less than {length_limit} ' \
                  + 'characters and should be on its own line.'

        # CLASS VALIDATION
        self.setup()

        # GENERATE IT
        # Generate
        if '____' in prompt:
            content = content + '  The prompt has some fill-in-the-blank placeholders so ensure ' \
                      + 'your answers make sense grammatically.  Do not restate any part of ' \
                      + 'the orignal prompt in your answer.'
        print(f'\nTHRIPLASH PROMPT: {prompt}')  # DEBUGGING
        print(f'\nCONTENT: {content}')  # DEBUGGING
        messages.append({'role': 'user', 'content': content})
        raw_answer = self._create_content(messages=messages)
        answers = [answer for answer in raw_answer.split('\n') if answer]
        # Validate results
        print(f'\nRAW ANSWERS: {raw_answer}')  # DEBUGGING
        print(f'\nANSWERS: {answers}')  # DEBUGGING
        if not answers:
            raise RuntimeError(f'OpenAI did *not* generate content for {prompt}')
        if len(answers) < 3:
            for _ in range(3 - len(answers)):
                answers.append('')
        elif len(answers) > 3:
            print(f'OpenAI generated more than just three lines here {answers}')  # DEBUGGING
            answers = answers[len(answers) - 3:]
        # Polish the format
        for index in range(0, len(answers)):
            for _ in range(2):
                # Do it twice because OpenAI be tricksey sometimes
                answers[index] = re.sub(r'^"|"$', '', answers[index])  # Remove quotes
                answers[index] = re.sub(r'^\d+\.\s+', '', answers[index])  # Strip numbering
            # Final length check (because the completions endpoint keeps adding quotes and numbers)
            if len(answers[index]) > length_limit:
                answers[index] = answers[index][:length_limit]  # Truncate it

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
        favorite = ''                   # Favorite from the answers list
        messages = self._base_messages  # Local copy of messages to update with actual query
        choice_dict = OrderedDict()     # Ordered dictionary of choices
        choices = ''                    # Human-readable list formed from choice_dict
        # Base prompt to prompt OpenAI to generate a single answer to a prompt
        content = f'I am going to give you some answers for the Quiplash 3 prompt "{prompt}".  ' \
                  + 'Pick the funniest answer from the choice list I give you.  ' \
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
        print(f'\nPROMPT: {prompt}')   # DEBUGGING
        print(f'\nCHOICES: {choices}')  # DEBUGGING
        print(f'\nCONTENT: {content}')  # DEBUGGING
        messages.append({'role': 'user', 'content': content})
        answer = self._create_content(messages=messages)
        favorite = self._extract_favorite(answer, choice_dict)

        # DONE
        return favorite

    def _create_content(self, messages=list) -> str:
        """Communicate with OpenAI using the API.

        Returns:
            The message content from the first choice.
        """
        # chat.completion endpoint
        #   GOOD NEWS: Maintained support
        # completion = self._client.chat.completions.create(model=self._model, messages=messages,
        #                                                   temperature=self._base_temp)
        # answer = completion.choices[0].message.content

        # completion endpoint
        #   BAD NEWS: Most models that support the legacy Completions endpoint will be shut off
        #       on January 4th, 2024.
        completion = self._client.completions.create(model='gpt-3.5-turbo-instruct',
                                                     prompt=messages[-1]['content'],
                                                     max_tokens=50,
                                                     temperature=self._base_temp)
        # Strip all leading and trailing newlines
        answer = re.sub(r'^\n+|\n+$', '', completion.choices[0].text)
        # print(f'COMPLETION: {completion}')  # DEBUGGING
        print(f"OPENAI'S ANSWER WAS {answer}")  # DEBUGGING
        return answer

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
            print(f'OpenAI failed with {answer} so {favorite} was chosen randomly')  # DEBUGGING
        # EXTRACT IT
        elif answer in choices.keys():
            favorite = choices[answer]  # Sometimes OpenAI follows instructions
            print(f'OpenAI followed instructions and {favorite} was chosen')  # DEBUGGING
        elif len(answer) != len(list(choices.keys())[0]) and answer[0] in choices.keys():
            favorite = choices[answer[0]]  # Sometimes OpenAI likes to add words
            print(f'OpenAI added words but we extracted {favorite} from {answer}')  # DEBUGGING
        else:
            # Did OpenAI give a response that wasn't a choice without failing the request?!
            favorite = _randomize_choice(choices=choices)
            print(f'OpenAI went crazy with {answer} so {favorite} was chosen randomly')  # DEBUGGING

        # DONE
        return favorite

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
