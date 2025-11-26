"""Matplotlib graph reporter module in the reporters package.

This module provides the base classes and options for creating
graph reporters using Matplotlib within the simplebench framework.

It includes the `MatPlotLibReporter` class, which serves as a base
for all Matplotlib-based graph reporters, and the `MatPlotLibOptions`
class for configuring reporter-specific options.

Public API
----------
- MatPlotLibOptions: Configuration options for MatPlotLib reporters.
- MatPlotLibReporter: Base class for MatPlotLib based graph reporters.
"""
from .options import MatPlotLibOptions
from .reporter import MatPlotLibReporter

__all__ = [
    "MatPlotLibOptions",
    "MatPlotLibReporter",
]
