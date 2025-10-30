"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations

from tests.kwargs.helpers import kwargclass_matches_modeledclass

from simplebench.reporters.reporter import Reporter
from .reporter_kwargs import ReporterKWArgs


def test_reporterkwargs_matches_reporter_signature():
    """Test that ReporterKWArgs __init__ signature matches Reporter __init__ signature."""
    kwargclass_matches_modeledclass(kwargs_class=ReporterKWArgs, modeled_class=Reporter)
