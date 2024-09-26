"""Unit test module for jitb_openai.remove_answer_overlap().

Typical Usage:
    python -m test                                                          # Run *all* test cases
    python -m test.unit_test                                                # Run *all* unit tests
    python -m test.unit_test.test_openai                                    # Run openai tests
    python -m test.unit_test.test_openai.test_remove_answer_overlap         # Run these unit tests
    python -m test.unit_test.test_openai.test_remove_answer_overlap -k n01  # Run just the n01 tests
"""

# Standard Imports
from typing import Any
# Third Party Imports
from test.unit_test.test_jackbox_games import TestJackboxGames
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from jitb.jitb_openai import remove_answer_overlap


class TestJitbOpenaiRemoveAnswerOverlap(TestJackboxGames):
    """The jitb_openai.remove_answer_overlap() unit test class.

    This class provides base functionality to run NEBS unit tests for
    jitb_openai.remove_answer_overlap().
    """

    # CORE CLASS METHODS
    # Methods listed in call order

    # pylint: disable = too-many-arguments
    # I'm leaving it like this and Pylint will just have to deal.  I don't want to implement
    # a whole NamedTuple, or some such container, just so Pylint is happy with test code.
    def run_test_success(self, in_prompt: str, in_answer: str, exp_result: str,
                         use_kwargs: bool = False, in_min_len: int = 4) -> None:
        """Wraps the calls to self.set_test_input(), self.expect_return() and self.run_test()."""
        if use_kwargs:
            self.set_test_input(prompt=in_prompt, answer=in_answer, min_len=in_min_len)
        else:
            self.set_test_input(in_prompt, in_answer, in_min_len)
        self.expect_return(exp_result)
        self.run_test()

    def call_callable(self) -> Any:
        """Calls jitb_openai.remove_answer_overlap().

        Overrides the parent method.  Defines the way to call jitb_openai.remove_answer_overlap().

        Args:
            None

        Returns:
            Return value of jitb_openai.remove_answer_overlap()

        Raises:
            Exceptions raised by jitb_openai.remove_answer_overlap() are bubbled up and handled by
                TediousUnitTest
        """
        return remove_answer_overlap(*self._args, **self._kwargs)


