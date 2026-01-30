from datetime import datetime, timedelta

import autopypath  # noqa: F401
import pytest
from testspec import PytestAction, TestAction

# Pytest native version
testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]

@pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
def test_timedistance_pytest(a: datetime, b: datetime, expected: timedelta) -> None:
    diff = a - b
    assert diff == expected


# PyTestAction Version

@pytest.mark.parametrize("testspec", [
    PytestAction('DATETIME_DIFF_001',
        name='Forward date difference with keyword args',
        kwargs={'a': datetime(2001, 12, 12), 'b': datetime(2001, 12, 11)}, expected=timedelta(1)),
    PytestAction('DATETIME_DIFF_002',
        name='Forward date difference with positional args',
        args=[datetime(2001, 12, 12), datetime(2001, 12, 11)], expected=timedelta(1)),
    PytestAction('DATETIME_DIFF_003',
        name='Backward date difference with keyword args',
        kwargs={'a': datetime(2001, 12, 11), 'b': datetime(2001, 12, 12)}, expected=timedelta(-1)),
    PytestAction('DATETIME_DIFF_004',
        name='Backward date difference with positional args',
        args=[datetime(2001, 12, 11), datetime(2001, 12, 12)], expected=timedelta(-1)),
])
def test_timedistance_pytestaction(testspec: TestAction) -> None:
    """Test the time distance between two datetime objects.

    action is set for all tests to compute the difference between a and b.
    It could be set in the PytestAction definition, but this is just to illustrate
    that action can be set at runtime en-masse for all tests.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    testspec.action = lambda a,b: a - b
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
