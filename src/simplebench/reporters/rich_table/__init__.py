"""Rich Table Reporter for SimpleBench.

This package provides a Rich Table reporter for the simplebench.reporters package.
It offers functionality for generating rich table reports
from benchmark results.

Public API
----------
- :class:`~.RichTableConfig`: Configuration class for the Rich Table reporter.
- :class:`~.RichTableOptions`: Options class for the Rich Table reporter.
- :class:`~.RichTableReporter`: The Rich Table reporter class.
"""
from .reporter import RichTableConfig, RichTableOptions, RichTableReporter

__all__ = [
    'RichTableConfig',
    'RichTableOptions',
    'RichTableReporter',
]
