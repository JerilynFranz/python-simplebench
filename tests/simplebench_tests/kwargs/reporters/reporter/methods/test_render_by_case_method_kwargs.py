"""Tests for tests.kwargs.reporters.reporter_kwargs.ReporterKWArgs."""
# ruff: noqa: F401
# These imports are necessary for the tests to run correctly as
# standalone tests because we need them in the global namespace.
# Also, ruff will remove "unused" imports without the noqa directive.
from argparse import Namespace
from pathlib import Path

import autopypath
import pytest
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue, kwargs_class_matches_modeled_call
from simplebench_tests.kwargs.reporters.reporter.methods.render_by_case_method_kwargs import RenderByCaseMethodKWArgs

from simplebench.case import Case
from simplebench.metadata import Metadata
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter import Reporter
from simplebench.session import Session

_KWARGS_CLASS = RenderByCaseMethodKWArgs
_MODELED_CLASS = Reporter
_MODELED_CALL = _MODELED_CLASS.render_by_case


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
