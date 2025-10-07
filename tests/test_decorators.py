"""Tests for the simplebench/decorators.py module."""
from __future__ import annotations

import pytest

from simplebench.decorators import clear_registered_cases, get_registered_cases, benchmark
from simplebench.enums import Verbosity
from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.session import Session


def mock_action(*arg, **kwargs) -> None:  # pylint: disable=unused-argument
    """A mock action that does nothing."""
    return None  # pragma: no cover


class MockRunner():
    """A mock SimpleRunner for testing."""

    def run(self, n: int, action, **kwargs):  # pylint: disable=unused-argument
        """Mock run method that just calls the action."""
        return action()


def test_benchmark_decorator_registers_case() -> None:
    """Test that the @benchmark decorator registers a case correctly."""
    # Clear any previously registered cases to ensure a clean test environment
    clear_registered_cases()
    assert len(get_registered_cases()) == 0, "Initial case registry not empty."
    initial_cases = get_registered_cases()
    initial_count = len(initial_cases)

    @benchmark(group='testgroup',
               title='Test Case',
               iterations=10,
               n=100,
               description="A simple test case function.")
    def test_case_function():
        """A simple test case function."""
        sum(range(100))  # pragma: no cover

    updated_cases = get_registered_cases()
    updated_count = len(updated_cases)

    assert updated_count == initial_count + 1, "Case count did not increase by 1 after decoration."

    # Verify that the last registered case matches the decorated function's details
    registered_case = updated_cases[-1]
    assert registered_case.group == 'testgroup'
    assert registered_case.title == 'Test Case'
    assert registered_case.iterations == 10
    assert registered_case.description == "A simple test case function."
    assert callable(registered_case.action), "Registered action is not callable."


def test_benchmark_decorator_preserves_functionality() -> None:
    """Test that the @benchmark decorator preserves the original function's behavior."""
    clear_registered_cases()

    @benchmark(group='math',
               title='Sum Function',
               iterations=5,
               min_time=0.5,
               max_time=2.0,
               variation_cols={"size": "Size"},
               kwargs_variations={"size": [10, 100, 1000]},
               n=50,
               description="Function to sum numbers from 0 to 49.")
    def sum_function(size: int) -> int:
        return sum(range(size))

    expected: int = sum(range(50))
    result: int = sum_function(50)
    assert result == expected, "The decorated function did not return the expected result."


def test_run_decorated_case() -> None:
    """Test that the action of a decorated case can be run."""
    clear_registered_cases()

    @benchmark(group='math',
               title='Sum Function',
               iterations=3,
               min_time=0.1,
               max_time=1.0,
               n=10,
               description="Function to sum numbers from 0 to 9.")
    def sum_function() -> int:
        return sum(range(10))

    cases = get_registered_cases()
    assert len(cases) == 1, "Expected exactly one registered case."

    case = cases[0]

    runner = MockRunner()
    result = case.action(runner)  # type: ignore
    expected = sum(range(10))
    assert result == expected, "The action did not return the expected result."

    clear_registered_cases()
    assert len(get_registered_cases()) == 0, "Case registry not empty after clearing."

    @benchmark(group='math2',
               title='Sum Function2',
               description="Function to sum numbers from 0 to 19.")
    def sum_function2() -> int:
        return sum(range(20))

    cases = get_registered_cases()
    assert len(cases) == 1, "Expected exactly one registered case."
    case = cases[0]
    result = case.action(runner)  # type: ignore
    expected = sum(range(20))
    assert result == expected, "The action did not return the expected result."


