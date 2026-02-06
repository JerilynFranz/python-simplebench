"""Test for simplebench.types.values module."""
# ruff: noqa: E501
#import importlib.util  # Import the utility
#import sys
#from pathlib import Path

import autopypath  # noqa: F401 # autopypath adjusts sys.path on import when run as script
import pytest

from testspec import Assert, TestSpec, PytestAction

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import Values


@pytest.mark.parametrize(
    'testspec', [
        PytestAction('VALUES_001',
            name='Create Values instance from list of ints and floats',
            action=Values, args=[[1, 2.5, 3]],
            assertion=Assert.ISINSTANCE,
            expected=Values),
        PytestAction('VALUES_002',
            name='Create Values instance from empty list',
            action=Values, args=[[]],
            expected=Values()),
        PytestAction('VALUES_003',
            name='Validate Values contents are floats',
            action=Values, args=[[1, 2.5, 3]],
            validate_result=lambda result: all(isinstance(v, float) for v in result)),
        PytestAction('VALUES_004',
            name='Create Values instance with non-iterable (int) raises SimpleBenchTypeError',
            action=Values, args=[1],
            exception=SimpleBenchTypeError),
        PytestAction('VALUES_005',
            name='Create Values instance with non-numeric types raises TypeError',
            action=Values, args=[['a', None, 3]],
            exception=SimpleBenchTypeError),
        PytestAction('VALUES_006',
            name='Create Values instance is equivalent to tuple of floats',
            action=Values, args=[[1, 2.0, 3, 4.5]],
            expected=(1.0, 2.0, 3.0, 4.5)),
    ],
)
def test_values(testspec: TestSpec) -> None:
    """Test the Values class.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize(
    'testspec', [
        PytestAction('HASH_001',
            name='Values instance is immutable and hashable',
            action=hash,
            args=[Values([1, 2.5, 3])],
            assertion=Assert.ISINSTANCE,
            expected=int),
    ],
)
def test_hash(testspec: TestSpec) -> None:
    testspec.run()


if __name__ == '__main__':
    pytest.main([__file__])
