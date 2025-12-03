"""Pytest Reporter for SimpleBench.

This package provides a Rich Table reporter for the simplebench.reporters package.
It offers functionality for generating rich table reports
from benchmark results.

Public API
----------
- :class:`~.PytestConfig`: Configuration class for the Rich Table reporter.
- :class:`~.PytestField`: Field enumeration for the Rich Table reporter.
- :class:`~.PytestOptions`: Options class for the Rich Table reporter.
- :class:`~.PytestReporter`: The Rich Table reporter class.
"""
from .reporter import PytestConfig, PytestField, PytestOptions, PytestReporter

__all__ = [
    'PytestConfig',
    'PytestField',
    'PytestOptions',
    'PytestReporter',
]
