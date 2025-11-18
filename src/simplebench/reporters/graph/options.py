"""Base class for graph reporters in the :mod:`~simplebench.reporters` package."""
from simplebench.reporters.reporter.options import ReporterOptions


class GraphOptions(ReporterOptions):
    """Base class for :class:`~simplebench.reporters.graph.matplotlib.reporter.MatplotlibReporter`
    specific options.
    """
