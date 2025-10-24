# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from .choices import Choices, Choice
from .csv import CSVReporter, CSVChoiceOptions
from .graph.scatter import ScatterGraphReporter, ScatterGraphChoiceOptions, ScatterGraphOptions
from .interfaces import Reporter
from .json import JSONReporter
from .reporter_manager import ReporterManager
from .rich_table import RichTableReporter, RichTableChoiceOptions


__all__ = [
    'Choices',
    'Choice',
    'CSVReporter',
    'CSVChoiceOptions',
    'JSONReporter',
    'ScatterGraphReporter',
    'ScatterGraphChoiceOptions',
    'ScatterGraphOptions',
    'Reporter',
    'RichTableReporter',
    'RichTableChoiceOptions',
    'ReporterManager',
]
