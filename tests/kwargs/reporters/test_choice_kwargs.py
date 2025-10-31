"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations

from tests.kwargs import kwargclass_matches_modeledclass

from simplebench.reporters.choice import Choice as _MODELED_CLASS
from .choice_kwargs import ChoiceKWArgs as _KWARGS_CLASS


def test_kwargs_matches_signature():
    """Test that KWargs sublass __init__ signature matches the modeled class __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=_KWARGS_CLASS, modeled_class=_MODELED_CLASS)


def test_can_instantiate():
    """Test that the KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)
