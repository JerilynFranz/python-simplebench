"""simplebench.reporters.choices.Choices KWArgs package for SimpleBench tests."""
import sys

import autopypath  # noqa: F401
import pytest
from simplebench_tests.kwargs import kwargs_class_matches_modeled_call
from simplebench_tests.kwargs.reporters.choices_kwargs import ChoicesKWArgs

from simplebench.reporters.choice import Choice  # noqa: F401
from simplebench.reporters.choices import Choices
from simplebench.simplebench_types import ElementCollection  # noqa: F401

_MODELED_CALL = Choices.__init__
_KWARGS_CLASS = ChoicesKWArgs

def test_kwargs_matches_signature() -> None:
    """Test that KWargs sublass __init__ signature matches the modeled call signature."""
    kwargs_class_matches_modeled_call(
        kwargs_class=_KWARGS_CLASS, modeled_call=_MODELED_CALL,
        globalns=globals(), localns=locals()
    )


def test_can_instantiate() -> None:
    """Test that the KWArgs subclass can be instantiated."""
    kwargs_instance = _KWARGS_CLASS()
    assert isinstance(kwargs_instance, _KWARGS_CLASS)


if __name__ == "__main__":
    sys.modules.pop("typeguard")
    pytest.main([__file__])
