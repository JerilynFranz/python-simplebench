""""Protocols for reporters stuff."""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from rich.table import Table
from rich.text import Text

# Disconnects any possible circular imports
if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.enums import Section
    from simplebench.reporters.reporter.options import ReporterOptions


@runtime_checkable
class ReportRenderer(Protocol):
    """A protocol for render methods in Reporters.

    Defines a method signature for rendering benchmark results for a given
    :class:`~simplebench.case.Case` and :class:`~simplebench.enums.Section`.

    The signature must match the following:

    .. code-block:: python

        def method_name(self, *, case: Case, section: Section, options: ReporterOptions) -> str | bytes | Text | Table:

    Subsets of ``str | bytes | Text | Table`` for the return type are allowed for specific
    reporters.
    """
    def __call__(self, *, case: Case, section: Section, options: ReporterOptions) -> str | bytes | Text | Table:
        """Renders the benchmark results for one section and returns the result.

        The result can be a :class:`str`, :class:`bytes`, :class:`~rich.text.Text`, or
        :class:`~rich.table.Table`.

        While required in the protocol, the value of the ``section`` argument should be
        ignored by reporters that do not render reports by section. It will be set to
        :attr:`~simplebench.enums.Section.NULL` by the
        :meth:`~simplebench.reporters.reporter.Reporter.render_by_case` method.

        :param case: The :class:`~simplebench.case.Case` instance representing the
            benchmarked code.
        :param section: The :class:`~simplebench.enums.Section` of the report to render
            (ignore value if not applicable to reporter).
        :param options: The reporter-specific options.
        :return: The rendered report data as a :class:`str`, :class:`bytes`,
            :class:`~rich.text.Text`, or :class:`~rich.table.Table`.
        """
        ...  # pylint: disable=unnecessary-ellipsis
