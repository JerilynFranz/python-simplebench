""""Protocols for reporters stuff."""
from __future__ import annotations
from typing import Protocol, TYPE_CHECKING, runtime_checkable

from rich.table import Table
from rich.text import Text

# Disconnects any possible circular imports
if TYPE_CHECKING:
    from simplebench.enums import Section
    from simplebench.case import Case
    from simplebench.reporters.reporter.options import ReporterOptions


@runtime_checkable
class ReportRenderer(Protocol):
    """A protocol for render methods in Reporters.

    Defines a method signature for rendering benchmark results for a given Case and Section.

    The signature must match the following:

    `def method_name(self, *, case: Case, section: Section, options: ReporterOptions) -> str | bytes | Text | Table:`

    Subsets of 'str | bytes | Text | Table' for the return type are allowed for specific reporters.
    """
    def __call__(self, *, case: Case, section: Section, options: ReporterOptions) -> str | bytes | Text | Table:
        """Renders the benchmark results for one section and returns the result as a str, bytes,
        rich.Text, or rich.Table.

        While required in the protocol, the value of the section argument should be ignored by reporters that do not
        render reports by section. It will be set to Section.NULL by the render_by_case() method.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The Section of the report to render (ignore value if not applicable to reporter).
            options (ReporterOptions): The reporter-specific options.

        Returns:
            str | bytes | Text | Table: The rendered report data as a str, bytes, rich.Text, or rich.Table.
        """
        ...  # pylint: disable=unnecessary-ellipsis
