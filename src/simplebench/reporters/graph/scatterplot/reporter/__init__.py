"""ScatterPlot graph.scatterplot.reporter module in the reporters package.

Purpose is to provide a scatter plot reporter for the simplebench.reporters package.

This package provides functionality for generating scatter plot graphs
using Matplotlib as the underlying graphing library.

Public API
----------
- ScatterPlotConfig: Configuration class for the ScatterPlot reporter.
- ScatterPlotOptions: Options class for the ScatterPlot reporter.
- ScatterPlotReporter: The ScatterPlot reporter class.
"""
from .config import ScatterPlotConfig
from .options import ScatterPlotOptions
from .reporter import ScatterPlotReporter

__all__ = [
    "ScatterPlotConfig",
    "ScatterPlotOptions",
    "ScatterPlotReporter",
]
