"""A mocked interfact to the actual JitbAI class integrated into this package.

No need to burn up all the free tokens while we test jitb functionality.  This mocked class
was inherited from the real JitbAi class, so it will pass input validation, overrides the
JitbAi methods, and even saves the sole constructor argument as an attribute.
"""

# Standard Imports
import random
# Third Party Imports
# Local Imports
from jitb.jitb_openai import JitbAi, MIN_FITB_LEN


class MockedJitbAi(JitbAi):
    """Mock the interfaces for the actual JitbAi for the purposes of testing."""

    def __init__(self, *args, **kwargs) -> None:
        """Class ctor.

        Args:
            model: Optional; OpenAI model to use.  See: https://platform.openai.com/docs/models
        """
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        """Do nothing."""

    def tear_down(self) -> None:
        """Do nothing."""

    def generate_answer(self, prompt: str, length_limit: int = 45,
                        min_len: int = MIN_FITB_LEN) -> str:
        """Randomize from a generic list of answers."""
        generic_answers = ['42', 'the meaning of life', 'nothing', 'no one remembers',
                           'bubble gum', 'Maybe', 'Not sure', "It's possible", 'Could be.',
                           'Let me check', "Can't say", 'Likely', 'I doubt it',
                           "I'll think about it", 'Perhaps not', 'banana flavoring']
        return random.choice(generic_answers)[:length_limit]

    # pylint: disable = no-value-for-parameter
    def generate_thriplash(self, prompt: str, length_limit: int = 30,
                           min_len: int = MIN_FITB_LEN) -> list:
        """Get three response from generate_answer()."""
        answer_list = []
        for _ in range(3):
            answer_list.append(self.generate_answer(prompt=prompt, length_limit=length_limit,
                                                    min_len=min_len))
        return answer_list

    def vote_favorite(self, prompt: str, answers: list) -> str:
        """Randomly choose an answer."""
        return random.choice(answers)
