# -*- coding: utf-8 -*-
"""Simple benchmarking framework."""

from .case import Case
from .cli import main
from .constants import (DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_SCALE,
                        MIN_MEASURED_ITERATIONS, DEFAULT_ITERATIONS,
                        DEFAULT_SIGNIFICANT_FIGURES, DEFAULT_TIMER,
                        BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT)
from .exceptions import ErrorTag, SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from .runners import SimpleRunner
from .results import Results
from .iteration import Iteration
from .session import Session, Verbosity
from .stats import OperationsPerInterval, OperationTimings, Stats
from .tasks import RichProgressTasks, RichTask
from .utils import sanitize_filename, si_scale_for_smallest, si_scale, si_scale_to_unit, sigfigs
from .reporters.interfaces import Reporter
from .reporters.choices import Choices, Choice, Section, Target, Format
from .reporters.rich_table import RichTableReporter
from .reporters.csv import CSVReporter
from .reporters.graph import GraphReporter


__all__ = [
    # Core classes
    'Case',
    'Choice',
    'Choices',
    'CSVReporter',
    'Format',
    'GraphReporter',
    'Iteration',
    'OperationsPerInterval',
    'OperationTimings',
    'Reporter',
    'Results',
    'RichProgressTasks',
    'RichTableReporter',
    'RichTask',
    'Section',
    'Session',
    'Stats',
    'SimpleRunner',
    'Target',
    'Verbosity',

    # Exceptions
    'ErrorTag',
    'SimpleBenchKeyError',
    'SimpleBenchTypeError',
    'SimpleBenchValueError',

    # Constants
    'MIN_MEASURED_ITERATIONS',
    'DEFAULT_ITERATIONS',
    'DEFAULT_SIGNIFICANT_FIGURES',
    'DEFAULT_TIMER',
    'DEFAULT_INTERVAL_SCALE',
    'DEFAULT_INTERVAL_UNIT',
    'DEFAULT_OPS_PER_INTERVAL_SCALE',
    'DEFAULT_OPS_PER_INTERVAL_UNIT',
    'BASE_INTERVAL_UNIT',
    'BASE_OPS_PER_INTERVAL_UNIT',

    # Utility functions
    'main',
    'sanitize_filename',
    'si_scale_for_smallest',
    'si_scale',
    'si_scale_to_unit',
    'sigfigs'
]
