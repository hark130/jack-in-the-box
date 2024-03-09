"""Unit test module for jitb_openai.polish_answer().

Typical Usage:
    python -m test                                                  # Run *all* test cases
    python -m test.unit_test                                        # Run *all* unit tests
    python -m test.unit_test.test_openai                            # Run openai tests
    python -m test.unit_test.test_openai.test_polish_answer         # Run these unit tests
    python -m test.unit_test.test_openai.test_polish_answer -k n01  # Run just the n01 tests
"""

# Standard Imports
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jitb_openai import polish_answer


# pylint: disable = too-many-arguments, too-many-public-methods
class TestJitbOpenaiPolishAnswer(TestJackboxGames):
    """The jitb_openai.polish_answer() unit test class.

    This class provides base functionality to run NEBS unit tests for
    jitb_openai.polish_answer().
    """

    # CORE CLASS METHODS
    # Methods listed in call order

    def run_test_success(self, in_prompt: str, in_answer: str, in_limit: int, exp_result: str,
                         use_kwargs: bool = False) -> None:
        """Wraps the calls to self.set_test_input(), self.expect_return() and self.run_test()."""
        if use_kwargs:
            self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        else:
            self.set_test_input(in_prompt, in_answer, in_limit)
        self.expect_return(exp_result)
        self.run_test()

    def call_callable(self) -> Any:
        """Calls jitb_openai.polish_answer().

        Overrides the parent method.  Defines the way to call jitb_openai.polish_answer().

        Args:
            None

        Returns:
            Return value of jitb_openai.polish_answer()

        Raises:
            Exceptions raised by jitb_openai.polish_answer() are bubbled up and handled by
                TediousUnitTest
        """
        return polish_answer(*self._args, **self._kwargs)