class NormalTestJitbOpenaiRemoveAnswerOverlap(TestJitbOpenaiRemoveAnswerOverlap):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_n01_no_fitb(self):
        """Prompt does not contain a fill-in-the-blank."""
        in_prompt = 'This prompt does not have a fill-in-the-blank'  # Prompt test input
        in_answer = 'I agree that it does not'                       # Answer test input
        self.run_test_success(in_prompt, in_answer, in_answer)

    def test_n02_basic_fitb(self):
        """Basic test-author-created fill-in-the-blank input."""
        in_prompt = 'This ________ is an example of a Jackbox fill-in-the-blank'  # Prompt input
        exp_answer = 'I agree,'                                                   # Expected return
        in_answer = f' {exp_answer} is'                                           # Answer input
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n03_real_quiplash_2_fitb_prompt_v1(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v1."""
        # Test input for the prompt argument
        in_prompt = 'Never take a first date to a ________'
        # Expected return value
        exp_answer = 'funeral home.'
        # Test input for the answer argument
        in_answer = f'a {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n04_real_quiplash_2_fitb_prompt_v2(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v2."""
        # Test input for the prompt argument
        in_prompt = 'The next TV spin-off: Law and Order: Special ________ Unit'
        # Expected return value
        exp_answer = 'Pizza'
        # Test input for the answer argument
        in_answer = f'Law and Order: Special {exp_answer} Unit'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n05_real_quiplash_2_fitb_prompt_v3(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v3."""
        # Test input for the prompt argument
        in_prompt = 'Surprising photos to find on Garfield’s phone would be of ________.'
        # Expected return value
        exp_answer = 'Lasagna-themed selfies'
        # Test input for the answer argument
        in_answer = f'of {exp_answer}.'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n06_real_quiplash_2_fitb_prompt_v4(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v4."""
        # Test input for the prompt argument
        in_prompt = "What you’ve been searching for wasn’t inside you this whole time. " \
                    + 'It was in ________!'
        # Expected return value
        exp_answer = "your neighbor's fridge"
        # Test input for the answer argument
        in_answer = f'{exp_answer}!'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n07_real_quiplash_2_fitb_prompt_v5(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v5."""
        # Test input for the prompt argument
        in_prompt = 'Your secret recipe for apple sauce is to simply ________'
        # Expected return value
        exp_answer = 'add unicorn tears!'
        # Test input for the answer argument
        in_answer = f'simply {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n08_real_quiplash_2_fitb_prompt_v6(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v6."""
        # Test input for the prompt argument
        in_prompt = 'The next big reality show: America’s Got ________'
        # Expected return value
        exp_answer = 'Farts'
        # Test input for the answer argument
        in_answer = f"America’s Got {exp_answer}"
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n09_real_quiplash_2_fitb_prompt_v7(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v7."""
        # Test input for the prompt argument
        in_prompt = 'A terrible name for a hotel: The ________ Inn'
        # Expected return value
        exp_answer = 'Roach Motel'
        # Test input for the answer argument
        in_answer = f'The {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n10_real_quiplash_2_fitb_prompt_v8(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v8."""
        # Test input for the prompt argument
        in_prompt = 'You know your company is going out of business when you show up to work ' \
                    + 'and notice ________'
        # Expected return value
        exp_answer = 'Clowns running the show.'
        # Test input for the answer argument
        in_answer = exp_answer
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_n11_real_quiplash_2_fitb_prompt_v9(self):
        """Actual fill-in-the-blank prompt example from Quiplahs 2 v9."""
        # Test input for the prompt argument
        in_prompt = "A weird dad keeps all of his children’s ________ as memories"
        # Expected return value
        exp_answer = 'boogers'
        # Test input for the answer argument
        in_answer = f"his children’s {exp_answer}"
        self.run_test_success(in_prompt, in_answer, exp_answer)


class ErrorTestJitbOpenaiRemoveAnswerOverlap(TestJitbOpenaiRemoveAnswerOverlap):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_e01_bad_data_type_prompt_none(self):
        """Bad data type: prompt == None."""
        in_prompt = None    # Test input for the prompt argument
        in_answer = 'None'  # Test input for the answer argument
        self.set_test_input(prompt=in_prompt, answer=in_answer)
        self.expect_exception(TypeError,
                              "Invalid data type for prompt argument: <class 'NoneType'>")
        self.run_test()

    def test_e02_bad_data_type_prompt_list(self):
        """Bad data type: prompt == None."""
        in_prompt = ['Something', ' ________ ', 'else']  # Test input for the prompt argument
        in_answer = 'None'                               # Test input for the answer argument
        self.set_test_input(prompt=in_prompt, answer=in_answer)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e03_bad_data_type_answer_none(self):
        """Bad data type: prompt == None."""
        in_prompt = 'None'  # Test input for the prompt argument
        in_answer = None    # Test input for the answer argument
        self.set_test_input(prompt=in_prompt, answer=in_answer)
        self.expect_exception(TypeError,
                              "Invalid data type for answer argument: <class 'NoneType'>")
        self.run_test()

    def test_e04_bad_data_type_answer_list(self):
        """Bad data type: prompt == None."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = ['Something']              # Test input for the answer argument
        self.set_test_input(prompt=in_prompt, answer=in_answer)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e05_bad_value_prompt_empty(self):
        """Bad data type: prompt == ''."""
        in_prompt = ''       # Test input for the prompt argument
        in_answer = 'Empty'  # Test input for the answer argument
        self.set_test_input(prompt=in_prompt, answer=in_answer)
        self.expect_exception(ValueError, 'Prompt may not be empty')
        self.run_test()

    def test_e06_bad_value_answer_empty(self):
        """Bad data type: prompt == ''."""
        in_prompt = 'Empty'  # Test input for the prompt argument
        in_answer = ''       # Test input for the answer argument
        self.set_test_input(prompt=in_prompt, answer=in_answer)
        self.expect_exception(ValueError, 'Answer may not be empty')
        self.run_test()

    def test_e07_bad_data_type_min_len_none(self):
        """Bad data type: min_len == None."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = 'None'                     # Test input for the answer argument
        in_min_len = None                      # Test input for the min_len argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, min_len=in_min_len)
        self.expect_exception(TypeError,
                              "Invalid data type for min_len argument: <class 'NoneType'>")
        self.run_test()

    def test_e08_bad_data_type_min_len_str(self):
        """Bad data type: min_len == '4'."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = 'None'                     # Test input for the answer argument
        in_min_len = '4'                       # Test input for the min_len argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, min_len=in_min_len)
        self.expect_exception(TypeError, 'Invalid data type')
        self.run_test()

    def test_e09_bad_value_min_len_zero(self):
        """Bad data type: min_len == 0."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = 'None'                     # Test input for the answer argument
        in_min_len = 0                         # Test input for the min_len argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, min_len=in_min_len)
        self.expect_exception(ValueError, 'Min_len must be positive')
        self.run_test()

    def test_e09_bad_value_min_len_negative(self):
        """Bad data type: min_len == -1."""
        in_prompt = 'Something ________ else'  # Test input for the prompt argument
        in_answer = 'None'                     # Test input for the answer argument
        in_min_len = -1                        # Test input for the min_len argument
        self.set_test_input(prompt=in_prompt, answer=in_answer, min_len=in_min_len)
        self.expect_exception(ValueError, 'Min_len must be positive')
        self.run_test()


class BoundaryTestJitbOpenaiRemoveAnswerOverlap(TestJitbOpenaiRemoveAnswerOverlap):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_b01_no_overlap(self):
        """No overlap between the prompt and answer."""
        # Test input for the prompt argument
        in_prompt = 'Nothing to see here'
        # Expected return value
        exp_answer = 'Keep moving'
        # Test input for the answer argument
        in_answer = exp_answer
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b02_single_char_overlap_leading(self):
        """Barely an overlap between the prompt and the answer: leading."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f' {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b03_single_char_overlap_trailing(self):
        """Barely an overlap between the prompt and the answer: trailing."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'{exp_answer} '
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b04_single_char_overlap_both_ends(self):
        """Barely an overlap between the prompt and the answer: both ends."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f' {exp_answer} '
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b05_single_char_overlap_leading(self):
        """Classless overlap between the prompt and the answer: leading."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f't {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b06_single_char_overlap_trailing(self):
        """Classless overlap between the prompt and the answer: trailing."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'{exp_answer} i'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b07_single_char_overlap_both_ends(self):
        """Classless overlap between the prompt and the answer: both ends."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f't {exp_answer} i'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b08_total_overlap_leading(self):
        """Total overlap between the prompt and the answer: leading."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'Some say that {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b09_total_overlap_trailing(self):
        """Total overlap between the prompt and the answer: trailing."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'{exp_answer} is unecessary'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_b10_total_overlap_both_ends(self):
        """Total overlap between the prompt and the answer: both ends."""
        # Test input for the prompt argument
        in_prompt = 'Some say that ________ is unecessary'
        # Expected return value
        exp_answer = 'testing'
        # Test input for the answer argument
        in_answer = f'Some say that {exp_answer} is unecessary'
        self.run_test_success(in_prompt, in_answer, exp_answer)


class SpecialTestJitbOpenaiRemoveAnswerOverlap(TestJitbOpenaiRemoveAnswerOverlap):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_s01_actual_fitb_but_good_answer(self):
        """Actual example of a fill-in-the-blank but AI answered it the right way.

        This is actual example input from Quiplash 2.
        """
        # Test input for the prompt argument
        in_prompt = 'Every airline flight should come with a free ________ for all passengers'
        # Test input for the answer argument
        in_answer = 'Snakes on a plane'
        self.run_test_success(in_prompt, in_answer, in_answer)

    def test_s02_leading_fitb_but_poor_answer(self):
        """The fill-in-the-blank begins the prompt and the answer has overlap."""
        # Test input for the prompt argument
        in_prompt = '________ is a terrible name for a hospital'
        # Expected return value
        exp_answer = 'Dollar Tree Mortuary'
        # Test input for the answer argument
        in_answer = f'{exp_answer} is a terrible name'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s03_trailing_fitb_but_poor_answer(self):
        """The fill-in-the-blank ends the prompt and the answer has overlap."""
        # Test input for the prompt argument
        in_prompt = 'Every airline flight should come with a free ________'
        # Expected return value
        exp_answer = 'snake'
        # Test input for the answer argument
        in_answer = f'a free {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s04_real_quiplash_2_fitb_prompt_punctuation(self):
        """This special case contains the prompts trailing text replicated inside the answer."""
        # Test input for the prompt argument
        in_prompt = 'A perplexing band would be Crosby, Stills, Nash, Young & ________'
        # Expected return value
        exp_answer = 'Old & Confused'
        # Test input for the answer argument
        in_answer = exp_answer
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s05_real_quiplash_2_fitb_prompt_case_mismatch_v1(self):
        """This special case contains part of the prompt but the case is different in the answer."""
        # Test input for the prompt argument
        in_prompt = 'A rejected superhero vehicle: the ________mobile'
        # Expected return value
        exp_answer = 'Fart'
        # Test input for the answer argument
        in_answer = f'The {exp_answer}mobile'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s06_real_quiplash_2_fitb_prompt_case_mismatch_v2(self):
        """This special case contains part of the prompt but the case is different in the answer."""
        # Test input for the prompt argument
        in_prompt = 'You know your company is going out of business when you show up to work ' \
                    + 'and notice ________'
        # Expected return value
        exp_answer = 'clowns running the show.'
        # Test input for the answer argument
        in_answer = f'Notice {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s07_fabricated_fitb_prompt_case_mismatch_v3(self):
        """This special case contains part of the prompt but the case is different in the answer."""
        # Test input for the prompt argument
        in_prompt = 'A rejected superhero vehicle: the ________mobile'
        # Expected return value
        exp_answer = 'Fart'
        # Test input for the answer argument
        in_answer = f'the {exp_answer}Mobile'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s08_fabricated_fitb_prompt_case_mismatch_v4(self):
        """This special case contains part of the prompt but the case is different in the answer."""
        # Test input for the prompt argument
        in_prompt = 'You know your company is going out of business when you show up to work ' \
                    + 'and notice ________'
        # Expected return value
        exp_answer = 'clowns running the show.'
        # Test input for the answer argument
        in_answer = f'Notice {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s09_variable_length_fitb_way_too_short(self):
        """Fill in the blank sub-string is much shorter than actual observed strings.

        Current implementation will likely use hard-coded prompt string.  As such, shorter strings
        will not be counted.  If this becomes a problem in the future, use this test case to
        highlight the change in behavior.

        EDIT: It became a problem when I discovered that different Jackbox Games use different
        length prompts.  Refactored to use regex to split on a repeating-underscore-string
        of a minimum length instead of using a hard-coded value.
        """
        # Test input for the prompt argument
        in_prompt = 'This blank ____ is way too short'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s10_variable_length_fitb_barely_too_short(self):
        """Fill in the blank sub-string is barely shorter than actual observed strings.

        Current implementation will likely use hard-coded prompt string.  As such, shorter strings
        will not be counted.  If this becomes a problem in the future, use this test case to
        highlight the change in behavior.

        EDIT: It became a problem when I discovered that different Jackbox Games use different
        length prompts.  Refactored to use regex to split on a repeating-underscore-string
        of a minimum length instead of using a hard-coded value.
        """
        # Test input for the prompt argument
        in_prompt = 'This blank _______ is barely too short'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = F'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s11_variable_length_fitb_barely_too_long(self):
        """Fill in the blank sub-string is barely longer than actual observed strings.

        Current implementation will likely use hard-coded prompt string.  As such, longer
        fill-in-the-blank strings could become a problem.  If this becomes a problem in the
        future, use this test case to verify the change in behavior.

        EDIT: It became a problem when I discovered that different Jackbox Games use different
        length prompts.  Refactored to use regex to split on a repeating-underscore-string
        of a minimum length instead of using a hard-coded value.
        """
        # Test input for the prompt argument
        in_prompt = 'This blank _________ is barely too long'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s12_variable_length_fitb_way_too_short(self):
        """Fill in the blank sub-string is much longer than actual observed strings.

        Current implementation is passing this test case as desired but future changes could
        make this a problem.  If this becomes a problem in the future, use this test case to
        verify the change in behavior.

        EDIT: It became a problem when I discovered that different Jackbox Games use different
        length prompts.  Refactored to use regex to split on a repeating-underscore-string
        of a minimum length instead of using a hard-coded value.
        """
        # Test input for the prompt argument
        in_prompt = 'This blank _______________ is much too long'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s13_more_than_one_fitb(self):
        """Input prompt has multiple fill-in-the-blanks.

        Current design of the function will be to ignore this input, as if there was no
        fill-in-the-blank at all.  If this functionality ever needs to change, use this test case
        to help define the new behavior.
        """
        # Test input for the prompt argument
        in_prompt = 'This function does not like ________ or ________ as input'
        # Test input for the answer argument
        in_answer = 'like bad data types or ill-formed values as input'
        self.run_test_success(in_prompt, in_answer, in_answer)

    def test_s14_variable_length_fitb_way_too_short(self):
        """Fill in the blank sub-string is double the length of actual observed strings.

        The current implementation treats this as there being two fill-in-the-blanks, which is
        fine.  Even so, it just returns the original answer, unedited, which is also fine.

        EDIT: The refactor necessitated an update to this test case.  The old implementation
        became a problem when I discovered that different Jackbox Games use different
        length prompts.  Refactored to use regex to split on a repeating-underscore-string
        of a minimum length instead of using a hard-coded value.
        """
        # Test input for the prompt argument
        in_prompt = 'This blank ________________ is much too long'
        # Expected return value
        exp_answer = 'certainly'
        # Test input for the answer argument
        in_answer = f'blank {exp_answer} is'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s15_actual_behavior_v1(self):
        """Behavior observed during actual execution v1."""
        # Test input for the prompt argument
        in_prompt = 'Joke 2 (of 2) Write your punchline: i have more eggs than _______'
        # Expected return value
        exp_answer = 'a chicken on steroids'
        # Test input for the answer argument
        in_answer = f'i have more eggs than {exp_answer}'
        self.run_test_success(in_prompt, in_answer, exp_answer)

    def test_s16_min_len_test_short_v1(self):
        """New min_len feature test: min_len == 1."""
        # Test input for the prompt argument
        in_prompt = 'this_will_not_trim_because_there_is_too_many_underscores'
        # Expected return value
        exp_answer = 'this will_not_trim'
        # Test input for the answer argument
        in_answer = exp_answer
        in_min_len = 1  # Test input for min_len
        self.run_test_success(in_prompt, in_answer, exp_answer, in_min_len=in_min_len)

    def test_s17_min_len_test_short_v2(self):
        """New min_len feature test: min_len == 1."""
        # Test input for the prompt argument
        in_prompt = 'This _ trim because it will match'
        # Expected return value
        exp_answer = 'will'
        # Test input for the answer argument
        in_answer = f'This {exp_answer} trim'
        in_min_len = 1  # Test input for min_len
        self.run_test_success(in_prompt, in_answer, exp_answer, in_min_len=in_min_len)

    def test_s18_min_len_test_short_v3(self):
        """New min_len feature test: min_len == 1."""
        # Test input for the prompt argument
        in_prompt = 'This __ trim because it will match'
        # Expected return value
        exp_answer = 'will'
        # Test input for the answer argument
        in_answer = f'This {exp_answer} trim'
        in_min_len = 1  # Test input for min_len
        self.run_test_success(in_prompt, in_answer, exp_answer, in_min_len=in_min_len)


if __name__ == '__main__':
    execute_test_cases()
