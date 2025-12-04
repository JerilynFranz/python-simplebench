"""Simple benchmarking framework."""
from simplebench._meta import __author__, __copyright__, __project__, __release__, __version__  # noqa: F401
from simplebench.case import Case
from simplebench.cli import main
from simplebench.decorators import benchmark
from simplebench.enums import Verbosity
from simplebench.reporters.csv.reporter.options import CSVOptions
from simplebench.reporters.json.reporter.options import JSONOptions
from simplebench.reporters.reporter_manager.decorators import register_reporter
from simplebench.reporters.rich_table.reporter.options import RichTableOptions
from simplebench.results import Results
from simplebench.session import Session

__all__ = [
    "main",
    "benchmark",
    "register_reporter",
    "Case",
    "Results",
    "CSVOptions",
    "JSONOptions",
    "RichTableOptions",
    "Session",
    "Verbosity",
]

# Optional imports for graph reporting functionality
try:
    from simplebench.reporters.graph.enums import ImageType  # noqa: F401
    from simplebench.reporters.graph.matplotlib import Style, Theme  # noqa: F401
    from simplebench.reporters.graph.scatterplot.reporter import ScatterPlotOptions  # noqa: F401

    __all__.extend(["ImageType", "Style", "Theme", "ScatterPlotOptions"])
except ImportError:
    pass

# Optional imports for pytest plugin functionality
try:
    from simplebench._pytest import BenchmarkRegistrar  # noqa: F401

    __all__.append("BenchmarkRegistrar")
except ImportError:
    pass
