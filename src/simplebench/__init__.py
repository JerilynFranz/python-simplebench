"""Simple benchmarking framework."""
from simplebench.cli import main
from simplebench.decorators import benchmark
from simplebench.case import Case
from simplebench.enums import Verbosity
from simplebench.reporters.csv.reporter.options import CSVOptions
from simplebench.reporters.graph.enums import ImageType
from simplebench.reporters.graph.matplotlib import Style, Theme
from simplebench.reporters.json.reporter.options import JSONOptions
from simplebench.reporters.rich_table.reporter.options import RichTableOptions
from simplebench.reporters.graph.scatterplot import ScatterPlotOptions
from simplebench.results import Results
from simplebench.session import Session
from simplebench.reporters.reporter_manager.decorators import register_reporter


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
