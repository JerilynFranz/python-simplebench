"""Base class for MatPlotLib based graph reporters in the reporters package.

By front-loading most of the common functionality into this base class, subclasses
can focus on the specific details of their graph types instead of boilerplate code.

It is not a complete implementation of a Reporter and must be subclassed to be used.
"""
from __future__ import annotations
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

# simplebench.reporters
from ...choice import Choice
from ...protocols import ReporterCallback
from ...reporter import Reporter

# simplebench.reporters.graph.matplotlib
from .options import MatPlotLibOptions

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session


class MatPlotLibReporter(Reporter):
    """Base class for MatPlotLib based graph reporters in the reporters package."""

    _HARDCODED_DEFAULT_OPTIONS = MatPlotLibOptions()
    """Built-in default ReporterOptions subclass instance for the reporter used if
    none is specified in a passed `Case`, `Choice`, or by `_DEFAULT_OPTIONS`. It
    forms the basis for the dynamic default options functionality provided by the
    `set_default_options()` and `get_default_options()` methods."""

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None
                   ) -> None:
        """Output the benchmark results as individual graphs for each case and section."""
        self.render_by_section(
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback)
