"""Tests for TargetCallbackMethodKWArgs."""
# ruff: noqa: F401
# These imports are necessary for the tests to run correctly as
# standalone tests because we need them in the global namespace.
# Also, ruff will remove "unused" imports without the noqa directive.
import autopypath
import pytest
from rich.table import Table
from rich.text import Text
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue, kwargs_class_matches_modeled_call
from simplebench_tests.kwargs.reporters.reporter.methods.target_callback_method_kwargs import TargetCallbackMethodKWArgs
from testspec import Assert, TestAction, TestSpec, idspec

from simplebench.case import Case
from simplebench.enums import Format
from simplebench.metrics import Metric
from simplebench.reporters.protocols.reporter_callback import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterProtocol
from simplebench.reporters.reporter import Reporter as _MODELED_CLASS

_MODELED_CALL = _MODELED_CLASS.target_callback
_KWARGS_CLASS = TargetCallbackMethodKWArgs

def test_kwargs_matches_signature() -> None:
    """Test that KWargs sublass __init__ signature matches the modeled call signature."""
    kwargs_class_matches_modeled_call(
        kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL, globalns=globals()
    )


def test_can_instantiate() -> None:
    """Test that KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)


if __name__ == "__main__":
    pytest.main([__file__])
