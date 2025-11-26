"""JSON Reporter public API.

Purpose is to provide a JSON reporter for the simplebench.reporters package.
This package provides functionality for generating JSON reports
from benchmark results.

Public API
----------
- :class:`~.JSONConfig`: Configuration class for the JSON reporter.
- :class:`~.JSONOptions`: Options class for the JSON reporter.
- :class:`~.JSONReporter`: The JSON reporter class.
"""
from .reporter import JSONConfig, JSONOptions, JSONReporter

__all__ = [
    'JSONReporter',
    'JSONConfig',
    'JSONOptions',
]
