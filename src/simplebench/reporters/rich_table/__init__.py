"""Rich Table Reporter for SimpleBench.

This package provides a Rich Table reporter for the simplebench.reporters package.
It offers functionality for generating rich table reports
from benchmark results.

Public API
----------
- :class:`simplebench.reporters.rich_table.config.RichTableConfig`: Configuration class for the Rich Table reporter.
- :class:`simplebench.reporters.rich_table.options.RichTableField`: Field enumeration for the Rich Table
    reporter options.
- :class:`simplebench.reporters.rich_table.reporter.RichTableReporter`: The Rich Table reporter class.
"""
# ruff: noqa: F401

from .config import RichTableConfig
from .reporter import RichTableReporter, _RichTableReporterErrorTag

__all__ = ["RichTableConfig", "RichTableReporter"]
