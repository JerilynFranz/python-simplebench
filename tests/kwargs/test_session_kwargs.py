"""simplebench.session KWArgs package for SimpleBench tests."""
from __future__ import annotations

from tests.kwargs.helpers import kwargclass_matches_modeledclass

from simplebench.session import Session
from .session_kwargs import SessionKWArgs


def test_sessionkwargs_matches_session_signature():
    """Test that SessionKWArgs __init__ signature matches Session __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=SessionKWArgs, modeled_class=Session)
