# -*- coding: utf-8 -*-
"""Simple benchmarking framework."""

from .case import Case
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
from .tasks import ProgressTasks
from .utils import (sanitize_filename, si_scale_for_smallest, si_scale, si_scale_to_unit, sigfigs)


__all__ = [
    # Core classes
    'Case',
    'Iteration',
    'Results',
    'SimpleRunner',
    'ProgressTasks',
    'Session',

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
    'sanitize_filename',
    'si_scale_for_smallest',
    'si_scale',
    'si_scale_to_unit',
    'sigfigs'
]
