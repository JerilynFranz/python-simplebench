"""Tests for Swap Memory report."""

import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench.report.versions import v1 as report
from simplebench_tests.factories.report import v1 as report_factories


@pytest.mark.parametrize("testspec", [
    PytestAction('INIT_001',
        name="Test good all argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs_factory(),
        assertion=Assert.ISINSTANCE,
        expected=report.SwapMemoryObject
    ),
    PytestAction('INIT_002',
        name="Test missing total argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs_factory() - {"total"},
        exception=TypeError),
])
def test_init(testspec: TestSpec) -> None:
    """Test the initialization of SwapMemoryObject."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
