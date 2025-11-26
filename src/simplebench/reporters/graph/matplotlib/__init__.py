"""Matplotlib graph reporter module.

This module provides common base functionality for Matplotlib-based graph reporters.
The :class:`~.MatPlotLibOptions` and :class:`~.MatPlotLibReporter` classes
are not intended to be used directly, but rather to be subclassed by specific
reporters for line plots, bar charts, scatter plots, etc.

Public API
----------
- :class:`~.MatPlotLibOptions`: Options specific to Matplotlib based graph reporters.
- :class:`~.MatPlotLibReporter`: Base class for Matplotlib based graph reporters.
- :class:`~.Style`: Enumeration of available styles.
- :class:`~.Theme`: Theme management for Matplotlib based graph reporters.
- `SUPPORTED_IMAGE_TYPES`: Frozen set of supported image output types.
"""
from .constants import SUPPORTED_IMAGE_TYPES
from .enums import Style
from .reporter import MatPlotLibOptions, MatPlotLibReporter
from .theme import Theme

__all__ = [
    "MatPlotLibOptions",
    "MatPlotLibReporter",
    "Style",
    "SUPPORTED_IMAGE_TYPES",
    "Theme",
]
