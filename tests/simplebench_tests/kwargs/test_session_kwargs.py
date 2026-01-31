"""simplebench.session KWArgs package for SimpleBench tests."""
import sys

import autopypath  # noqa: F401  # adjusts sys.path for imports for running tests as script
import pytest
from simplebench_tests.kwargs.kwargs import kwargs_class_matches_modeled_call
from simplebench_tests.kwargs.session_kwargs import SessionKWArgs as _KWARGS_CLASS

from simplebench.session import Session as _MODELED_CLASS

_MODELED_CALL = _MODELED_CLASS.__init__


def test_kwargs_matches_signature() -> None:
    """Test that KWargs sublass __init__ signature matches the modeled class __init__ signature."""
    kwargs_class_matches_modeled_call(kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL)


def test_can_instantiate() -> None:
    """Test that the KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)


if __name__ == '__main__':
    sys.modules.pop('typeguard')
    pytest.main([__file__])
