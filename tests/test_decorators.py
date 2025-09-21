"""Tests for the simplebench/decorators.py module."""
from __future__ import annotations

import pytest

from simplebench import clear_registered_cases, get_registered_cases, benchmark


def test_benchmark_decorator_registers_case():
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


if __name__ == "__main__":
    pytest.main()
