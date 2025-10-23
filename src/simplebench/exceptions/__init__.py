# -*- coding: utf-8 -*-
"""Custom exceptions for the simplebench package."""
import argparse
from enum import Enum
from typing import Any, Generic, TypeVar

from ..enums import enum_docstrings
from .base import ErrorTag
from .case import CaseErrorTag
from .cli import CLIErrorTag
from .decorators import DecoratorsErrorTag
from .iteration import IterationErrorTag
from .results import ResultsErrorTag
from .runners import RunnersErrorTag
from .session import SessionErrorTag
from .si_units import SIUnitsErrorTag
from .utils import UtilsErrorTag
from .validators import ValidatorsErrorTag

__all__ = [
    "TaggedException",
    "SimpleBenchTypeError",
    "SimpleBenchValueError",
    "SimpleBenchKeyError",
    "SimpleBenchRuntimeError",
    "SimpleBenchNotImplementedError",
    "SimpleBenchAttributeError",
    "SimpleBenchArgumentError",
    "SimpleBenchImportError",
    "ErrorTag",
    "GlobalErrorTag",
    "CaseErrorTag",
    "CLIErrorTag",
    "DecoratorsErrorTag",
    "IterationErrorTag",
    "ResultsErrorTag",
    "RunnersErrorTag",
    "SessionErrorTag",
    "SIUnitsErrorTag",
    "UtilsErrorTag",
    "ValidatorsErrorTag",
]


