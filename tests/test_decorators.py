"""Tests for the simplebench/decorators.py module."""
from __future__ import annotations

import pytest

from simplebench.decorators import clear_registered_cases, get_registered_cases, benchmark
from simplebench.enums import Verbosity
from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.session import Session


def mock_action(*arg, **kwargs) -> None:  # pylint: disable=unused-argument
    """A mock action that does nothing."""
    return None


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
        sum(range(100))

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


def test_decorator_invalid_parameters() -> None:
    """Test that the @benchmark decorator raises errors for invalid parameters."""

    clear_registered_cases()

    # Invalid title type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title=123)  # type: ignore
        def invalid_title_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_TITLE_TYPE

    # Empty title value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='   ')
        def empty_title_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_TITLE_VALUE

    # Invalid description type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', description=456)  # type: ignore
        def invalid_description_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_TYPE

    # Empty description value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', description='   ')
        def empty_description_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_VALUE

    # Invalid iterations type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', iterations='ten')  # type: ignore
        def invalid_iterations_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_TYPE

    # Non-positive iterations value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', iterations=0)
        def non_positive_iterations_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_VALUE

    # Invalid warmup_iterations type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', warmup_iterations='five')  # type: ignore
        def invalid_warmup_iterations_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE

    # Negative warmup_iterations value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', warmup_iterations=-1)
        def negative_warmup_iterations_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE

    # use_field_for_n not a string
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'length': 'Length'},
                   kwargs_variations={'length': [10, 100, 1000]},
                   use_field_for_n=123)  # type: ignore
        def use_field_not_a_string():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE

    # Invalid n type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'length': 'Length'},
                   kwargs_variations={'length': [10, 100, 1000]},
                   use_field_for_n='size',
                   n='ten')  # type: ignore
        def invalid_n_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_N_TYPE

    # Non-positive n value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'length': 'Length'},
                   kwargs_variations={'length': [10, 100, 1000]},
                   use_field_for_n='size',
                   n=0)
        def non_positive_n_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_N_VALUE

    # Missing kwargs_variations with use_field_for_n
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test',
                   title='Valid Title',
                   use_field_for_n='size')
        def missing_kwargs_variations():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS, (
        f"Got {excinfo.value.tag_code}")

    # Invalid group type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group=123, title='Valid Title')  # type: ignore
        def invalid_group_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_GROUP_TYPE, f"Got {excinfo.value.tag_code}"

    # Empty group value
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='    ', title='Valid Title', description='Valid Description')
        def empty_group_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_GROUP_VALUE, f"Got {excinfo.value.tag_code}"

    # Invalid min_time type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', min_time='zero')  # type: ignore
        def invalid_min_time_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_TYPE, f"Got {excinfo.value.tag_code}"

    # Invalid max_time type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', max_time='ten')  # type: ignore
        def invalid_max_time_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_TYPE, f"Got {excinfo.value.tag_code}"

    # Invalid kwargs_variations type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations='not_a_dict')  # type: ignore
        def invalid_kwargs_variations_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_TYPE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid kwargs_variations keys/values
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations={123: [1, 2, 3]})  # type: ignore
        def invalid_kwargs_variations_keys():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_KEY_TYPE

    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', kwargs_variations={'param': 'not_a_list'})  # type: ignore
        def invalid_kwargs_variations_values():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_TYPE

    # Invalid variation_cols type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', variation_cols='not_a_dict', kwargs_variations={})  # type: ignore
        def invalid_variation_cols_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_TYPE

    # Invalid variation_cols keys/values
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title',
                   variation_cols={123: 'Length', 'kwargs_variations': {}})  # type: ignore
        def invalid_variation_cols_keys():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_KEY_TYPE

    # Missing kwargs_variations with variation_cols
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title - Missing kwargs_variations', variation_cols={'length': 'Length'})
        def missing_kwargs_variations_with_variation_cols():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_KWARGS_VARIATIONS_MISMATCH, (
        f"Got {excinfo.value.tag_code}")

    # Invalid variation_cols values types
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', variation_cols={'length': 456})  # type: ignore
        def invalid_variation_cols_values():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_TYPE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid variation_cols values (empty string)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', variation_cols={'length': '   '})
        def empty_variation_cols_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_VALUE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid variation_cols key (blank string)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', variation_cols={'': 'Length'})
        def empty_variation_cols_key():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_KEY_VALUE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid variation_cols type (list instead of dict)
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', variation_cols=['not', 'a', 'dict'])  # type: ignore
        def variation_cols_not_dict():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_TYPE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid use_field_for_n type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', use_field_for_n=456)  # type: ignore
        def invalid_use_field_for_n_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE, f"Got {excinfo.value.tag_code}"

    # Invalid use_field_for_n value (empty string)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', use_field_for_n='   ')
        def empty_use_field_for_n_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_VALUE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid use_field_for_n value (not in kwargs_variations)
    with pytest.raises(SimpleBenchTypeError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   use_field_for_n='size',
                   kwargs_variations={'length': [10, 100, 1000]})
        def use_field_for_n_not_in_kwargs_variations():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS, (
        f"Got {excinfo.value.tag_code}")

    # Invalid options type
    with pytest.raises(SimpleBenchTypeError) as excinfo:
        @benchmark(group='test', title='Valid Title', options='not_a_dict')  # type: ignore
        def invalid_options_type():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_OPTIONS_TYPE, f"Got {excinfo.value.tag_code}"

    # Invalid kwargs_variations values (empty list)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test', title='Valid Title', kwargs_variations={'param': []})
        def empty_kwargs_variations_value():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_VALUE, (
        f"Got {excinfo.value.tag_code}")

    # Invalid use_field_for_n values (non-positive integers in list)
    with pytest.raises(SimpleBenchValueError) as excinfo:  # type: ignore[assignment]
        @benchmark(group='test',
                   title='Valid Title',
                   variation_cols={'size': 'Size'},
                   kwargs_variations={'size': [0, -10, 100]},
                   use_field_for_n='size')
        def non_positive_use_field_for_n_values():
            pass
    assert excinfo.value.tag_code == ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE, (
        f"Got {excinfo.value.tag_code}")


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
