"""ErrorTags for the ``graph.scatterplot.reporter`` module in the reporters package."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class ScatterPlotReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the :class:`~.ScatterPlotReporter` class."""
    # render()
    RENDER_INVALID_CASE = "SCATTERPLOT_REPORTER_RENDER_INVALID_CASE"
    """The ``case`` argument passed to the :meth:`~.ScatterPlotReporter.render` method is not
    a :class:`~simplebench.case.Case` instance.
    """
    RENDER_INVALID_SECTION = "SCATTERPLOT_REPORTER_RENDER_INVALID_SECTION"
    """The ``section`` argument passed to the :meth:`~.ScatterPlotReporter.render` method is
    not a :class:`~simplebench.enums.Section` enum member.
    """
    RENDER_INVALID_OPTIONS = "SCATTERPLOT_REPORTER_RENDER_INVALID_OPTIONS"
    """The ``options`` argument passed to the :meth:`~.ScatterPlotReporter.render` method is
    not a :class:`~.ScatterPlotOptions` instance.
    """