@enum_docstrings
class GlobalErrorTag(ErrorTag):
    """Global collection of ErrorTags in SimpleBench."""

    # Stats() tags
    STATS_INVALID_UNIT_ARG_TYPE = "STATS_INVALID_UNIT_ARG_TYPE"
    """Invalid unit argument passed to the Stats() constructor - must be a str"""
    STATS_INVALID_UNIT_ARG_VALUE = "STATS_INVALID_UNIT_ARG_VALUE"
    """Invalid unit argument passed to the Stats() constructor - must be a non-empty str"""
    STATS_INVALID_SCALE_ARG_TYPE = "STATS_INVALID_SCALE_ARG_TYPE"
    """Invalid scale argument passed to the Stats() constructor - must be a number (int or float)"""
    STATS_INVALID_SCALE_ARG_VALUE = "STATS_INVALID_SCALE_ARG_VALUE"
    """Invalid scale argument passed to the Stats() constructor - must be greater than zero"""
    STATS_INVALID_DATA_ARG_TYPE = "STATS_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the Stats() constructor - must be a list of numbers (int or float) or None"""
    STATS_INVALID_DATA_ARG_ITEM_TYPE = "STATS_INVALID_DATA_ARG_ITEM_TYPE"
    """Invalid data argument item passed to the Stats() constructor - must be a number (int or float)"""
    STATS_COMPARISON_INCOMPATIBLE_SCALES = "STATS_COMPARISON_INCOMPATIBLE_SCALES"
    """Incompatible scales when comparing two Stats instances"""
    STATS_COMPARISON_INCOMPATIBLE_UNITS = "STATS_COMPARISON_INCOMPATIBLE_UNITS"
    """Incompatible units when comparing two Stats instances"""
    STATS_FROM_DICT_INVALID_DATA_ARG_TYPE = "STATS_FROM_DICT_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the Stats.from_dict() method - must be a dict"""
    STATS_FROM_DICT_MISSING_UNIT_KEY = "STATS_FROM_DICT_MISSING_UNIT_KEY"
    """Missing unit key in the data dictionary passed to the Stats.from_dict() method"""
    STATS_FROM_DICT_MISSING_SCALE_KEY = "STATS_FROM_DICT_MISSING_SCALE_KEY"
    """Missing scale key in the data dictionary passed to the Stats.from_dict() method"""
    STATS_FROM_DICT_MISSING_DATA_KEY = "STATS_FROM_DICT_MISSING_DATA_KEY"
    """Missing data key in the data dictionary passed to the Stats.from_dict() method"""

    # MemoryUsage() tags
    STATS_MEMORY_USAGE_INVALID_ITERATIONS_ARG_TYPE = "STATS_MEMORY_USAGE_INVALID_ITERATIONS_ARG_TYPE"
    """Invalid iterations argument passed to the MemoryUsage() constructor
    - must be a Sequence of Iteration objects or None"""
    STATS_MEMORY_USAGE_INVALID_ITERATIONS_ITEM_ARG_TYPE = "STATS_MEMORY_USAGE_INVALID_ITERATIONS_ITEM_ARG_TYPE"
    """Invalid type of item passed to the MemoryUsage() constructor in the iterations argument
    - all items must be Iteration objects"""
    STATS_MEMORY_USAGE_INVALID_DATA_ARG_TYPE = "STATS_MEMORY_USAGE_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the MemoryUsage() constructor
    - must be a sequence of numbers (int or float) or None"""
    STATS_MEMORY_USAGE_INVALID_DATA_ARG_ITEM_TYPE = "STATS_MEMORY_USAGE_INVALID_DATA_ARG_ITEM_TYPE"
    """Invalid data argument item passed to the MemoryUsage() constructor - must be a number (int or float)"""
    STATS_MEMORY_USAGE_INVALID_DATA_ARG_VALUE = "STATS_MEMORY_USAGE_INVALID_DATA_ARG_VALUE"
    """Invalid data argument value passed to the MemoryUsage() constructor
    - must be a non-empty sequence of numbers (int or float)"""
    STATS_MEMORY_USAGE_NO_DATA_OR_ITERATIONS_PROVIDED = "STATS_MEMORY_USAGE_NO_DATA_OR_ITERATIONS_PROVIDED"
    """No data or iterations provided to the MemoryUsage() constructor"""

    # PeakMemoryUsage() tags
    STATS_PEAK_MEMORY_USAGE_INVALID_ITERATIONS_ARG_TYPE = "STATS_PEAK_MEMORY_USAGE_INVALID_ITERATIONS_ARG_TYPE"
    """Invalid iterations argument passed to the PeakMemoryUsage() constructor
    - must be a Sequence of Iteration objects or None"""
    STATS_PEAK_MEMORY_USAGE_INVALID_ITERATIONS_ITEM_ARG_TYPE = (
        "STATS_PEAK_MEMORY_USAGE_INVALID_ITERATIONS_ITEM_ARG_TYPE")
    """Invalid type of item passed to the PeakMemoryUsage() constructor in the iterations argument
    - all items must be Iteration objects"""
    STATS_PEAK_MEMORY_USAGE_INVALID_DATA_ARG_TYPE = "STATS_PEAK_MEMORY_USAGE_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the PeakMemoryUsage() constructor
    - must be a sequence of numbers (int or float) or None"""
    STATS_PEAK_MEMORY_USAGE_INVALID_DATA_ARG_ITEM_TYPE = "STATS_PEAK_MEMORY_USAGE_INVALID_DATA_ARG_ITEM_TYPE"
    """Invalid data argument item passed to the PeakMemoryUsage() constructor - must be a number (int or float)"""
    STATS_PEAK_MEMORY_USAGE_INVALID_DATA_ARG_VALUE = "STATS_PEAK_MEMORY_USAGE_INVALID_DATA_ARG_VALUE"
    """Invalid data argument value passed to the PeakMemoryUsage() constructor
    - must be a non-empty sequence of numbers (int or float)"""
    STATS_PEAK_MEMORY_USAGE_NO_DATA_OR_ITERATIONS_PROVIDED = "STATS_PEAK_MEMORY_USAGE_NO_DATA_OR_ITERATIONS_PROVIDED"
    """No data or iterations provided to the PeakMemoryUsage() constructor"""

    # OperationsPerInterval() tags
    STATS_OPS_INVALID_ITERATIONS_ARG_TYPE = "STATS_OPS_INVALID_ITERATIONS_ARG_TYPE"
    """Invalid iterations argument passed to the OperationsPerInterval() constructor
    - must be a Sequence of Iteration objects or None"""
    STATS_OPS_INVALID_ITERATIONS_ITEM_ARG_TYPE = "STATS_OPS_INVALID_ITERATIONS_ITEM_ARG_TYPE"
    """Invalid type of item passed to the OperationsPerInterval() constructor in the iterations argument
    - all items must be Iteration objects"""
    STATS_OPS_INVALID_DATA_ARG_TYPE = "STATS_OPS_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the OperationsPerInterval() constructor
    - must be a sequence of numbers (int or float) or None"""
    STATS_OPS_INVALID_DATA_ARG_ITEM_TYPE = "STATS_OPS_INVALID_DATA_ARG_ITEM_TYPE"
    """Invalid data argument item passed to the OperationsPerInterval() constructor - must be a number (int or float)"""
    STATS_OPS_INVALID_DATA_ARG_VALUE = "STATS_OPS_INVALID_DATA_ARG_VALUE"
    """Invalid data argument value passed to the OperationsPerInterval() constructor
    - must be a non-empty sequence of numbers (int or float)"""
    STATS_OPS_NO_DATA_OR_ITERATIONS_PROVIDED = "STATS_OPS_NO_DATA_OR_ITERATIONS_PROVIDED"
    """No data or iterations provided to the OperationsPerInterval() constructor"""

    # OperationTimings() tags
    STATS_TIMINGS_INVALID_ITERATIONS_ARG_TYPE = "STATS_TIMINGS_INVALID_ITERATIONS_ARG_TYPE"
    """Invalid iterations argument passed to the OperationTimings() constructor
    - must be a Sequence of Iteration objects or None"""
    STATS_TIMINGS_INVALID_ITERATIONS_ITEM_ARG_TYPE = "STATS_TIMINGS_INVALID_ITERATIONS_ITEM_ARG_TYPE"
    """Invalid type of item passed to the OperationTimings() constructor in the iterations argument
    - all items must be Iteration objects"""
    STATS_TIMINGS_INVALID_DATA_ARG_TYPE = "STATS_TIMINGS_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the OperationTimings() constructor
    - must be a sequence of numbers (int or float) or None"""
    STATS_TIMINGS_INVALID_DATA_ARG_ITEM_TYPE = "STATS_TIMINGS_INVALID_DATA_ARG_ITEM_TYPE"
    """Invalid data argument item passed to the OperationTimings() constructor - must be a number (int or float)"""
    STATS_TIMINGS_INVALID_DATA_ARG_VALUE = "STATS_TIMINGS_INVALID_DATA_ARG_VALUE"
    """Invalid data argument value passed to the OperationTimings() constructor
    - must be a non-empty sequence of numbers (int or float)"""
    STATS_TIMINGS_NO_DATA_OR_ITERATIONS_PROVIDED = "STATS_TIMINGS_NO_DATA_OR_ITERATIONS_PROVIDED"
    """No data or iterations provided to the OperationTimings() constructor"""

    # StatsSummary() tags
    STATS_SUMMARY_INVALID_UNIT_ARG_TYPE = "STATS_SUMMARY_INVALID_UNIT_ARG_TYPE"
    """Invalid unit argument passed to the StatsSummary() constructor - must be a str"""
    STATS_SUMMARY_INVALID_UNIT_ARG_VALUE = "STATS_SUMMARY_INVALID_UNIT_ARG_VALUE"
    """Invalid unit argument passed to the StatsSummary() constructor - must be a non-empty str"""
    STATS_SUMMARY_INVALID_SCALE_ARG_TYPE = "STATS_SUMMARY_INVALID_SCALE_ARG_TYPE"
    """Invalid scale argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_SCALE_ARG_VALUE = "STATS_SUMMARY_INVALID_SCALE_ARG_VALUE"
    """Invalid scale argument passed to the StatsSummary() constructor - must be greater than zero"""
    STATS_SUMMARY_INVALID_MINIMUM_ARG_TYPE = "STATS_SUMMARY_INVALID_MINIMUM_ARG_TYPE"
    """Invalid minimum argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_MAXIMUM_ARG_TYPE = "STATS_SUMMARY_INVALID_MAXIMUM_ARG_TYPE"
    """Invalid maximum argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_MEAN_ARG_TYPE = "STATS_SUMMARY_INVALID_MEAN_ARG_TYPE"
    """Invalid mean argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_MEDIAN_ARG_TYPE = "STATS_SUMMARY_INVALID_MEDIAN_ARG_TYPE"
    """Invalid median argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_STANDARD_DEVIATION_ARG_TYPE = "STATS_SUMMARY_INVALID_STANDARD_DEVIATION_ARG_TYPE"
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_STANDARD_DEVIATION_ARG_VALUE = "STATS_SUMMARY_INVALID_STANDARD_DEVIATION_ARG_VALUE"
    """Invalid standard_deviation argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE = (
        "STATS_SUMMARY_INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE")
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be a number (int or float)"""
    STATS_SUMMARY_INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE = (
        "STATS_SUMMARY_INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE")
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be greater than zero"""
    STATS_SUMMARY_INVALID_PERCENTILES_ARG_TYPE = "STATS_SUMMARY_INVALID_PERCENTILES_ARG_TYPE"
    """Invalid percentiles argument passed to the StatsSummary() constructor
    - must be a sequence of numbers (int or float)"""
    STATS_SUMMARY_INVALID_PERCENTILES_ARG_VALUE = "STATS_SUMMARY_INVALID_PERCENTILES_ARG_VALUE"
    """Invalid percentiles item passed to the StatsSummary() constructor in sequence
    - must be a number (int or float)"""
    STATS_SUMMARY_FROM_DICT_INVALID_DATA_ARG_TYPE = "STATS_SUMMARY_FROM_DICT_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the StatsSummary.from_dict() method - must be a dict"""
    STATS_SUMMARY_FROM_DICT_MISSING_KEY = "STATS_SUMMARY_FROM_DICT_MISSING_KEY"
    """Missing key in the data dictionary passed to the StatsSummary.from_dict() method"""
    STATS_SUMMARY_FROM_STATS_INVALID_STATS_ARG_TYPE = "STATS_SUMMARY_FROM_STATS_INVALID_STATS_ARG_TYPE"
    """Invalid stats argument passed to the StatsSummary.from_stats() method - must be a Stats instance"""

    # CSVReporter() tags
    CSV_REPORTER_INIT_INVALID_CASE_ARG = "CSV_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter() constructor"""
    CSV_REPORTER_INIT_INVALID_SESSION_ARG = "CSV_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the CSVReporter() constructor"""
    CSV_REPORTER_RUN_REPORT_INVALID_CASE_ARG = "CSV_REPORTER_RUN_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter.run_report() method"""
    CSV_REPORTER_RUN_REPORT_INVALID_SESSION_ARG = "CSV_REPORTER_RUN_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the CSVReporter.run_report() method"""
    CSV_REPORTER_RUN_REPORT_INVALID_CHOICE_ARG = "CSV_REPORTER_RUN_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the CSVReporter.run_report() method"""
    CSV_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION = "CSV_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the CSVReporter.run_report() method in the choice.sections"""
    CSV_REPORTER_TO_CSV_INVALID_CASE_ARG = "CSV_REPORTER_TO_CSV_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_TO_CSV_INVALID_CSVFILE_ARG = "CSV_REPORTER_TO_CSV_INVALID_CSVFILE_ARG"
    """Something other than a file-like object was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_TO_CSV_INVALID_BASE_UNIT_ARG = "CSV_REPORTER_TO_CSV_INVALID_BASE_UNIT_ARG"
    """Something other than a non-empty string was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_TO_CSV_INVALID_TARGET_ARG = "CSV_REPORTER_TO_CSV_INVALID_TARGET_ARG"
    """Something other than a valid target string was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_RUN_REPORT_INVALID_PATH_ARG_TYPE = "CSV_REPORTER_RUN_REPORT_INVALID_PATH_ARG_TYPE"
    """Something other than a Path instance was passed to the CSVReporter.run_report() method as the path arg"""
    CSV_REPORTER_RUN_REPORT_INVALID_CALLBACK_ARG_TYPE = "CSV_REPORTER_RUN_REPORT_INVALID_CALLBACK_ARG_TYPE"
    """Something other than a callable was passed to the CSVReporter.run_report() method as the callback arg"""
    REPORTER_RUN_REPORT_UNSUPPORTED_TARGET = "REPORTER_RUN_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the reporter's run_report() method"""

    # ScatterGraphReporter() tags
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE")
    """The default targets specified in the ScatterGraphChoiceOptions must be an iterable of Target enum members."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE")
    """The default targets specified in the ScatterGraphChoiceOptions are not valid Target enum members."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE")
    """The default targets specified in the ScatterGraphChoiceOptions cannot be empty."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_SUBDIR_TYPE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_SUBDIR_TYPE")
    """The subdir specified in the ScatterGraphChoiceOptions must be a string."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_SUBDIR_VALUE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_SUBDIR_VALUE")
    """The subdir specified in the ScatterGraphChoiceOptions cannot be an empty string."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_WIDTH_TYPE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_WIDTH_TYPE")
    """The width specified in the ScatterGraphChoiceOptions must be an integer."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_WIDTH_VALUE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_WIDTH_VALUE")
    """The width specified in the ScatterGraphChoiceOptions must be greater than zero."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_HEIGHT_TYPE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_HEIGHT_TYPE")
    """The height specified in the ScatterGraphChoiceOptions must be an integer."""
    SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_HEIGHT_VALUE = (
        "SCATTER_GRAPH_REPORTER_CHOICE_OPTIONS_INVALID_HEIGHT_VALUE")
    """The height specified in the ScatterGraphChoiceOptions must be greater than zero."""

    # ScatterGraphReporter() tags
    GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_THEME_TYPE = "GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_THEME_TYPE"
    """The theme specified in the GraphOptions has an invalid type. It must be a dict or None."""
    GRAPH_REPORTER_INIT_INVALID_CASE_ARG = "GRAPH_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the ScatterGraphReporter() constructor"""
    GRAPH_REPORTER_INIT_INVALID_SESSION_ARG = "GRAPH_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the ScatterGraphReporter() constructor"""
    GRAPH_REPORTER_REPORT_INVALID_CASE_ARG = "GRAPH_REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the ScatterGraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG = "GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the ScatterGraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG = "GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the ScatterGraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION = "GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the ScatterGraphReporter.report() method in the Choice.sections"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET = "GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the ScatterGraphReporter.report() method in the Choice.targets"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT = "GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the ScatterGraphReporter.report() method in the Choice.formats"""
    GRAPH_REPORTER_REPORT_MISSING_PATH_ARG = "GRAPH_REPORTER_REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the ScatterGraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_PATH_ARG = "GRAPH_REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the ScatterGraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG = "GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the ScatterGraphReporter.report() method as the callback argument"""
    GRAPH_REPORTER_RUN_REPORT_INVALID_PATH_ARG = "GRAPH_REPORTER_RUN_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the ScatterGraphReporter.run_report() method as the path arg"""
    GRAPH_REPORTER_RUN_REPORT_UNSUPPORTED_OUTPUT_FORMAT = "GRAPH_REPORTER_RUN_REPORT_UNSUPPORTED_OUTPUT_FORMAT"
    """The output format specified in the GraphOptions is not supported. Supported formats are 'svg' and 'png'"""
    GRAPH_REPORTER_GRAPH_OPTIONS_UNSUPPORTED_STYLE = "GRAPH_REPORTER_GRAPH_OPTIONS_UNSUPPORTED_STYLE"
    """The style specified in the GraphOptions is not supported. Supported styles are 'darkgrid' and 'default'"""
    GRAPH_REPORTER_GRAPH_OPTIONS_UNSUPPORTED_OUTPUT_FORMAT = "GRAPH_REPORTER_GRAPH_OPTIONS_UNSUPPORTED_OUTPUT_FORMAT"
    """The output format specified in the GraphOptions is not supported. Supported formats are 'svg' and 'png'"""
    GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_ASPECT_RATIO = "GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_ASPECT_RATIO"
    """The aspect ratio specified in the GraphOptions is invalid. It must be a positive number."""
    GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_X_LABELS_ROTATION_TYPE = (
        "GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_X_LABELS_ROTATION_TYPE")
    """The x_labels_rotation specified in the GraphOptions has an invalid type. It must be a float."""
    GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_Y_STARTS_AT_ZERO_TYPE = (
        "GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_Y_STARTS_AT_ZERO_TYPE")
    """The y_starts_at_zero value specified in the GraphOptions has an invalid type. It must be a bool."""
    GRAPH_REPORTER_PLOT_INVALID_CASE_ARG = "GRAPH_REPORTER_PLOT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the ScatterGraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG = "GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG"
    """Something other than a Path instance was passed to the ScatterGraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_SECTION_ARG = "GRAPH_REPORTER_PLOT_INVALID_SECTION_ARG"
    """Something other than a valid Section was passed to the ScatterGraphReporter.plot() method"""

    # JSONReporter() tags
    JSON_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION = "JSON_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the JSONReporter.run_report() method in the choice.sections"""
    REPORTER_JSON_OUTPUT_ERROR = "REPORTER_JSON_OUTPUT_ERROR"
    """An error occurred while serializing the JSON output."""

    # RichTask() tags
    RICH_TASK_INIT_INVALID_NAME_ARG = "RICH_TASK_INIT_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichTask() constructor"""
    RICH_TASK_INIT_INVALID_DESCRIPTION_ARG = "RICH_TASK_INIT_INVALID_DESCRIPTION_ARG"
    """Something other than a string or rich.Text was passed to the RichTask() constructor"""
    RICH_TASK_INIT_INVALID_PROGRESS_ARG = "RICH_TASK_INIT_INVALID_PROGRESS_ARG"
    """Something other than a Progress instance was passed to the RichTask() constructor"""
    RICH_TASK_INIT_EMPTY_STRING_NAME = "RICH_TASK_INIT_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    RICH_TASK_INIT_EMPTY_STRING_DESCRIPTION = "RICH_TASK_INIT_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    RICH_TASK_UPDATE_INVALID_COMPLETED_ARG = "RICH_TASK_UPDATE_INVALID_COMPLETED_ARG"
    """Something other than an int was passed to the RichTask() update method"""
    RICH_TASK_UPDATE_INVALID_DESCRIPTION_ARG = "RICH_TASK_UPDATE_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichTask() update method"""
    RICH_TASK_UPDATE_INVALID_REFRESH_ARG = "RICH_TASK_UPDATE_INVALID_REFRESH_ARG"
    """Something other than a bool was passed to the RichTask() update method"""
    RICH_TASK_UPDATE_ALREADY_TERMINATED_TASK = "RICH_TASK_UPDATE_ALREADY_TERMINATED_TASK"
    """The task has already been terminated"""
    RICH_TASK_TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK = "RICH_TASK_TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK"
    """The task has already been terminated"""

    # Rich ProgressTask() tags
    RICH_PROGRESS_TASK_DELITEM_INVALID_NAME_ARG = "RICH_PROGRESS_TASK_DELITEM_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() __delitem__ method"""
    RICH_PROGRESS_TASK_DELITEM_NOT_FOUND = "RICH_PROGRESS_TASK_DELITEM_NOT_FOUND"
    """The requested task was not found"""
    RICH_PROGRESS_TASK_GETITEM_INVALID_NAME_ARG = "RICH_PROGRESS_TASK_GETITEM_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() __getitem__ method"""
    RICH_PROGRESS_TASK_GETITEM_NOT_FOUND = "RICH_PROGRESS_TASK_GETITEM_NOT_FOUND"
    """The requested task was not found"""
    RICH_PROGRESS_TASK_NEW_TASK_INVALID_NAME_ARG = "RICH_PROGRESS_TASK_NEW_TASK_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() new_task method"""
    RICH_PROGRESS_TASK_NEW_TASK_INVALID_DESCRIPTION_ARG = "RICH_PROGRESS_TASK_NEW_TASK_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichProgressTask() new_task method"""
    RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_NAME = "RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_DESCRIPTION = "RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    RICH_PROGRESS_TASKS_INIT_INVALID_VERBOSITY_ARG = "RICH_PROGRESS_TASKS_INIT_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the RichProgressTasks()
    constructor as the verbosity arg"""
    RICH_PROGRESS_TASKS_INIT_INVALID_PROGRESS_ARG = "RICH_PROGRESS_TASKS_INIT_INVALID_PROGRESS_ARG"
    """Something other than a Progress instance was passed to the RichProgressTasks() constructor as the progress arg"""
    RICH_PROGRESS_TASKS_INIT_INVALID_CONSOLE_ARG = "RICH_PROGRESS_TASKS_INIT_INVALID_CONSOLE_ARG"
    """Something other than a Console instance was passed to the RichProgressTasks() constructor as the console arg"""

    # reporters.ReporterManager() tags
    REPORTER_MANAGER_REGISTER_INVALID_REPORTER_ARG = "REPORTER_MANAGER_REGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the ReporterManager.register() method"""
    REPORTER_MANAGER_REGISTER_INVALID_CHOICES_RETURNED = "REPORTER_MANAGER_REGISTER_INVALID_CHOICES_RETURNED"
    """Something other than a Choices instance was returned from the reporter.choices property"""
    REPORTER_MANAGER_REGISTER_INVALID_CHOICES_CONTENT = "REPORTER_MANAGER_REGISTER_INVALID_CHOICES_CONTENT"
    """Something other than a Choice instance was found in the Choices instance returned
    from the reporter.choices property"""
    REPORTER_MANAGER_REGISTER_DUPLICATE_NAME = "REPORTER_MANAGER_REGISTER_DUPLICATE_NAME"
    """A Reporter with the same name already exists in the ReporterManager instance"""
    REPORTER_MANAGER_REGISTER_DUPLICATE_CLI_ARG = "REPORTER_MANAGER_REGISTER_DUPLICATE_CLI_ARG"
    """A Reporter with the same CLI argument already exists in the ReporterManager instance"""
    REPORTER_MANAGER_UNREGISTER_INVALID_REPORTER_ARG = "REPORTER_MANAGER_UNREGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the ReporterManager.unregister() method"""
    REPORTER_MANAGER_UNREGISTER_UNKNOWN_NAME = "REPORTER_MANAGER_UNREGISTER_UNKNOWN_NAME"
    """No Reporter with the given name is registered in the ReporterManager instance"""
    REPORTER_MANAGER_ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG = (
        "REPORTER_MANAGER_ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG"
    )
    """Something other than an ArgumentParser instance was passed to the
    ReporterManager.add_reporters_to_argparse() method"""
    REPORTER_MANAGER_ARGUMENT_ERROR_ADDING_FLAGS = "REPORTER_MANAGER_ARGUMENT_ERROR_ADDING_FLAGS"
    """An ArgumentError was raised when adding reporter flags to the ArgumentParser instance"""

    # validate.py - validate_reporter_callback() tags
    VALIDATE_INVALID_REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE = "VALIDATE_INVALID_REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE"
    """The reporter callback is neither a callable nor None"""
    VALIDATE_INVALID_REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS = (
        "VALIDATE_INVALID_REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS")
    """The reporter callback does not have the correct number of parameters"""

    # validate.py - validate_callback() tags
    VALIDATE_INVALID_CALLBACK_UNRESOLVABLE_HINTS = "VALIDATE_INVALID_CALLBACK_UNRESOLVABLE_HINTS"
    """The type hints for the callback function could not be resolved"""

    # validate.py - validate_callback_parameter() tags
    VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER = (
        "VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER")
    """The callback function is missing a required parameter"""
    VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE = (
        "VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE")
    """The callback function has a parameter with an incorrect type annotation"""
    VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY = (
        "VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function has a parameter that is not keyword-only"""


E = TypeVar('E', bound=Exception)


class TaggedException(Exception, Generic[E]):
    """
    A generic exception that can be specialized with a base exception type
    and requires a tag during instantiation.

    This class extends the built-in Exception class and adds a mandatory tag
    attribute. The tag is intended to provide additional context or categorization
    for the exception.

    The tag must be an instance of Enum to ensure a controlled set of possible tags and
    must be the first argument provided during instantiation if passed positionally.

    It is used by other exceptions in the simplebench package to provide
    standardized error tagging for easier identification and handling of specific error conditions.
    and is used to create exceptions with specific tags for error handling and identification.
    with this base class.

    Example:

    class MyTaggedException(TaggedException[ValueError]):
    '''A tagged exception that is a specialized ValueError.'''

    raise MyTaggedException("An error occurred", tag=MyErrorTags.SOME_ERROR)


    Args:
        tag (Enum, keyword): An Enum member representing the error code.
        *args: Positional arguments to pass to the base exception's constructor.
        **kwargs: Keyword arguments to pass to the base exception's constructor.

    Attributes:
        tag_code: Enum
    """
    def __init__(self, *args: Any, tag: Enum, **kwargs: Any) -> None:
        """
        Initializes the exception with a mandatory tag.

        Args:
            *args: Positional arguments to pass to the base exception's constructor.
            tag (Enum, keyword): An Enum member representing the error code.
            **kwargs: Keyword arguments to pass to the base exception's constructor.
        """
        if not isinstance(tag, Enum):
            raise TypeError("Missing or wrong type 'tag' argument (must be Enum)")
        self.tag_code = tag
        super().__init__(*args, **kwargs)


class SimpleBenchTypeError(TaggedException[ValueError]):
    """Base class for all SimpleBench type errors.

    It differs from a standard TypeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchTypeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str, positional): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchTypeError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchValueError(TaggedException[ValueError]):
    """Base class for all SimpleBench value errors.

    It differs from a standard ValueError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchValueError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchKeyError(TaggedException[KeyError]):
    """Base class for all SimpleBench key errors.

    It differs from a standard KeyError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchKeyError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchKeyError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchRuntimeError(TaggedException[RuntimeError]):
    """Base class for all SimpleBench runtime errors.

    It differs from a standard RuntimeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchRuntimeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchRuntimeError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchNotImplementedError(TaggedException[NotImplementedError]):
    """Base class for all SimpleBench not implemented errors.

    It differs from a standard NotImplementedError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchNotImplementedError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchNotImplementedError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchAttributeError(TaggedException[AttributeError]):
    """Base class for all SimpleBench attribute errors.

    It differs from a standard AttributeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchAttributeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
        name (str | None): The attribute name.
        obj (object): The object the attribute was not found on.
    """
    def __init__(self, msg: str, *, tag: ErrorTag, name: str | None = None, obj: object = ..., ) -> None:
        """Raises a SimpleBenchAttributeError with the given message, name, obj, and tag.

        Args:
            msg (str): The error message.
            name (str | None): The attribute name.
            obj (object): The object the attribute was not found on.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag, name=name, obj=obj)


