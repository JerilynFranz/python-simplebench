"""ErrorTags for the ``graph.scatterplot.reporter`` module in the reporters package."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ScatterPlotReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the :class:`~.ScatterPlotReporter` class."""

    # render()
    RENDER_INVALID_CASE = auto()
    """The ``case`` argument passed to the :meth:`~.ScatterPlotReporter.render` method is not
    a :class:`~simplebench.case.Case` instance.
    """
    RENDER_INVALID_SECTION = auto()
    """The ``metric`` argument passed to the :meth:`~.ScatterPlotReporter.render` method is
    not a :class:`~simplebench.metric.Metric` enum member.
    """
    RENDER_INVALID_OPTIONS = auto()
    """The ``options`` argument passed to the :meth:`~.ScatterPlotReporter.render` method is
    not a :class:`~.ScatterPlotOptions` instance.
    """
