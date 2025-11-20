"""Rich Table Reporter for SimpleBench."""
from simplebench.reporters.rich_table.reporter.exceptions import _RichTableReporterErrorTag
from simplebench.reporters.rich_table.reporter.options import RichTableOptions
from simplebench.reporters.rich_table.reporter.options.exceptions import _RichTableOptionsErrorTag
from simplebench.reporters.rich_table.reporter.reporter import RichTableReporter

__all__ = [
    'RichTableReporter',
    '_RichTableReporterErrorTag',
    'RichTableOptions',
    '_RichTableOptionsErrorTag',
]
"""'*' imports for Rich Table Reporter."""
