"""Tests for tests.kwargs.reporters.reporter_kwargs.ReporterKWArgs."""
from simplebench.reporters.reporter import Reporter as _MODELED_CLASS

from ....kwargs import kwargs_class_matches_modeled_call
from .dispatch_to_targets_method_kwargs import DispatchToTargetsMethodKWArgs as _KWARGS_CLASS

_MODELED_CALL = _MODELED_CLASS.dispatch_to_targets


def test_kwargs_matches_signature():
    """Test that KWargs subclass __init__ signature matches the modeled call signature."""
    kwargs_class_matches_modeled_call(kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL)


def test_can_instantiate():
    """Test that KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)
