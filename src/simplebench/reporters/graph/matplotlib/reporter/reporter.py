"""Base class for MatPlotLib based graph reporters in the :mod:`~simplebench.reporters` package.

Intended to provide a common base for MatPlotLib based graph reporters,
such as line plots, bar charts, scatter plots, etc.
"""
from __future__ import annotations

from typing import TypeAlias

from ....reporter import Reporter
from .options import MatPlotLibOptions

Options: TypeAlias = MatPlotLibOptions


class MatPlotLibReporter(Reporter):
    """Base class for MatPlotLib based graph reporters in the :mod:`~simplebench.reporters`
    package.
    """
