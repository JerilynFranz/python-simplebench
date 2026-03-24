"""Tests for ValueBlockKWArgs package for SimpleBench tests."""
import sys

import autopypath  # noqa: F401 # ensure sys.path setup when running tests directly
import pytest

from simplebench.report.versions.v1 import MetricType
from simplebench_tests.kwargs import kwargs_class_matches_modeled_call
from simplebench_tests.kwargs.report.v1 import MetricTypeKWArgs

_KWARGS_CLASS = MetricTypeKWArgs
_MODELED_CLASS = MetricType
_MODELED_CALL = _MODELED_CLASS.__init__


def test_kwargs_matches_signature() -> None:
    """Test that KWargs sublass __init__ signature matches the modeled class __init__ signature."""
    kwargs_class_matches_modeled_call(kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL)


def test_can_instantiate() -> None:
    """Test that the KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)


if __name__ == "__main__":
    sys.modules.pop("typeguard")
    pytest.main([__file__])