def test_decorator_invalid_title_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid title type."""
    clear_registered_cases()

    # Invalid title type (not a string)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title=123)  # type: ignore
        def invalid_title_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_TITLE_TYPE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_TITLE_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_blank_title() -> None:
    """Test that the @benchmark decorator raises expected errors for blank title."""
    clear_registered_cases()

    # Empty title value (only whitespace)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='   ')
        def empty_title_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_TITLE_VALUE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_TITLE_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_description_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid description type."""
    clear_registered_cases()

    # Invalid description type (not a string)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', description=456)  # type: ignore
        def invalid_description_type():    # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_TYPE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_blank_description() -> None:
    """Test that the @benchmark decorator raises expected errors for blank description."""
    clear_registered_cases()

    # Empty description value (only whitespace)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', description='   ')
        def empty_description_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_VALUE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_iterations_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid iterations type"""
    clear_registered_cases()

    # Invalid iterations type (not an integer)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', iterations='ten')  # type: ignore
        def invalid_iterations_type():   # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_TYPE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_iterations_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid iterations value."""
    clear_registered_cases()

    # Non-positive iterations value (zero)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', iterations=0)
        def non_positive_iterations_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_VALUE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_warmup_iterations_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid warmup_iterations type."""
    clear_registered_cases()

    # Invalid warmup_iterations type (not an integer)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', warmup_iterations='five')  # type: ignore
        def invalid_warmup_iterations_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_warmup_iterations_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid warmup_iterations value."""
    clear_registered_cases()

    # Negative warmup_iterations value (negative integer)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', warmup_iterations=-1)
        def negative_warmup_iterations_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE, (
        f"Wrong tag code: Expected {ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_use_field_for_n_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid use_field_for_n type."""
    clear_registered_cases()

    # use_field_for_n not a string
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'length': 'Length'},
                   kwargs_variations={'length': [10, 100, 1000]},
                   use_field_for_n=123)  # type: ignore
        def use_field_not_a_string():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_use_field_for_n_not_in_kwargs_variations() -> None:
    """Test that the @benchmark decorator raises expected errors for use_field_for_n not in kwargs_variations."""
    clear_registered_cases()

    # Invalid use_field_for_n value (not in kwargs_variations)
    with pytest.raises(SimpleBenchTypeError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   use_field_for_n='size',
                   kwargs_variations={'length': [10, 100, 1000]})
        def use_field_for_n_not_in_kwargs_variations():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_non_positive_use_field_for_n_values() -> None:
    """Test that the @benchmark decorator raises expected errors for non-positive use_field_for_n values."""
    # Invalid use_field_for_n values (non-positive integers in list)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'size': 'Size'},
                   kwargs_variations={'size': [0, -10, 100]},
                   use_field_for_n='size')
        def non_positive_use_field_for_n_values():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_n_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid n type."""
    # Invalid n type (not an integer)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'length': 'Length'},
                   kwargs_variations={'length': [10, 100, 1000]},
                   use_field_for_n='size',
                   n='ten')  # type: ignore
        def invalid_n_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_N_TYPE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_N_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_n_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid n value."""
    clear_registered_cases()
    # Non-positive n value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'length': 'Length'},
                   kwargs_variations={'length': [10, 100, 1000]},
                   use_field_for_n='size',
                   n=0)
        def non_positive_n_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_N_VALUE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_N_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_missing_kwargs_variations_with_use_field_for_n() -> None:
    """Test that the @benchmark decorator raises expected errors for missing kwargs_variations with use_field_for_n."""
    clear_registered_cases()

    # Missing kwargs_variations with use_field_for_n
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test',
                   title='Valid Title',
                   use_field_for_n='size')
        def missing_kwargs_variations():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS.name}, "
        f"Got {excinfo.value.tag_code}")


def test_decorator_invalid_group_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid group type."""
    clear_registered_cases()

    # Invalid group type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group=123, title='Valid Title')  # type: ignore
        def invalid_group_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_GROUP_TYPE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_GROUP_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_group_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid group value."""
    clear_registered_cases()

    # Empty group value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='    ', title='Valid Title', description='Valid Description')
        def empty_group_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_GROUP_VALUE, (
        f"Expected: {ErrorTag.BENCHMARK_DECORATOR_GROUP_VALUE.name}, "
        f"Got: {excinfo.value.tag_code.name}")


