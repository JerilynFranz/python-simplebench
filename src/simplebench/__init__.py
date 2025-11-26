"""Simple benchmarking framework."""
from simplebench._meta import __author__, __copyright__, __project__, __release__, __version__  # noqa: F401
from simplebench.case import Case
from simplebench.cli import main
from simplebench.decorators import benchmark
from simplebench.enums import Verbosity
from simplebench.reporters.csv.reporter.options import CSVOptions
from simplebench.reporters.graph.enums import ImageType
from simplebench.reporters.graph.matplotlib import Style, Theme
from simplebench.reporters.graph.scatterplot.reporter import ScatterPlotOptions
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
    "ImageType",
    "Style",
    "Theme",
    "JSONOptions",
    "RichTableOptions",
    "ScatterPlotOptions",
    "Session",
    "Results",
    "Verbosity",
]
"""Simple benchmarking framework public API."""