class SimpleBenchArgumentError(TaggedException[argparse.ArgumentError]):
    """Base class for re-raising all SimpleBench ArgumentError errors.

    It is designed to be used in places where an argparse.ArgumentError
    would be appropriate and for re-raising ArgumentErrors
    caught from argparse operations.

    It differs from a argparse.ArgumentError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support
    and by directly setting the argument_name property to the name of the
    argument that caused the error. This is because the argparse.ArgumentError
    constructor expects an argparse.Action instance as the first argument
    and that is not always available when re-raising the exception.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchArgumentError(argument_name="my-arg",
                                       message="An error occurred",
                                       tag=MyErrorTags.SOME_ERROR)

    Args:
        argument_name (str | None): The argument name.
        message (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, argument_name: str | None, message: str, *, tag: ErrorTag) -> None:
        # argparse.ArgumentError has a specific signature we must adapt to. It expects
        # to get an argparse.Action instance as the first argument to infer the
        # argument_name from, which we don't have here, and so must backfill the argument_name
        # after initialization.
        if tag.__doc__ is None:
            message = f"{message}: {tag.value}"
        else:
            message = f"{message}: {tag.__doc__}"
        super().__init__(None, message, tag=tag)
        self.argument_name = argument_name


class SimpleBenchImportError(TaggedException[ImportError]):
    """Base class for all SimpleBench import errors.

    It differs from a standard ImportError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchImportError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchImportError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)