def test_decorator_invalid_min_time_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid min_time type."""
    clear_registered_cases()

    # Invalid min_time type (not a float)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', min_time='zero')  # type: ignore
        def invalid_min_time_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_TYPE, (
        f"Expecgted {ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_min_time_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid min_time value."""
    clear_registered_cases()

    # Invalid min_time value (non-positive)
    with pytest.raises(SimpleBenchValueError) as excinfo:
        @benchmark(group='test', title='Valid Title', min_time=0.0)
        def negative_min_time_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_VALUE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_max_time_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid max_time type."""
    clear_registered_cases()

    # Invalid max_time type (not a float)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', max_time='ten')  # type: ignore
        def invalid_max_time_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_TYPE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_max_time_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid max_time value."""
    clear_registered_cases()

    # Invalid max_time value (non-positive)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', max_time=-1.0)
        def negative_max_time_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_VALUE, (
        f"Expected {ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_VALUE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_kwargs_variations_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid kwargs_variations type"""
    clear_registered_cases()

    # Invalid kwargs_variations type (not a dict)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations='not_a_dict')  # type: ignore
        def invalid_kwargs_variations_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT, (
        f"Expected {ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_kwargs_variations_keys_types() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid kwargs_variations key types."""
    clear_registered_cases()

    # Invalid kwargs_variations keys/values
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations={123: [1, 2, 3]})  # type: ignore
        def invalid_kwargs_variations_keys_types():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE, (
        f"Expected {ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_kwargs_variations_key_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid kwargs_variations key value."""
    clear_registered_cases()

    # Invalid kwargs_variations key (blank string)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', kwargs_variations={' ': [1, 2, 3]})
        def empty_kwargs_variations_key_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER, (
        f"Expected {ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_kwargs_variations_values_types() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid kwargs_variations value types."""
    clear_registered_cases()

    # Invalid kwargs_variations values type (not a list)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations={'param': 'not_a_list'})  # type: ignore
        def invalid_kwargs_variations_values():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST, (
        f"Expected {ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_kwargs_variations_values_value() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid kwargs_variations value."""
    clear_registered_cases()

    # Invalid kwargs_variations values (empty list)
    with pytest.raises(SimpleBenchValueError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations={'param': []})
        def empty_kwargs_variations_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST, (
        f"Expected {ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_variation_cols_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid variation_cols type."""
    clear_registered_cases()

    # Invalid variation_cols type (not a dict)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', variation_cols='not_a_dict', kwargs_variations={})  # type: ignore
        def invalid_variation_cols_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_VARIATION_COLS_NOT_DICT, (
        f"Expected {ErrorTag.CASE_INVALID_VARIATION_COLS_NOT_DICT.name}, "
        f"Got {excinfo.value.tag_code.name}"
    )


def test_decorator_invalid_variation_cols_key_not_in_kwargs() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid variation_cols key values."""
    # Invalid variation_cols key values (not in kwargs_variations)
    with pytest.raises(SimpleBenchValueError) as excinfo:
        @benchmark(group='test', title='Valid Title',
                   variation_cols={123: 'Length', 'kwargs_variations': {}})  # type: ignore
        def invalid_variation_cols_keys():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS, (
        f"Expected {ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_variation_cols_value_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid variation_cols value types."""
    clear_registered_cases()

    # Invalid variation_cols values types (not strings)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title',
                   variation_cols={'length': 456},  # type: ignore
                   kwargs_variations={'length': [10, 100, 1000]})
        def invalid_variation_cols_values():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING, (
        f"Expected {ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_variation_cols_values() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid variation_cols values."""
    clear_registered_cases()

    # Invalid variation_cols values (blank string)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   kwargs_variations={'length': [10, 100, 1000]},
                   variation_cols={'length': '   '})
        def empty_variation_cols_value():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK, (
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_options_type() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid options type."""
    clear_registered_cases()

    # Invalid options type (not a list)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', options='not_a_list')  # type: ignore
        def invalid_options_type():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_OPTIONS_NOT_LIST, (
        f"Expected {ErrorTag.CASE_INVALID_OPTIONS_NOT_LIST.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_invalid_options_values() -> None:
    """Test that the @benchmark decorator raises expected errors for invalid options values."""
    clear_registered_cases()

    # Invalid options values (not a ReporterOption)
    with pytest.raises(SimpleBenchTypeError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', options=['invalid_option'])  # type: ignore
        def invalid_options_values():  # pragma: no cover
            pass
    assert excinfo.value.tag_code == ErrorTag.CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION, (
        f"Expected {ErrorTag.CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION.name}, "
        f"Got {excinfo.value.tag_code.name}")


def test_decorator_use_field_for_n_valid() -> None:
    """Test that the @benchmark decorator works correctly with valid use_field_for_n."""
    clear_registered_cases()

    sizes: list[int] = [10, 100, 1000]

    @benchmark(group='test',
               title='Valid use_field_for_n',
               variation_cols={'size': 'Size'},
               min_time=0.1,
               max_time=1.0,
               kwargs_variations={'size': sizes},
               use_field_for_n='size',
               n=50)
    def valid_use_field_for_n(size: int) -> int:
        return sum(range(size))

    cases = get_registered_cases()

    print(str(cases))
    assert len(cases) == 1, "Expected exactly one registered case."

    session = Session(cases=cases, verbosity=Verbosity.QUIET)
    session.run()
    # cases should have been run without errors and results collected

    test_case = cases[0]
    assert test_case.results is not None, "Expected results to be collected."
    assert len(test_case.results) == 3, "Expected three results for the three size variations."
    expected_n_values: set[int] = set(sizes)
    actual_n_values: set[int] = set(result.n for result in test_case.results)
    assert actual_n_values == expected_n_values, "The n values in results do not match the expected sizes."


if __name__ == "__main__":
    pytest.main()
