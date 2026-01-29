"""CSV reporter package for simplebench.

Purpose is to provide a CSV reporter for the simplebench.reporters package.
This package provides functionality for generating CSV reports
from benchmark results.

Public API
----------
- :class:`simplebench.reporters.csv.reporter.CSVReporter`: The CSV reporter class.
- :class:`simplebench.reporters.csv.config.CSVConfig`: Configuration class for the CSV reporter.

"""
# ruff: noqa: F401

from .config import CSVConfig
from .reporter import CSVReporter, _CSVReporterErrorTag

__all__ = ['CSVReporter', 'CSVConfig']
