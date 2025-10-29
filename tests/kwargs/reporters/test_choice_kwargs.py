"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations

from tests.kwargs.helpers import kwargclass_matches_modeledclass

from simplebench.reporters.choice import Choice
from .choice_kwargs import ChoiceKWArgs


def test_choicekwargs_matches_choice_signature():
    """Test that ChoiceKWArgs __init__ signature matches Choice __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=ChoiceKWArgs, modeled_class=Choice)
