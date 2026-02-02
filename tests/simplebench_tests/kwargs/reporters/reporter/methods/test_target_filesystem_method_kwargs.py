"""Tests for TargetFilesystemMethodKWArgs."""
# ruff: noqa: F401
# These imports are necessary for the tests to run correctly as
# standalone tests because we need them in the global namespace.
# Also, ruff will remove "unused" imports without the noqa directive.
from pathlib import Path

import autopypath
import pytest
from rich.table import Table
from rich.text import Text
from simplebench_tests.kwargs import kwargs_class_matches_modeled_call
from simplebench_tests.kwargs.reporters.reporter.methods.target_filesystem_method_kwargs import (
    TargetFilesystemMethodKWArgs,
)

from simplebench.metadata import Metadata
from simplebench.reporters.reporter import Reporter, ReporterProtocol

_KWARGS_CLASS = TargetFilesystemMethodKWArgs
_MODELED_CLASS = Reporter
_MODELED_CALL = _MODELED_CLASS.target_filesystem


def test_kwargs_matches_signature() -> None:
    """Test that KWargs sublass __init__ signature matches the modeled call signature."""
    kwargs_class_matches_modeled_call(
        kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL, localns=locals(),globalns=globals()
    )


def test_can_instantiate() -> None:
    """Test that KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)


if __name__ == "__main__":
    pytest.main([__file__])
