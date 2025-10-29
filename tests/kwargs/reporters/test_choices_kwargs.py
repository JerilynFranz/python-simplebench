"""simplebench.reporters.choices.Choices KWArgs package for SimpleBench tests."""
from __future__ import annotations

from tests.kwargs.helpers import kwargclass_matches_modeledclass

from simplebench.reporters.choices import Choices
from .choices_kwargs import ChoicesKWArgs


def test_choiceskwargs_matches_choices_signature():
    """Test that ChoicesKWArgs __init__ signature matches Choices __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=ChoicesKWArgs, modeled_class=Choices)
