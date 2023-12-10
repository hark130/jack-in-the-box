"""The package's interface to OpenAI's API."""
# Standard
import os
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
        content = f'Give me a funny answer, limited to {length_limit} characters, for' \
                  + f'for the Quiplash 3 prompt "{prompt}"'

        # CLASS VALIDATION
        self.setup()

        # GENERATE IT
        messages.append({'role': 'user', 'content': content})
        answer = self._create_content(messages=messages)

        # DONE
        return answer

    def vote_favorite(self, prompt: str, answers: list) -> str:
        """Prompt OpenAI to choose a favorite answer for the prompt from a list of options.

        Args:
            prompt: The original prompt.
            answers: A non-empty list of answers, as strings, to choose from.

        Returns:
            One of the answers entries.
        """
        # LOCAL VARIABLES
        favorite = ''  # Favorite from the answers list

        # CLASS VALIDATION
        self.setup()

        # VOTE IT

        # DONE
        return favorite

    def _create_content(self, messages=list) -> str:
        """Communicate with OpenAI using the API.

        Returns:
            The message content from the first choice.
        """
        completion = self._client.chat.completions.create(model=self._model, messages=messages,
                                                          temperature=self._base_temp)
        answer = completion.choices[0].message.content
        print(f"OPENAI'S ANSWER WAS {answer}")  # DEBUGGING
        return answer
