"""CSV reporter package for simplebench.

Purpose is to provide a CSV reporter for the simplebench.reporters package.
This package provides functionality for generating CSV reports
from benchmark results.

Public API
----------
- :class:`~.CSVOptions`: Options class for the CSV reporter.
- :class:`~.CSVReporter`: The CSV reporter class.
- :class:`~.CSVConfig`: Configuration class for the CSV reporter.

"""
from .reporter import CSVConfig, CSVOptions, CSVReporter

__all__ = [
    'CSVConfig',
    'CSVOptions',
    'CSVReporter',
]
