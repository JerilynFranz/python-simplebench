"""simplebench.reporters.choices.Choices KWArgs package for SimpleBench tests."""
from __future__ import annotations

from simplebench.reporters.choices import Choices as _MODELED_CLASS

from ..kwargs import kwargs_class_matches_modeled_call
from .choices_conf_kwargs import ChoicesConfKWArgs as _KWARGS_CLASS

_MODELED_CALL = _MODELED_CLASS.__init__


def test_kwargs_matches_signature():
    """Test that KWargs sublass __init__ signature matches the modeled call signature."""
    kwargs_class_matches_modeled_call(kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL)


def test_can_instantiate():
    """Test that the KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)
