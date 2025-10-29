"""simplebench.cases.Case KWArgs package for SimpleBench tests."""
from __future__ import annotations

from tests.kwargs.helpers import kwargclass_matches_modeledclass

from simplebench.case import Case
from .case_kwargs import CaseKWArgs


def test_casekwargs_matches_case_signature():
    """Test that CaseKWArgs __init__ signature matches Case __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=CaseKWArgs, modeled_class=Case)
