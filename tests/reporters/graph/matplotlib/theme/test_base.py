"""Tests for the Matplotlib Theme base class."""
import pytest

from tests.testspec import TestSpec, TestAction, idspec, Assert

from simplebench.reporters.graph.matplotlib.theme.base import Theme


@pytest.mark.parametrize("testspec", [
    idspec('INIT_001', TestAction(
        name="no_params",
        action=Theme,
        assertion=Assert.ISINSTANCE,
        expected=Theme
    )),
])
def test_init(testspec: TestSpec):
    """Test Theme class initialization."""
    testspec.run()
