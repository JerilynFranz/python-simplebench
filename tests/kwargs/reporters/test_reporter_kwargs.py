"""Tests for tests.kwargs.reporters.reporter_kwargs.ReporterKWArgs."""
from tests.kwargs import kwargclass_matches_modeledclass

from simplebench.reporters.reporter import Reporter as _MODELED_CLASS
from .reporter_kwargs import ReporterKWArgs as _KWARGS_CLASS


def test_kwargs_matches_signature():
    """Test that KWargs sublass __init__ signature matches the modeled class __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=_KWARGS_CLASS, modeled_class=_MODELED_CLASS)


def test_can_instantiate():
    """Test that KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)
