"""ReporerOptions subclass for CSV reporter specific options.

This module defines the :class:`~.CSVOptions` class, which is a subclass of
:class:`~simplebench.reporters.reporter.options.ReporterOptions` and is used
to hold options specific to the CSV reporter.
"""
# simplebench.reporters.reporter
from simplebench.reporters.reporter.options import ReporterOptions


class CSVOptions(ReporterOptions):
    """Class for holding CSV reporter specific options.

    This class provides additional configuration options specific to the CSV reporter.
    It is accessed via the :attr:`~simplebench.reporters.choice.Choice.options`
    attribute of a :class:`~simplebench.reporters.choice.Choice` instance or a
    :class:`~simplebench.case.Case` instance.

    It is currently only a stub for future expansion.
    """
