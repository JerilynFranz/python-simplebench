"""Validation tests for TypedDict mimic functions."""

from typing import TypedDict

import pytest
from testspec import PytestAction, TestSpec

from simplebench._log import _log
from simplebench.validators import is_typed_dict_mimic

_log.setLevel('DEBUG')

class SimpleTypedDict(TypedDict):
    name: str
    value: int


@pytest.mark.parametrize('testspec', [
    PytestAction('MIMIC_001',
        name='MIMIC_001: dict conforming to SimpleTypedDict is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic, args=[{'name': 'test', 'value': 42}, SimpleTypedDict],
        expected=True
    ),
    PytestAction('MIMIC_002',
        name='MIMIC_002: dict NOT conforming to SimpleTypedDict is NOT recognized as a TypedDict mimic',
        action=is_typed_dict_mimic, args=[{'name': 2, 'value': 42}, SimpleTypedDict],
        expected=False
    ),
])
def test_typed_dict_mimic(testspec: TestSpec) -> None:
    """Test that a valid TypedDict mimic is recognized as such."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
