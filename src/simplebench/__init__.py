# -*- coding: utf-8 -*-
"""Simple benchmarking framework."""

from .case import Case
from .constants import (DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_SCALE,
                        MIN_MEASURED_ITERATIONS, DEFAULT_ITERATIONS,
                        DEFAULT_SIGNIFICANT_FIGURES, DEFAULT_TIMER,
                        BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT)
from .decorators import benchmark, clear_registered_cases, get_registered_cases
from .enums import Section, Verbosity
from .exceptions import ErrorTag, SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from .runners import SimpleRunner
from .results import Results
from .iteration import Iteration
from .stats import OperationsPerInterval, OperationTimings, Stats, StatsSummary, MemoryUsage, PeakMemoryUsage
from .tasks import RichProgressTasks, RichTask
from .si_units import si_scale, si_scale_for_smallest, si_scale_to_unit, si_unit_base
from .utils import sanitize_filename, sigfigs, kwargs_variations
from .reporters import ReporterManager
from .reporters.interfaces import Reporter
from .reporters.choices import Choices, Choice, Target, Format
from .reporters.json import JSONReporter
from .reporters.reporter_option import ReporterOption
from .reporters.rich_table import RichTableReporter
from .reporters.csv import CSVReporter
from .reporters.graph import GraphReporter
from .session import Session
from .cli import main


__all__ = [
    # Core classes
    'Case',
    'Choice',
    'Choices',
    'CSVReporter',
    'Format',
    'GraphReporter',
    'Iteration',
    'JSONReporter',
    'OperationsPerInterval',
    'OperationTimings',
    'Reporter',
    'ReporterManager',
    'ReporterOption',
    'Results',
    'RichProgressTasks',
    'RichTableReporter',
    'RichTask',
    'Section',
    'Session',
    'Stats',
    'StatsSummary',
    'MemoryUsage',
    'OperationsPerInterval',
    'OperationTimings',
    'PeakMemoryUsage',
    'SimpleRunner',
    'Target',
    'Verbosity',

    # Decorator functions
    'benchmark',
    'clear_registered_cases',
    'get_registered_cases',

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
    'si_unit_base',
    'kwargs_variations',
    'sigfigs'
]