class NormalTestJitbOpenaiPolishAnswer(TestJitbOpenaiPolishAnswer):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_legacy_rao_input_no_fitb(self):
        """Prompt does not contain a fill-in-the-blank.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45                                                # The length_limit argument
        in_prompt = 'This prompt does not have a fill-in-the-blank'  # Prompt test input
        in_answer = 'I agree that it does not'                       # Answer test input
        self.run_test_success(in_prompt, in_answer, in_limit, in_answer)

    def test_n02_legacy_rao_input_basic_fitb(self):
        """Basic test-author-created fill-in-the-blank input.

        Legacy, but modified, jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45                                                             # length_limit arg
        in_prompt = 'This ________ is an example of a Jackbox fill-in-the-blank'  # Prompt input
        exp_answer = 'I agree'                                                    # Expected return
        in_answer = f' {exp_answer}, is'                                          # Answer input
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n03_legacy_rao_input_real_quiplash_2_fitb_prompt_v1(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v1.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Never take a first date to a ________'
        # Expected return value
        exp_answer = 'funeral home.'
        # Test input for the answer argument
        in_answer = f'a {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n04_legacy_rao_input_real_quiplash_2_fitb_prompt_v2(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v2.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'The next TV spin-off: Law and Order: Special ________ Unit'
        # Expected return value
        exp_answer = 'Pizza'
        # Test input for the answer argument
        in_answer = f'Law and Order: Special {exp_answer} Unit'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n05_legacy_rao_input_real_quiplash_2_fitb_prompt_v3(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v3.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Surprising photos to find on Garfield’s phone would be of ________.'
        # Expected return value
        exp_answer = 'Lasagna-themed selfies'
        # Test input for the answer argument
        in_answer = f'of {exp_answer}.'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n06_legacy_rao_input_real_quiplash_2_fitb_prompt_v4(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v4.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = "What you’ve been searching for wasn’t inside you this whole time. " \
                    + 'It was in ________!'
        # Expected return value
        exp_answer = "your neighbor's fridge"
        # Test input for the answer argument
        in_answer = f'{exp_answer}!'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n07_legacy_rao_input_real_quiplash_2_fitb_prompt_v5(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v5.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Your secret recipe for apple sauce is to simply ________'
        # Expected return value
        exp_answer = 'add unicorn tears!'
        # Test input for the answer argument
        in_answer = f'simply {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n08_legacy_rao_input_real_quiplash_2_fitb_prompt_v6(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v6.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'The next big reality show: America’s Got ________'
        # Expected return value
        exp_answer = 'Farts'
        # Test input for the answer argument
        in_answer = f"America’s Got {exp_answer}"
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n09_legacy_rao_input_real_quiplash_2_fitb_prompt_v7(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v7.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A terrible name for a hotel: The ________ Inn'
        # Expected return value
        exp_answer = 'Roach Motel'
        # Test input for the answer argument
        in_answer = f'The {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n10_legacy_rao_input_real_quiplash_2_fitb_prompt_v8(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v8.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'You know your company is going out of business when you show up to work ' \
                    + 'and notice ________'
        # Expected return value
        exp_answer = 'Clowns running the show.'
        # Test input for the answer argument
        in_answer = exp_answer
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n11_legacy_rao_input_real_quiplash_2_fitb_prompt_v9(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v9.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = "A weird dad keeps all of his children’s ________ as memories"
        # Expected return value
        exp_answer = 'boogers'
        # Test input for the answer argument
        in_answer = f"his children’s {exp_answer}"
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n12_single_feature_leading_quotes(self):
        """Tests a single feature: leading quotes."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A great name for a superhero who can communicate with cats'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'
        # Test input for the answer argument
        in_answer = f'"{exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n13_single_feature_trailing_quotes(self):
        """Tests a single feature: trailing quotes."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A great name for a superhero who can communicate with cats'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'
        # Test input for the answer argument
        in_answer = f'{exp_answer}"'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n14_single_feature_trailing_quotes(self):
        """Tests a single feature: wrapped quotes."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A great name for a superhero who can communicate with cats'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'
        # Test input for the answer argument
        in_answer = f'"{exp_answer}"'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n15_single_feature_trailing_punctuation_positive(self):
        """Tests a single feature: trailing punctuation to remove."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A great name for a superhero who can communicate with cats'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'
        # Test input for the answer argument
        in_answer = f'{exp_answer}.'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n16_single_feature_trailing_punctuation_negative_v1(self):
        """Tests a single feature: trailing punctuation to leave alone; exclamation."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A great name for a superhero who can communicate with cats'
        # Expected return value
        exp_answer = 'Feline Friend Fatale!'
        # Test input for the answer argument
        in_answer = f'{exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n17_single_feature_trailing_punctuation_negative_v2(self):
        """Tests a single feature: trailing punctuation to leave alone; fitb."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = "The next big reality show: America’s Got ________"
        # Expected return value
        exp_answer = 'Farts.'
        # Test input for the answer argument
        in_answer = f'{exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n18_single_feature_shorten_answer(self):
        """Tests a single feature: trailing punctuation to remove."""
        in_limit = 4  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = 'Feline Friend Fatale'
        # Expected return value
        exp_answer = in_answer[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n19_compound_features_two_v1(self):
        """Tests feature interoperability: [ ] quotes, [X] overlap, [ ] punctuation, [X] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = 'Feline Friend Fatale is a great name'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n20_compound_features_two_v2(self):
        """Tests feature interoperability: [X] quotes, [ ] overlap, [ ] punctuation, [X] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale"'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n21_compound_features_two_v3(self):
        """Tests feature interoperability: [X] quotes, [ ] overlap, [X] punctuation, [ ] long."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale."'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n22_compound_features_two_v4(self):
        """Tests feature interoperability: [ ] quotes, [X] overlap, [X] punctuation, [ ] long."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = 'Feline Friend Fatale is a great name?'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n23_compound_features_three_v1(self):
        """Tests feature interoperability: [ ] quotes, [X] overlap, [X] punctuation, [X] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale" is a great name!'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n24_compound_features_three_v2(self):
        """Tests feature interoperability: [X] quotes, [ ] overlap, [X] punctuation, [X] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale!"'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n25_compound_features_three_v3(self):
        """Tests feature interoperability: [X] quotes, [X] overlap, [ ] punctuation, [X] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale" is a great name'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n26_compound_features_three_v4(self):
        """Tests feature interoperability: [X] quotes, [X] overlap, [X] punctuation, [ ] long."""
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale" is a great name.'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_n27_compound_features_one_with_everything(self):
        """Tests feature interoperability: [X] quotes, [X] overlap, [X] punctuation, [X] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '"Feline Friend Fatale" is a great name!'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)


class ErrorTestJitbOpenaiPolishAnswer(TestJitbOpenaiPolishAnswer):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_prompt_none(self):
        """Bad data type: prompt == None."""
        in_prompt = None    # Test input for the prompt argument
        in_answer = 'None'  # Test input for the answer argument
        in_limit = 45       # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(TypeError,
                              "Invalid data type for prompt argument: <class 'NoneType'>")
        self.run_test()

    def test_e02_bad_data_type_prompt_list(self):
        """Bad data type: prompt == None."""
        in_prompt = ['Something', ' ________ ', 'else']  # Test input for the prompt argument
        in_answer = 'None'                               # Test input for the answer argument
        in_limit = 45                                    # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e03_bad_data_type_answer_none(self):
        """Bad data type: prompt == None."""
        in_prompt = 'None'  # Test input for the prompt argument
        in_answer = None    # Test input for the answer argument
        in_limit = 45       # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(TypeError,
                              "Invalid data type for answer argument: <class 'NoneType'>")
        self.run_test()

    def test_e04_bad_data_type_answer_list(self):
        """Bad data type: prompt == None."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = ['Something']              # Test input for the answer argument
        in_limit = 45                          # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e05_bad_data_type_length_limit_none(self):
        """Bad data type: length_limit == None."""
        in_prompt = 'None'  # Test input for the prompt argument
        in_answer = 'N'     # Test input for the answer argument
        in_limit = None     # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(TypeError,
                              'The length_limit argument must be an int')
        self.run_test()

    def test_e06_bad_data_type_length_limit_str(self):
        """Bad data type: length_limit == '45'."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = 'Something'                # Test input for the answer argument
        in_limit = '45'                        # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(TypeError, 'The length_limit argument must be an int')
        self.run_test()

    def test_e07_bad_value_prompt_empty(self):
        """Bad data type: prompt == ''."""
        in_prompt = ''       # Test input for the prompt argument
        in_answer = 'Empty'  # Test input for the answer argument
        in_limit = 45        # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(ValueError, 'Prompt may not be empty')
        self.run_test()

    def test_e08_bad_value_answer_empty(self):
        """Bad data type: prompt == ''."""
        in_prompt = 'Empty'  # Test input for the prompt argument
        in_answer = ''       # Test input for the answer argument
        in_limit = 45        # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(ValueError, 'Answer may not be empty')
        self.run_test()

    def test_e09_bad_value_length_limit_negative(self):
        """Bad data type: length_limit == -45."""
        in_prompt = 'Empty'  # Test input for the prompt argument
        in_answer = 'E'      # Test input for the answer argument
        in_limit = -45       # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(ValueError, 'The length_limit must be a positive number')
        self.run_test()


class BoundaryTestJitbOpenaiPolishAnswer(TestJitbOpenaiPolishAnswer):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_b01_legacy_rao_input_no_overlap(self):
        """No overlap between the prompt and answer.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Nothing to see here'
        # Expected return value
        exp_answer = 'Keep moving'
        # Test input for the answer argument
        in_answer = exp_answer
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b02_legacy_rao_input_single_char_overlap_leading(self):
        """Barely an overlap between the prompt and the answer: leading.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f' {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b03_legacy_rao_input_single_char_overlap_trailing(self):
        """Barely an overlap between the prompt and the answer: trailing.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'{exp_answer} '
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b04_legacy_rao_input_single_char_overlap_both_ends(self):
        """Barely an overlap between the prompt and the answer: both ends.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f' {exp_answer} '
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b05_legacy_rao_input_single_char_overlap_leading(self):
        """Classless overlap between the prompt and the answer: leading.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f't {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b06_legacy_rao_input_single_char_overlap_trailing(self):
        """Classless overlap between the prompt and the answer: trailing.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'{exp_answer} i'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b07_legacy_rao_input_single_char_overlap_both_ends(self):
        """Classless overlap between the prompt and the answer: both ends.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f't {exp_answer} i'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b08_legacy_rao_input_total_overlap_leading(self):
        """Total overlap between the prompt and the answer: leading.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'Some say that {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b09_legacy_rao_input_total_overlap_trailing(self):
        """Total overlap between the prompt and the answer: trailing.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'{exp_answer} is unecessary'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b10_legacy_rao_input_total_overlap_both_ends(self):
        """Total overlap between the prompt and the answer: both ends.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'Some say that {exp_answer} is unecessary'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b11_very_bad_value_length_limit_negative(self):
        """Bad value: length_limit == -100."""
        in_prompt = 'Bad Value'  # Test input for the prompt argument
        in_answer = 'Val'        # Test input for the answer argument
        in_limit = -100          # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(ValueError, 'The length_limit must be a positive number')
        self.run_test()

    def test_b12_barely_bad_value_length_limit_negative(self):
        """Bad value: length_limit == -1."""
        in_prompt = 'Bad Value'  # Test input for the prompt argument
        in_answer = 'Val'        # Test input for the answer argument
        in_limit = -1            # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(ValueError, 'The length_limit must be a positive number')
        self.run_test()

    def test_b13_barely_bad_value_length_limit_zero(self):
        """Bad value: length_limit == 0."""
        in_prompt = 'Bad Value'  # Test input for the prompt argument
        in_answer = 'Val'        # Test input for the answer argument
        in_limit = 0             # Test input for the length_limit argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, length_limit=in_limit)
        self.expect_exception(ValueError, 'The length_limit must be a positive number')
        self.run_test()

    def test_b14_barely_good_value_length_limit_one(self):
        """Good value: length_limit == 1."""
        in_limit = 1  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = "A weird dad keeps all of his children’s ________ as memories"
        # Expected return value
        exp_answer = 'b'
        # Test input for the answer argument
        in_answer = ' boogers as'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b15_good_value_length_limit_less_than_answer(self):
        """Good value: length_limit == 6."""
        in_limit = 6  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This prompt is fabricated input'
        # Test input for the answer argument
        in_answer = 'This answer is also fabricated'
        # Expected return value
        exp_answer = in_answer[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_b16_good_value_length_limit_more_than_answer(self):
        """Good value: length_limit == 6."""
        in_limit = 60  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This prompt is fabricated input'
        # Test input for the answer argument
        in_answer = 'This answer is also fabricated'
        # Expected return value
        exp_answer = in_answer
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)


class SpecialTestJitbOpenaiPolishAnswer(TestJitbOpenaiPolishAnswer):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_legacy_rao_input_actual_fitb_but_good_answer(self):
        """Actual example of a fill-in-the-blank but AI answered it the right way.

        This is actual example input from Quiplash 2.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Every airline flight should come with a free ________ for all passengers'
        # Test input for the answer argument
        in_answer = 'Snakes on a plane'
        self.run_test_success(in_prompt, in_answer, in_limit, in_answer)

    def test_s02_legacy_rao_input_leading_fitb_but_poor_answer(self):
        """The fill-in-the-blank begins the prompt and the answer has overlap.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = '________ is a terrible name for a hospital'
        # Expected return value
        exp_answer = 'Dollar Tree Mortuary'
        # Test input for the answer argument
        in_answer = f'{exp_answer} is a terrible name'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s03_legacy_rao_input_trailing_fitb_but_poor_answer(self):
        """The fill-in-the-blank ends the prompt and the answer has overlap.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'Every airline flight should come with a free ________'
        # Expected return value
        exp_answer = 'snake'
        # Test input for the answer argument
        in_answer = f'a free {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s04_legacy_rao_input_real_quiplash_2_fitb_prompt_punctuation(self):
        """This special case contains the prompts trailing text replicated inside the answer.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A perplexing band would be Crosby, Stills, Nash, Young & ________'
        # Expected return value
        exp_answer = 'Old & Confused'
        # Test input for the answer argument
        in_answer = exp_answer
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s05_legacy_rao_input_real_quiplash_2_fitb_prompt_case_mismatch_v1(self):
        """This special case contains part of the prompt but the case is different in the answer.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A rejected superhero vehicle: the ________mobile'
        # Expected return value
        exp_answer = 'Fart'
        # Test input for the answer argument
        in_answer = f'The {exp_answer}mobile'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s06_legacy_rao_input_real_quiplash_2_fitb_prompt_case_mismatch_v2(self):
        """This special case contains part of the prompt but the case is different in the answer.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'You know your company is going out of business when you show up to work ' \
                    + 'and notice ________'
        # Expected return value
        exp_answer = 'clowns running the show.'
        # Test input for the answer argument
        in_answer = f'Notice {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s07_legacy_rao_input_fabricated_fitb_prompt_case_mismatch_v3(self):
        """This special case contains part of the prompt but the case is different in the answer.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'A rejected superhero vehicle: the ________mobile'
        # Expected return value
        exp_answer = 'Fart'
        # Test input for the answer argument
        in_answer = f'the {exp_answer}Mobile'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s08_legacy_rao_input_fabricated_fitb_prompt_case_mismatch_v4(self):
        """This special case contains part of the prompt but the case is different in the answer.

        Legacy jitb_openai.remove_answer_overlap() test case.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'You know your company is going out of business when you show up to work ' \
                    + 'and notice ________'
        # Expected return value
        exp_answer = 'clowns running the show.'
        # Test input for the answer argument
        in_answer = f'Notice {exp_answer}'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s09_legacy_rao_input_variable_length_fitb_way_too_short(self):
        """Fill in the blank sub-string is much shorter than actual observed strings.

        Legacy jitb_openai.remove_answer_overlap() test case.

        Current implementation will likely use hard-coded prompt string.  As such, shorter strings
        will not be counted.  If this becomes a problem in the future, use this test case to
        highlight the change in behavior.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This blank ____ is way too short'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s10_legacy_rao_input_variable_length_fitb_barely_too_short(self):
        """Fill in the blank sub-string is barely shorter than actual observed strings.

        Legacy jitb_openai.remove_answer_overlap() test case.

        Current implementation will likely use hard-coded prompt string.  As such, shorter strings
        will not be counted.  If this becomes a problem in the future, use this test case to
        highlight the change in behavior.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This blank _______ is barely too short'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s11_legacy_rao_input_variable_length_fitb_barely_too_long(self):
        """Fill in the blank sub-string is barely longer than actual observed strings.

        Legacy jitb_openai.remove_answer_overlap() test case.

        Current implementation will likely use hard-coded prompt string.  As such, longer
        fill-in-the-blank strings could become a problem.  If this becomes a problem in the
        future, use this test case to verify the change in behavior.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This blank _________ is barely too long'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer}_ is'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s12_legacy_rao_input_variable_length_fitb_way_too_short(self):
        """Fill in the blank sub-string is much longer than actual observed strings.

        Legacy jitb_openai.remove_answer_overlap() test case.

        Current implementation is passing this test case as desired but future changes could
        make this a problem.  If this becomes a problem in the future, use this test case to
        verify the change in behavior.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This blank _______________ is much too long'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer}_______ is'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s13_legacy_rao_input_more_than_one_fitb(self):
        """Input prompt has multiple fill-in-the-blanks.

        Legacy jitb_openai.remove_answer_overlap() test case.

        Current design of the function will be to ignore this input, as if there was no
        fill-in-the-blank at all.  If this functionality ever needs to change, use this test case
        to help define the new behavior.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This function does not like ________ or ________ as input'
        # Test input for the answer argument
        in_answer = 'like bad data types or ill-formed values as input'
        # Expected return value
        exp_answer = in_answer[:45]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s14_legacy_rao_input_variable_length_fitb_way_too_short(self):
        """Fill in the blank sub-string is double the length of actual observed strings.

        Legacy jitb_openai.remove_answer_overlap() test case.

        The current implementation treats this as there being two fill-in-the-blanks, which is
        fine.  Even so, it just returns the original answer, unedited, which is also fine.
        """
        in_limit = 45  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'This blank ________________ is much too long'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)

    def test_s15_compound_features_multiples_of_everything(self):
        """Tests feature interoperability: [2] quotes, [1] overlap, [2] punctuation, [1] long."""
        in_limit = 10  # Test input for the length_limit argument
        # Test input for the prompt argument
        in_prompt = 'I think ________ is a great name for a superhero who can communicate with cats'
        # Test input for the answer argument
        in_answer = '""Feline Friend Fatale." is a great name?"'
        # Expected return value
        exp_answer = 'Feline Friend Fatale'[:in_limit]
        self.run_test_success(in_prompt, in_answer, in_limit, exp_answer)
# pylint: enable = too-many-arguments, too-many-public-methods


if __name__ == '__main__':
    execute_test_cases()
