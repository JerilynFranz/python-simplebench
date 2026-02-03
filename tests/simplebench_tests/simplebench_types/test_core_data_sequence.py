"""Tests for CoreDataSequence type."""
# ruff: noqa: F401
import autopypath
import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench.simplebench_types import CoreDataSequence, ImmutableCoreDataTypes


@pytest.mark.parametrize('testspec', [
    PytestAction('INIT_001',
        name='Initialize CoreDataSequence with empty input',
        action=CoreDataSequence,
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_002',
        name='Initialize CoreDataSequence with list of integers',
        action=CoreDataSequence,
        args=[[1, 2, 3, 4, 5]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_003',
        name='Initialize CoreDataSequence with tuple of strings',
        action=CoreDataSequence,
        args=[('a', 'b', 'c')],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_004',
        name='Initialize CoreDataSequence with mixed primitive types',
        action=CoreDataSequence,
        args=[[1, 'two', 3.0, True, None]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
