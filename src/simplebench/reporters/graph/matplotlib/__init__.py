"""Matplotlib graph reporter module in the reporters package.

This package provides common functionality for Matplotlib-based graph reporters.
"""
from simplebench.reporters.graph.matplotlib.constants import SUPPORTED_IMAGE_TYPES
from simplebench.reporters.graph.matplotlib.enums import Style
from simplebench.reporters.graph.matplotlib.exceptions import _MatPlotLibReporterErrorTag
from simplebench.reporters.graph.matplotlib.options import MatPlotLibOptions, _MatPlotLibOptionsErrorTag
from simplebench.reporters.graph.matplotlib.reporter import MatPlotLibReporter
from simplebench.reporters.graph.matplotlib.theme import Theme

__all__ = [
    "SUPPORTED_IMAGE_TYPES",
    "MatPlotLibOptions",
    "_MatPlotLibOptionsErrorTag",
    "MatPlotLibReporter",
    "_MatPlotLibReporterErrorTag",
    "Style",
    "Theme",
]
"""Matplotlib graph reporter package in the reporters package."""
