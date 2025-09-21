"""Tests for the simplebench/decorators.py module."""
from __future__ import annotations

import pytest

from simplebench import clear_registered_cases, get_registered_cases, benchmark


class MockRunner:
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
    result = case.action(runner)
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
    result = case.action(runner)
    expected = sum(range(20))
    assert result == expected, "The action did not return the expected result."


if __name__ == "__main__":
    pytest.main()
