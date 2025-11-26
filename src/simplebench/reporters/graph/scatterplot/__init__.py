"""ScatterPlot graph.scatterplot module in the reporters package.

Purpose is to provide a scatter plot reporter for the simplebench.reporters package.

This package provides functionality for generating scatter plot graphs
using Matplotlib as the underlying graphing library.

Public API
----------
- :class:`~.ScatterPlotConfig`: Configuration class for the ScatterPlot reporter.
- :class:`~.ScatterPlotOptions`: Options class for the ScatterPlot reporter.
- :class:`~.ScatterPlotReporter`: The ScatterPlot reporter class.
"""
from .reporter import ScatterPlotConfig, ScatterPlotOptions, ScatterPlotReporter

__all__ = [
    "ScatterPlotReporter",
    "ScatterPlotOptions",
    "ScatterPlotConfig",
]
