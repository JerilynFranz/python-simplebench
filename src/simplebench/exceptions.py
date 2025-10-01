# -*- coding: utf-8 -*-
"""Custom exceptions for the simplebench package."""
import argparse
from enum import Enum
from sys import version_info
from typing import Any, Generic, TypeVar


class ErrorTag(str, Enum):
    """Tags for error path identification for tests for the simplebench packages.

    ErrorTags' are used to identify specific error conditions in the simplebench package.
    Tests use these tags to assert specific error condition paths.
    """
    # @benchmark decorator tags
    BENCHMARK_DECORATOR_GROUP_TYPE = "BENCHMARK_DECORATOR_GROUP_TYPE"
    """Something other than a str was passed as the group"""
    BENCHMARK_DECORATOR_GROUP_VALUE = "BENCHMARK_DECORATOR_GROUP_VALUE"
    """The group must be a non-empty string"""
    BENCHMARK_DECORATOR_TITLE_TYPE = "BENCHMARK_DECORATOR_TITLE_TYPE"
    """Something other than a str was passed as the title"""
    BENCHMARK_DECORATOR_TITLE_VALUE = "BENCHMARK_DECORATOR_TITLE_VALUE"
    """The title must be a non-empty string"""
    BENCHMARK_DECORATOR_DESCRIPTION_TYPE = "BENCHMARK_DECORATOR_DESCRIPTION_TYPE"
    """Something other than a str was passed as the description"""
    BENCHMARK_DECORATOR_DESCRIPTION_VALUE = "BENCHMARK_DECORATOR_DESCRIPTION_VALUE"
    """The description must be a non-empty string"""
    BENCHMARK_DECORATOR_ITERATIONS_TYPE = "BENCHMARK_DECORATOR_ITERATIONS_TYPE"
    """Something other than an int was passed as the iterations"""
    BENCHMARK_DECORATOR_ITERATIONS_VALUE = "BENCHMARK_DECORATOR_ITERATIONS_VALUE"
    """The iterations must be a positive integer"""
    BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE = "BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE"
    """Something other than an int was passed as the warmup_iterations"""
    BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE = "BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE"
    """The warmup_iterations must be a non-negative integer"""
    BENCHMARK_DECORATOR_MIN_TIME_TYPE = "BENCHMARK_DECORATOR_MIN_TIME_TYPE"
    """Something other than a float was passed as the min_time"""
    BENCHMARK_DECORATOR_MIN_TIME_VALUE = "BENCHMARK_DECORATOR_MIN_TIME_VALUE"
    """The min_time must be a positive float"""
    BENCHMARK_DECORATOR_MAX_TIME_TYPE = "BENCHMARK_DECORATOR_MAX_TIME_TYPE"
    """Something other than a float was passed as the max_time"""
    BENCHMARK_DECORATOR_MAX_TIME_VALUE = "BENCHMARK_DECORATOR_MAX_TIME_VALUE"
    """The max_time must be a positive float"""
    BENCHMARK_DECORATOR_VARIATION_COLS_TYPE = "BENCHMARK_DECORATOR_VARIATION_COLS_TYPE"
    """Something other than a dict was passed as the variation_cols"""
    BENCHMARK_DECORATOR_VARIATION_COLS_VALUE = "BENCHMARK_DECORATOR_VARIATION_COLS_VALUE"
    """The variation_cols must be a non-empty dictionary"""
    BENCHMARK_DECORATOR_KWARGS_VARIATIONS_TYPE = "BENCHMARK_DECORATOR_KWARGS_VARIATIONS_TYPE"
    """Something other than a dict was passed as the kwargs_variations"""
    BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE = "BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE"
    """The kwargs_variations must be a non-empty dictionary"""
    BENCHMARK_DECORATOR_OPTIONS_TYPE = "BENCHMARK_DECORATOR_OPTIONS_TYPE"
    """Something other than a list was passed as the options"""
    BENCHMARK_DECORATOR_OPTIONS_VALUE = "BENCHMARK_DECORATOR_OPTIONS_VALUE"
    """The options must be a non-empty list"""
    BENCHMARK_DECORATOR_N_TYPE = "BENCHMARK_DECORATOR_N_TYPE"
    """Something other than an int was passed as the n"""
    BENCHMARK_DECORATOR_N_VALUE = "BENCHMARK_DECORATOR_N_VALUE"
    """The n must be a positive integer"""
    BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE = "BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE"
    """Something other than a str was passed as the use_field_for_n"""
    BENCHMARK_DECORATOR_USE_FIELD_FOR_N_VALUE = "BENCHMARK_DECORATOR_USE_FIELD_FOR_N_VALUE"
    """The use_field_for_n must be a non-empty string"""
    BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS = "BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS"
    """The use_field_for_n must be a key in kwargs_variations"""
    BENCHMARK_DECORATOR_USE_FIELD_FOR_N_VALUES = "BENCHMARK_DECORATOR_USE_FIELD_FOR_N_VALUES"
    """If use_field_for_n is provided, the matching kwargs_variations field must have positive integer values only"""
    BENCHMARK_DECORATOR_KWARGS_VARIATIONS_KEY_TYPE = "BENCHMARK_DECORATOR_KWARGS_VARIATIONS_KEY_TYPE"
    """Something other than a str was passed as the key in kwargs_variations"""
    BENCHMARK_DECORATOR_KWARGS_VARIATIONS_KEY_VALUE = "BENCHMARK_DECORATOR_KWARGS_VARIATIONS_KEY_VALUE"
    """The keys in kwargs_variations must be non-empty strings."""
    BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_TYPE = "BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_TYPE"
    """Something other than a list was passed as the value in kwargs_variations"""
    BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_VALUE = "BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_VALUE"
    """The values for each key in kwargs_variations must be a list of values, and cannot be an empty list."""
    BENCHMARK_DECORATOR_VARIATION_COLS_KEY_TYPE = "BENCHMARK_DECORATOR_VARIATION_COLS_KEY_TYPE"
    """Something other than a str was passed as the key in variation_cols"""
    BENCHMARK_DECORATOR_VARIATION_COLS_KEY_VALUE = "BENCHMARK_DECORATOR_VARIATION_COLS_KEY_VALUE"
    """The keys in variation_cols must be non-empty strings."""
    BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_TYPE = "BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_TYPE"
    """Something other than a non-empty str was passed as the value in variation_cols"""
    BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_VALUE = "BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_VALUE"
    """The values in variation_cols must be non-empty strings."""
    BENCHMARK_DECORATOR_VARIATION_COLS_KWARGS_VARIATIONS = (
            "BENCHMARK_DECORATOR_VARIATION_COLS_KWARGS_VARIATIONS")
    """The 'variation_cols' parameter to the @benchmark decorator requires "
    that 'kwargs_variations' also be provided."""
    BENCHMARK_DECORATOR_VARIATION_COLS_KWARGS_VARIATIONS_MISMATCH = (
            "BENCHMARK_DECORATOR_VARIATION_COLS_KWARGS_VARIATIONS_MISMATCH")
    """The keys in variation_cols must also be present in kwargs_variations."""
    BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE = "BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE"
    """The value in kwargs_variations for the key specified in use_field_for_n must be a positive integer."""
    BENCHMARK_DECORATOR_USE_FIELD_FOR_N_MISSING_IN_RUNNER = (
            "BENCHMARK_DECORATOR_USE_FIELD_FOR_N_MISSING_IN_RUNNER")
    """The use_field_for_n parameter was specified, but the matching field is missing
    from the kwargs from the runner."""

    # Results() tags
    RESULTS_GROUP_INVALID_ARG_TYPE = "RESULTS_GROUP_INVALID_ARG_TYPE"
    """Something other than a str was passed as the group"""
    RESULTS_GROUP_INVALID_ARG_VALUE = "RESULTS_GROUP_INVALID_ARG_VALUE"
    """The group must be a non-empty string"""
    RESULTS_TITLE_INVALID_ARG_TYPE = "RESULTS_TITLE_INVALID_ARG_TYPE"
    """Something other than a str was passed as the title arg"""
    RESULTS_TITLE_INVALID_ARG_VALUE = "RESULTS_TITLE_INVALID_ARG_VALUE"
    """The title arg passed must be a non-empty string"""
    RESULTS_DESCRIPTION_INVALID_ARG_TYPE = "RESULTS_DESCRIPTION_INVALID_ARG_TYPE"
    """Something other than a str was passed as the description arg"""
    RESULTS_N_INVALID_ARG_TYPE = "RESULTS_N_INVALID_ARG_TYPE"
    """Something other than an int was passed as the n arg"""
    RESULTS_N_INVALID_ARG_VALUE = "RESULTS_N_INVALID_ARG_VALUE"
    """The n arg passed must be greater than zero"""
    RESULTS_INTERVAL_UNIT_INVALID_ARG_TYPE = "RESULTS_INTERVAL_UNIT_INVALID_ARG_TYPE"
    """Something other than a str was passed as the interval_unit arg"""
    RESULTS_INTERVAL_UNIT_INVALID_ARG_VALUE = "RESULTS_INTERVAL_UNIT_INVALID_ARG_VALUE"
    """The interval_unit arg passed must be a non-empty string"""
    RESULTS_INTERVAL_SCALE_INVALID_ARG_TYPE = "RESULTS_INTERVAL_SCALE_INVALID_ARG_TYPE"
    """Something other than a float was passed as the interval_scale arg"""
    RESULTS_INTERVAL_SCALE_INVALID_ARG_VALUE = "RESULTS_INTERVAL_SCALE_INVALID_ARG_VALUE"
    """The interval_scale arg passed must be greater than zero"""
    RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_TYPE = "RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_TYPE"
    """Something other than a str was passed as the ops_per_interval_unit arg"""
    RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_VALUE = "RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_VALUE"
    """The ops_per_interval_unit arg passed must be a non-empty string"""
    RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_TYPE = "RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_TYPE"
    """Something other than a float was passed as the ops_per_interval_scale arg"""
    RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE = "RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE"
    """The ops_per_interval_scale arg passed must be greater than zero"""
    RESULTS_TOTAL_ELAPSED_INVALID_ARG_TYPE = "RESULTS_TOTAL_ELAPSED_INVALID_ARG_TYPE"
    """Something other than a float was passed as the total_elapsed arg"""
    RESULTS_TOTAL_ELAPSED_INVALID_ARG_VALUE = "RESULTS_TOTAL_ELAPSED_INVALID_ARG_VALUE"
    """The total_elapsed arg passed must be greater than zero"""
    RESULTS_VARIATION_MARKS_INVALID_ARG_TYPE = "RESULTS_VARIATION_MARKS_INVALID_ARG_TYPE"
    """Something other than a dict of str to str was passed as the variation_marks arg"""
    RESULTS_VARIATION_MARKS_INVALID_ARG_KEY_TYPE = "RESULTS_VARIATION_MARKS_INVALID_ARG_KEY_TYPE"
    """Something other than a str was found as a key in the dict passed as the variation_marks arg"""
    RESULTS_VARIATION_MARKS_INVALID_ARG_VALUE_TYPE = "RESULTS_VARIATION_MARKS_INVALID_ARG_VALUE_TYPE"
    """Something other than a str was found as a value in the dict passed as the variation_marks arg"""
    RESULTS_EXTRA_INFO_INVALID_ARG_TYPE = "RESULTS_EXTRA_INFO_INVALID_ARG_TYPE"
    """Something other than a dict was passed as the extra_info arg"""
    RESULTS_OPS_PER_SECOND_INVALID_ARG_TYPE = "RESULTS_OPS_PER_SECOND_INVALID_ARG_TYPE"
    """Something other than an OperationsPerInterval instance was passed as the ops_per_second arg"""
    RESULTS_PER_ROUND_TIMINGS_INVALID_ARG_TYPE = "RESULTS_PER_ROUND_TIMINGS_INVALID_ARG_TYPE"
    """Something other than an OperationTimings instance was passed as the per_round_timings arg"""
    RESULTS_ITERATIONS_INVALID_ARG_TYPE = "RESULTS_ITERATIONS_INVALID_ARG_TYPE"
    """Something other than a Sequence of Iteration instances was passed as the iterations arg"""
    RESULTS_ITERATIONS_INVALID_ARG_IN_SEQUENCE = "RESULTS_ITERATIONS_INVALID_ARG_IN_SEQUENCE"
    """Something other than an Iteration instance was found in the Sequence passed as the iterations arg"""
    RESULTS_VARIATION_COLS_INVALID_ARG_TYPE = "RESULTS_VARIATION_COLS_INVALID_ARG_TYPE"
    """Something other than a dict of str to str was passed as the variation_cols arg"""
    RESULTS_VARIATION_COLS_INVALID_ARG_KEY_TYPE = "RESULTS_VARIATION_COLS_INVALID_ARG_KEY_TYPE"
    """Something other than a str was found as a key in the dict passed as the variation_cols arg"""
    RESULTS_VARIATION_COLS_INVALID_ARG_KEY_VALUE = "RESULTS_VARIATION_COLS_INVALID_ARG_KEY_VALUE"
    """An empty string was found as a key in the dict passed as the variation_cols arg"""
    RESULTS_VARIATION_COLS_INVALID_ARG_VALUE_TYPE = "RESULTS_VARIATION_COLS_INVALID_ARG_VALUE_TYPE"
    """Something other than a str was found as a value in the dict passed as the variation_cols arg"""
    RESULTS_RESULTS_SECTION_INVALID_SECTION_ARG_TYPE = "RESULTS_RESULTS_SECTION_INVALID_SECTION_ARG_TYPE"
    """Something other than a Section enum was passed as the results_sections arg"""
    RESULTS_RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE = "RESULTS_RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE"
    """Something other than a Section.OPS or Section.TIMING was passed to the Results.result_section() method"""
    RESULTS_MEMORY_INVALID_ARG_TYPE = "RESULTS_MEMORY_INVALID_ARG_TYPE"
    """Something other than a MemoryUsage instance was passed as the memory arg"""
    RESULTS_PEAK_MEMORY_INVALID_ARG_TYPE = "RESULTS_PEAK_MEMORY_INVALID_ARG_TYPE"
    """Something other than a PeakMemoryUsage instance was passed as the peak_memory arg"""

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

    # Iteration() tags
    ITERATION_INIT_N_ARG_TYPE = "ITERATION_INIT_N_ARG_TYPE"
    """Invalid n argument passed to the Iteration() constructor - must be an int"""
    ITERATION_INIT_N_ARG_VALUE = "ITERATION_INIT_N_ARG_VALUE"
    """Invalid n argument passed to the Iteration() constructor - must be greater than zero"""
    ITERATION_INIT_ELAPSED_ARG_TYPE = "ITERATION_INIT_ELAPSED_ARG_TYPE"
    """Invalid elapsed argument passed to the Iteration() constructor - must be an int"""
    ITERATION_INIT_ELAPSED_ARG_VALUE = "ITERATION_INIT_ELAPSED_ARG_VALUE"
    """Invalid elapsed argument passed to the Iteration() constructor - must be zero or greater"""
    ITERATION_INIT_MEMORY_ARG_TYPE = "ITERATION_INIT_MEMORY_ARG_TYPE"
    """Invalid memory argument passed to the Iteration() constructor - must be an int"""
    ITERATION_INIT_PEAK_MEMORY_ARG_TYPE = "ITERATION_INIT_PEAK_MEMORY_ARG_TYPE"
    """Invalid peak_memory argument passed to the Iteration() constructor - must be an int"""
    ITERATION_INIT_UNIT_ARG_TYPE = "ITERATION_INIT_UNIT_ARG_TYPE"
    """Invalid unit argument passed to the Iteration() constructor - must be a str"""
    ITERATION_INIT_UNIT_ARG_VALUE = "ITERATION_INIT_UNIT_ARG_VALUE"
    """Invalid unit argument passed to the Iteration() constructor - must be a non-empty str"""
    ITERATION_INIT_SCALE_ARG_TYPE = "ITERATION_INIT_SCALE_ARG_TYPE"
    """Invalid scale argument passed to the Iteration() constructor - must be a float"""
    ITERATION_INIT_SCALE_ARG_VALUE = "ITERATION_INIT_SCALE_ARG_VALUE"
    """Invalid scale argument passed to the Iteration() constructor - must be greater than zero"""
    ITERATION_SET_PER_ROUND_ELAPSED_ARG_TYPE = "ITERATION_SET_PER_ROUND_ELAPSED_ARG_TYPE"
    """Invalid per_round_elapsed type of value assigned to per_round_elapsed attribute - must be a float"""
    ITERATION_SET_PER_ROUND_ELAPSED_ARG_VALUE = "ITERATION_SET_PER_ROUND_ELAPSED_ARG_VALUE"
    """Invalid per_round_elapsed value assigned to per_round_elapsed attribute - must be a non-negative float"""
    ITERATION_SET_MEMORY_ARG_TYPE = "ITERATION_SET_MEMORY_ARG_TYPE"
    """Invalid memory argument passed to the Iteration.memory setter - must be an int"""
    ITERATION_SET_PEAK_MEMORY_ARG_TYPE = "ITERATION_SET_PEAK_MEMORY_ARG_TYPE"
    """Invalid peak_memory argument passed to the Iteration.peak_memory setter - must be an int"""
    ITERATION_ITERATION_SECTION_INVALID_SECTION_ARG_TYPE = "ITERATION_ITERATION_SECTION_INVALID_SECTION_ARG_TYPE"
    """Something other than a Section instance was passed to the Iteration.iteration_section() method"""
    ITERATION_ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE = (
        "ITERATION_ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE")
    """The requested section is not supported by the Iteration.iteration_section() method"""
    ITERATION_SET_N_ARG_TYPE = "ITERATION_SET_N_ARG_TYPE"
    """Invalid n type of value assigned to n attribute - must be an int"""
    ITERATION_SET_N_ARG_VALUE = "ITERATION_SET_N_ARG_VALUE"
    """Invalid n value assigned to n attribute - must be greater than zero"""

    # Case() tags
    CASE_INVALID_GROUP_TYPE = "CASE_INVALID_GROUP_TYPE"
    """Invalid group argument type passed to the Case() constructor"""
    CASE_INVALID_GROUP_VALUE = "CASE_INVALID_GROUP_VALUE"
    """Invalid group argument value passed to the Case() constructor"""
    CASE_INVALID_TITLE_TYPE = "CASE_INVALID_TITLE_TYPE"
    """Invalid title argument type passed to the Case() constructor"""
    CASE_INVALID_TITLE_VALUE = "CASE_INVALID_TITLE_VALUE"
    """Invalid title argument value passed to the Case() constructor"""
    CASE_INVALID_DESCRIPTION_TYPE = "CASE_INVALID_DESCRIPTION_TYPE"
    """Invalid description argument type passed to the Case() constructor"""
    CASE_INVALID_DESCRIPTION_VALUE = "CASE_INVALID_DESCRIPTION_VALUE"
    """Invalid description argument value passed to the Case() constructor"""
    CASE_INVALID_ITERATIONS_TYPE = "CASE_INVALID_ITERATIONS_TYPE"
    """Invalid iterations argument type passed to the Case() constructor"""
    CASE_INVALID_ITERATIONS_VALUE = "CASE_INVALID_ITERATIONS_VALUE"
    """Invalid iterations argument value passed to the Case() constructor"""
    CASE_INVALID_WARMUP_ITERATIONS_TYPE = "CASE_INVALID_WARMUP_ITERATIONS_TYPE"
    """Invalid warmup_iterations argument type passed to the Case() constructor"""
    CASE_INVALID_WARMUP_ITERATIONS_VALUE = "CASE_INVALID_WARMUP_ITERATIONS_VALUE"
    """Invalid warmup_iterations argument value passed to the Case() constructor"""
    CASE_INVALID_MIN_TIME_TYPE = "CASE_INVALID_MIN_TIME_TYPE"
    """Invalid min_time argument type passed to the Case() constructor"""
    CASE_INVALID_MIN_TIME_VALUE = "CASE_INVALID_MIN_TIME_VALUE"
    """Invalid min_time argument value passed to the Case() constructor"""
    CASE_INVALID_MAX_TIME_TYPE = "CASE_INVALID_MAX_TIME_TYPE"
    """Invalid max_time argument type passed to the Case() constructor"""
    CASE_INVALID_MAX_TIME_VALUE = "CASE_INVALID_MAX_TIME_VALUE"
    """Invalid max_time argument value passed to the Case() constructor"""
    CASE_INVALID_TIME_RANGE = "CASE_INVALID_TIME_RANGE"
    """max_time must be greater than or equal to min_time in the Case() constructor"""
    CASE_INVALID_NAME = "CASE_INVALID_NAME"
    """Something other than a non-empty string was passed to the Case() constructor as the name arg"""
    CASE_INVALID_DESCRIPTION = "CASE_INVALID_DESCRIPTION"
    """Something other than a string was passed to the Case() constructor as the description arg"""
    CASE_INVALID_RUNNER_NOT_CALLABLE_OR_NONE = "CASE_INVALID_RUNNER_NOT_CALLABLE_OR_NONE"
    """Something other than a callable (function or method) was passed to the Case() constructor as the runner arg"""
    CASE_INVALID_ACTION_NOT_CALLABLE = "CASE_INVALID_ACTION_NOT_CALLABLE"
    """Something other than a callable (function or method) was passed to the Case() constructor as the action arg"""
    CASE_INVALID_SETUP = "CASE_INVALID_SETUP"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the setup arg"""
    CASE_INVALID_TEARDOWN = "CASE_INVALID_TEARDOWN"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the teardown arg"""
    CASE_INVALID_VARIATION_COLS_NOT_DICT = "CASE_INVALID_VARIATION_COLS_NOT_DICT"
    """Something other than a dictionary was passed to the Case() constructor as the variation_cols arg"""
    CASE_INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS = "CASE_INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS"
    """Something other than string keys and string or number values were found in the dictionary passed to
    the Case() constructor as the variation_cols arg"""
    CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT = "CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT"
    """Something other than a dictionary was passed to the Case() constructor as the kwargs_variations arg"""
    CASE_INVALID_OPTIONS_NOT_LIST = "CASE_INVALID_OPTIONS_NOT_LIST"
    """Something other than a list was passed to the Case() constructor as the options arg"""
    CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION = "CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION"
    """Something other than a ReporterOptions instance was found in the list passed to the Case() constructor
    as the options arg"""
    CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE = "CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the callback arg"""
    CASE_SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT = "CASE_SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT"
    """Something other than a Section instance was passed to the Case() constructor as the section arg"""
    CASE_SECTION_MEAN_INVALID_SECTION_ARGUMENT = "CASE_SECTION_MEAN_INVALID_SECTION_ARGUMENT"
    """Something other than Section.OPS or Section.TIMING was passed to the Case.section_mean() method"""
    CASE_INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS = "CASE_INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS"
    """Something other than a SimpleRunner or a subclass was passed to the Case() constructor as the runner arg"""
    CASE_INVALID_ACTION_MISSING_BENCH_PARAMETER = "CASE_INVALID_ACTION_MISSING_BENCH_PARAMETER"
    """The action function is missing the required 'bench' parameter."""
    CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER = "CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER"
    """The action function is missing the required '**kwargs' parameter."""
    CASE_INVALID_VARIATION_COLS_ENTRY_KEY_TYPE = "CASE_INVALID_VARIATION_COLS_ENTRY_KEY_TYPE"
    """The variation_cols dictionary contains a key that is not type str"""
    CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS = "CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS"
    """The variation_cols dictionary contains a key that does not appear in kwargs_variations."""
    CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING = "CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING"
    """The variation_cols dictionary contains a value that is not a string."""
    CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK = "CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK"
    """The variation_cols dictionary contains a value that is a blank string."""
    CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE = "CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE"
    """The kwargs_variations dictionary contains a key that is not type str"""
    CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER = "CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER"
    """The kwargs_variations dictionary contains a key that is not a valid Python identifier."""
    CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST = "CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST"
    """The kwargs_variations dictionary contains a value that is not a list."""
    CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST = "CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST"
    """The kwargs_variations dictionary contains a value that is an empty list."""
    CASE_INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS = "CASE_INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS"
    """The callback function must accept exactly four parameters: the Case instance, a Section instance,
    a Format instance, and a value (which may be of any type.)"""
    CASE_INVALID_ACTION_INCORRECT_SIGNATURE = "CASE_INVALID_ACTION_INCORRECT_SIGNATURE"
    """The action function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter."""
    CASE_INVALID_ACTION_PARAMETER_COUNT = "CASE_INVALID_ACTION_PARAMETER_COUNT"
    """The action function must accept exactly two parameters: a 'bench' parameter and a '**kwargs' parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER")
    """The callback function is missing the required 'case' parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE")
    """The callback function's 'case' parameter must be type Case."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_NOT_KEYWORD_ONLY = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'case' parameter must be a keyword-only parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER")
    """The callback function is missing the required 'section' parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE")
    """The callback function's 'section' parameter must be type Section."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'section' parameter must be a keyword-only parameter."""
    SECTION_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY = (
        "SECTION_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'section' parameter must be a keyword-only parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER")
    """The callback function is missing the required 'output_format' parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE")
    """The callback function's 'output_format' parameter must be type Format."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_NOT_KEYWORD_ONLY = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'output_format' parameter must be a keyword-only parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER")
    """The callback function is missing the required 'output' parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_NOT_KEYWORD_ONLY = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'output' parameter must be a keyword-only parameter."""
    CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE = (
        "CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE")
    """The callback function's 'output' parameter must have a type annotation."""
    CASE_MODIFY_READONLY_GROUP = "CASE_MODIFY_READONLY_GROUP"
    """The group attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_TITLE = "CASE_MODIFY_READONLY_TITLE"
    """The title attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_DESCRIPTION = "CASE_MODIFY_READONLY_DESCRIPTION"
    """The description attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_NAME = "CASE_MODIFY_READONLY_NAME"
    """The name attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_RUNNER = "CASE_MODIFY_READONLY_RUNNER"
    """The runner attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_ACTION = "CASE_MODIFY_READONLY_ACTION"
    """The action attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_ITERATIONS = "CASE_MODIFY_READONLY_ITERATIONS"
    """The iterations attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_WARMUP_ITERATIONS = "CASE_MODIFY_READONLY_WARMUP_ITERATIONS"
    """The warmup_iterations attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_MIN_TIME = "CASE_MODIFY_READONLY_MIN_TIME"
    """The min_time attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_MAX_TIME = "CASE_MODIFY_READONLY_MAX_TIME"
    """The max_time attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_VARIATION_COLS = "CASE_MODIFY_READONLY_VARIATION_COLS"
    """The variation_cols attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_KWARGS_VARIATIONS = "CASE_MODIFY_READONLY_KWARGS_VARIATIONS"
    """The kwargs_variations attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_OPTIONS = "CASE_MODIFY_READONLY_OPTIONS"
    """The options attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_CALLBACK = "CASE_MODIFY_READONLY_CALLBACK"
    """The callback attribute is read-only and cannot be modified."""
    CASE_MODIFY_READONLY_RESULTS = "CASE_MODIFY_READONLY_RESULTS"
    """The results attribute is read-only and cannot be modified."""
    CASE_INVALID_RESULTS_NOT_LIST = "CASE_INVALID_RESULTS_NOT_LIST"
    """Something other than a list was assigned to the results attribute"""
    CASE_INVALID_RESULTS_ENTRY_NOT_RESULTS_INSTANCE = "CASE_INVALID_RESULTS_ENTRY_NOT_RESULTS_INSTANCE"
    """Something other than a Results instance was found in the list assigned to the results attribute"""
    CASE_INVALID_CALLBACK_UNRESOLVABLE_HINTS = "CASE_INVALID_CALLBACK_UNRESOLVABLE_HINTS"
    """The type hints for the callback function could not be resolved."""
    CASE_INVALID_DEFAULT_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS = "CASE_INVALID_DEFAULT_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS"
    """Attempted to set a default runner for Case that is not a SimpleRunner or a subclass."""
    CASE_BENCHMARK_ACTION_RAISED_EXCEPTION = "CASE_BENCHMARK_ACTION_RAISED_EXCEPTION"
    """The action function raised an exception during execution."""

    # Results() tags
    RESULTS_RESULTS_SECTION_INVALID_SECTION_TYPE_ARGUMENT = "RESULTS_RESULT_SECTION_INVALID_SECTION_TYPE_ARGUMENT"
    """Something other than a Section instance was passed to the Results.result_section() method"""
    RESULTS_RESULTS_SECTION_UNSUPPORTED_SECTION_ARGUMENT = "RESULTS_RESULT_SECTION_UNSUPPORTED_SECTION_ARGUMENT"
    """Something other than Section.OPS or Section.TIMING was passed to the Results.result_section() method"""

    # Session() tags
    SESSION_INIT_INVALID_CASES_SEQUENCE_ARG = "SESSION_INIT_INVALID_CASES_SEQUENCE_ARG"
    """Something other than a Sequence of Case instances was passed to the Session() constructor"""
    SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE = "SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE"
    """Something other than a Case instance was found in the Sequence passed to the Session() constructor"""
    SESSION_INIT_INVALID_VERBOSITY_ARG = "SESSION_INIT_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the Session() constructor"""
    SESSION_INIT_INVALID_OUTPUT_PATH_ARG = "SESSION_INIT_INVALID_OUTPUT_PATH_ARG"
    """Something other than a Path instance was passed to the Session() constructor as the path arg"""
    SESSION_PROPERTY_INVALID_CASES_ARG = "SESSION_PROPERTY_INVALID_CASES_ARG"
    """Something other than a Sequence of Case instances was passed to the cases property"""
    SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE = "SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE"
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    SESSION_PROPERTY_INVALID_VERBOSITY_ARG = "SESSION_PROPERTY_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the verbosity property"""
    SESSION_PROPERTY_INVALID_CASE_ARG = "SESSION_PROPERTY_INVALID_CASE_ARG"
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    SESSION_PROPERTY_INVALID_PROGRESS_ARG = "SESSION_PROPERTY_INVALID_PROGRESS_ARG"
    """Something other than a bool was passed to the progress property"""
    SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG = "SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG"
    """Something other than a Path instance was passed to the output_path property"""
    SESSION_RUN_NO_CASES_TO_RUN = "SESSION_RUN_NO_CASES_TO_RUN"
    """No benchmark cases were found to run"""
    SESSION_REPORT_INVALID_CHOICE_RETRIEVED = "SESSION_REPORT_INVALID_CHOICE_RETRIEVED"
    """Something other than a Choice instance was retrieved from the report"""
    SESSION_REPORT_OUTPUT_PATH_NOT_SET = "SESSION_REPORT_OUTPUT_PATH_NOT_SET"
    """The output path must be set to generate reports"""
    SESSION_PARSE_ARGS_INVALID_ARGSPARSER_ARG = "SESSION_PARSE_ARGS_INVALID_ARGSPARSER_ARG"
    """Something other than an ArgumentParser instance was passed to the Session.parse_args() method"""
    SESSION_INVALID_ARGSPARSER_ARG = "SESSION_INVALID_ARGSPARSER_ARG"
    """Something other than an ArgumentParser instance was assigned to the args_parser property"""
    SESSION_PROPERTY_INVALID_ARGS_ARG = "SESSION_PROPERTY_INVALID_ARGS_ARG"
    """Something other than a Namespace instance was found in the args property"""
    SESSION_PROPERTY_INVALID_DEFAULT_RUNNER_ARG = "SESSION_PROPERTY_INVALID_DEFAULT_RUNNER_ARG"
    """Something other than a subclass of SimpleRunner or None was assigned to the default_runner property"""
    SESSION_PROPERTY_INVALID_CONSOLE_ARG = "SESSION_PROPERTY_INVALID_CONSOLE_ARG"
    """Something other than a Console instance was assigned to the console property"""

    # Reporters() tags
    REPORTERS_REGISTER_INVALID_REPORTER_ARG = "REPORTERS_REGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the Reporters.register() method"""
    REPORTERS_REGISTER_DUPLICATE_NAME = "REPORTERS_REGISTER_DUPLICATE_NAME"
    """A Reporter with the same name already exists in the Reporters instance"""
    REPORTERS_UNREGISTER_UNKNOWN_NAME = "REPORTERS_UNREGISTER_UNKNOWN_NAME"
    """No Reporter with the given name is registered in the Reporters instance"""
    REPORTERS_UNREGISTER_INVALID_NAME_ARG = "REPORTERS_UNREGISTER_INVALID_NAME_ARG"
    """Something other than a string was passed to the Reporters.unregister() method"""

    # RichTableReporter() tags
    RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG = "RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the RichTableReporter() constructor"""
    RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG = "RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the RichTableReporter() constructor"""
    RICH_TABLE_REPORTER_REPORT_INVALID_CASE_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_SESSION_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_CHOICE_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_SECTION = "RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the RichTableReporter.report() method in the Choice.sections"""
    RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_TARGET = "RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the RichTableReporter.report() method in the Choice.targets"""
    RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_FORMAT = "RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the RichTableReporter.report() method in the Choice.formats"""
    RICH_TABLE_REPORTER_REPORT_MISSING_PATH_ARG = "RICH_TABLE_REPORTER_REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_PATH_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_CALLBACK_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the RichTableReporter.report() method as the callback argument"""

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

    # GraphReporter() tags
    GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_THEME_TYPE = "GRAPH_REPORTER_GRAPH_OPTIONS_INVALID_THEME_TYPE"
    """The theme specified in the GraphOptions has an invalid type. It must be a dict or None."""
    GRAPH_REPORTER_INIT_INVALID_CASE_ARG = "GRAPH_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter() constructor"""
    GRAPH_REPORTER_INIT_INVALID_SESSION_ARG = "GRAPH_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the GraphReporter() constructor"""
    GRAPH_REPORTER_REPORT_INVALID_CASE_ARG = "GRAPH_REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG = "GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG = "GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION = "GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the GraphReporter.report() method in the Choice.sections"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET = "GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the GraphReporter.report() method in the Choice.targets"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT = "GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the GraphReporter.report() method in the Choice.formats"""
    GRAPH_REPORTER_REPORT_MISSING_PATH_ARG = "GRAPH_REPORTER_REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_PATH_ARG = "GRAPH_REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG = "GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the GraphReporter.report() method as the callback argument"""
    GRAPH_REPORTER_RUN_REPORT_INVALID_PATH_ARG = "GRAPH_REPORTER_RUN_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.run_report() method as the path arg"""
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
    """Something other than a Case instance was passed to the GraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG = "GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_SECTION_ARG = "GRAPH_REPORTER_PLOT_INVALID_SECTION_ARG"
    """Something other than a valid Section was passed to the GraphReporter.plot() method"""

    # JSONReporter() tags
    JSON_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION = "JSON_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the JSONReporter.run_report() method in the choice.sections"""

    # RichTask() tags
    RICH_TASK_INIT_INVALID_NAME_ARG = "RICH_TASK_INIT_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichTask() constructor"""
    RICH_TASK_INIT_INVALID_DESCRIPTION_ARG = "RICH_TASK_INIT_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichTask() constructor"""
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

    # reporters.Choice() tags
    CHOICE_INIT_INVALID_REPORTER_ARG = "CHOICE_INIT_INVALID_REPORTER_ARG"
    """Something other than a ReporterProtocol instance was passed to the Choice() constructor"""
    CHOICE_INIT_INVALID_RUNNER_ARG = "CHOICE_INIT_INVALID_RUNNER_ARG"
    """Something other than a callable (function or method) was passed to the Choice() constructor"""
    CHOICE_INIT_INVALID_NAME_ARG = "CHOICE_INIT_INVALID_NAME_ARG"
    """Something other than a string was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_STRING_NAME = "CHOICE_INIT_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    CHOICE_INIT_INVALID_DESCRIPTION_ARG = "CHOICE_INIT_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_STRING_DESCRIPTION = "CHOICE_INIT_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    CHOICE_INIT_INVALID_SECTIONS_ARG = "CHOICE_INIT_INVALID_SECTIONS_ARG"
    """Something other than a set of Section enums was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_SECTIONS = "CHOICE_INIT_EMPTY_SECTIONS"
    """The sections arg cannot be an empty set"""
    CHOICE_INIT_INVALID_TARGETS_ARG = "CHOICE_INIT_INVALID_TARGETS_ARG"
    """Something other than a set of Target enums was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_TARGETS = "CHOICE_INIT_EMPTY_TARGETS"
    """The targets arg cannot be an empty set"""
    CHOICE_INIT_INVALID_FORMATS_ARG = "CHOICE_INIT_INVALID_FORMATS_ARG"
    """Something other than a set of Format enums was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_FORMATS = "CHOICE_INIT_EMPTY_FORMATS"
    """The formats arg cannot be an empty set"""

    # reporters.Choices() tags
    CHOICES_INIT_INVALID_CHOICES_ARG_TYPE = "CHOICES_INIT_INVALID_CHOICES_ARG_TYPE"
    """Something other than a Sequence of Choice instances was passed to the Choices() constructor"""
    CHOICES_ADD_INVALID_CHOICE_ARG = "CHOICES_ADD_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the Choices.add() method"""
    CHOICES_ADD_DUPLICATE_CHOICE_NAME = "CHOICES_ADD_DUPLICATE_CHOICE_NAME"
    """A Choice with the same name already exists in the Choices instance"""
    CHOICES_ADD_DUPLICATE_CLI_ARG = "CHOICES_ADD_DUPLICATE_CLI_ARG"
    """A Choice with the same CLI argument already exists in the Choices instance"""
    CHOICES_EXTEND_INVALID_CHOICES_ARG = "CHOICES_EXTEND_INVALID_CHOICES_ARG"
    """Something other than a Choices instance was passed to the Choices.extend() method"""
    CHOICES_EXTEND_INVALID_CHOICES_CONTENT = "CHOICES_EXTEND_INVALID_CHOICES_CONTENT"
    """Something other than a Choice instance was found in the Choices instance passed to the Choices.extend() method"""
    CHOICES_EXTEND_DUPLICATE_CHOICE_NAME = "CHOICES_EXTEND_DUPLICATE_CHOICE_NAME"
    """A Choice with the same name already exists in the Choices instance"""
    CHOICES_EXTEND_DUPLICATE_CLI_ARG = "CHOICES_EXTEND_DUPLICATE_CLI_ARG"
    """A Choice with the same CLI argument already exists in the Choices instance"""
    CHOICES_CHOICE_FOR_FLAG_INVALID_ARG = "CHOICES_CHOICE_FOR_FLAG_INVALID_ARG"
    """Something other than a string was passed to the Choices.choice_for_flag() method"""
    CHOICES_GET_CHOICE_BY_CLI_TAG_INVALID_ARG = "CHOICES_GET_CHOICE_BY_CLI_TAG_INVALID_ARG"
    """Something other than a string was passed to the Choices.get_choice_by_cli_tag() method"""
    CHOICES_ALL_CHOICE_FLAGS_INVALID_RETURN = "CHOICES_ALL_CHOICE_FLAGS_INVALID_RETURN"
    """Something other than a set of strings was returned from the Choices.all_choice_flags() method"""
    CHOICES_REMOVE_UNKNOWN_CHOICE_NAME = "CHOICES_REMOVE_UNKNOWN_CHOICE_NAME"
    """No Choice with the given name exists in the Choices instance"""
    CHOICES_ADD_DUPLICATE_CHOICE_FLAG = "CHOICES_ADD_DUPLICATE_CHOICE_FLAG"
    """A Choice with the same CLI argument already exists in the Choices instance"""

    # Reporter() tags
    REPORTER_NOT_IMPLEMENTED = "REPORTER_NOT_IMPLEMENTED"
    """The Reporter base class is an abstract base class and must be subclassed"""
    REPORTER_INIT_NOT_IMPLEMENTED = "REPORTER_INIT_NOT_IMPLEMENTED"
    """The Reporter base class cannot be instantiated directly"""
    REPORTER_CHOICES_NOT_IMPLEMENTED = "REPORTER_CHOICES_NOT_IMPLEMENTED"
    """The Reporter.choices property must be implemented in subclasses"""
    REPORTER_LOAD_CHOICES_NOT_IMPLEMENTED = "REPORTER_LOAD_CHOICES_NOT_IMPLEMENTED"
    """The Reporter._load_choices() method must be implemented in subclasses"""
    REPORTER_NAME_NOT_IMPLEMENTED = "REPORTER_NAME_NOT_IMPLEMENTED"
    """The Reporter.name property must be initialized as a str by subclasses"""
    REPORTER_NAME_INVALID_VALUE = "REPORTER_NAME_INVALID_VALUE"
    """The Reporter.name property must be initialized as a non-empty string by subclasses"""
    REPORTER_DESCRIPTION_NOT_IMPLEMENTED = "REPORTER_DESCRIPTION_NOT_IMPLEMENTED"
    """The Reporter.description property must be initialized as a str by subclasses"""
    REPORTER_DESCRIPTION_INVALID_VALUE = "REPORTER_DESCRIPTION_INVALID_VALUE"
    """The Reporter.description property must be initialized as a string by subclasses"""
    REPORTER_RUN_REPORT_NOT_IMPLEMENTED = "REPORTER_RUN_REPORT_NOT_IMPLEMENTED"
    """The Reporter.run_report() method must be implemented by subclasses"""
    REPORTER_ADD_FLAGS_NOT_IMPLEMENTED = "REPORTER_ADD_FLAGS_NOT_IMPLEMENTED"
    """The Reporter.add_flags_to_argparse() method must be implemented in subclasses"""
    REPORTER_FORMATS_NOT_IMPLEMENTED = "REPORTER_FORMATS_NOT_IMPLEMENTED"
    """The Reporter.formats property must be implemented in subclasses"""
    REPORTER_INVALID_FORMATS_ENTRY_TYPE = "REPORTER_INVALID_FORMATS_ENTRY_TYPE"
    """Something other than a Format enum was found in the formats argument."""
    REPORTER_SECTIONS_NOT_IMPLEMENTED = "REPORTER_SECTIONS_NOT_IMPLEMENTED"
    """The Reporter.sections property must be implemented in subclasses"""
    REPORTER_INVALID_SECTIONS_ENTRY_TYPE = "REPORTER_INVALID_SECTIONS_ENTRY_TYPE"
    """Something other than a Section enum was found in the sections argument."""
    REPORTER_TARGETS_NOT_IMPLEMENTED = "REPORTER_TARGETS_NOT_IMPLEMENTED"
    """The Reporter.targets property must be implemented in subclasses"""
    REPORTER_INVALID_TARGETS_ENTRY_TYPE = "REPORTER_INVALID_TARGETS_ENTRY_TYPE"
    """Something other than a Target enum was found in the targets argument."""
    REPORTER_REPORT_INVALID_CASE_ARG = "REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_CHOICE_ARG = "REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_SESSION_ARG = "REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_PATH_ARG = "REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_CALLBACK_ARG = "REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the Reporter.report() method as the callback argument"""
    REPORTER_REPORT_UNSUPPORTED_SECTION = "REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the Reporter.report() method in the Choice.sections"""
    REPORTER_REPORT_UNSUPPORTED_TARGET = "REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the Reporter.report() method in the Choice.targets"""
    REPORTER_REPORT_UNSUPPORTED_FORMAT = "REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the Reporter.report() method in the Choice.formats"""
    REPORTER_ADD_CHOICE_INVALID_ARG_TYPE = "REPORTER_ADD_CHOICE_INVALID_ARG_TYPE"
    """Something other than a Choice instance was passed to the Reporter.add_choice() method"""
    REPORTER_ADD_CHOICE_DUPLICATE_NAME = "REPORTER_ADD_CHOICE_DUPLICATE_NAME"
    """A Choice with the same name already exists in the Reporter instance"""
    REPORTER_ADD_CHOICE_DUPLICATE_CLI_ARG = "REPORTER_ADD_CHOICE_DUPLICATE_CLI_ARG"
    """A Choice with the same CLI argument already exists in the Reporter instance"""
    REPORTER_ADD_CHOICES_INVALID_ARG_TYPE = "REPORTER_ADD_CHOICES_INVALID_ARG_TYPE"
    """Something other than a Choices instance was passed to the Reporter.add_choices() method"""
    REPORTER_ADD_CHOICES_INVALID_CONTENT_TYPE = "REPORTER_ADD_CHOICES_INVALID_CONTENT_TYPE"
    """Something other than a Choice instance was found in the Choices instance passed to the
    Reporter.add_choices() method"""
    REPORTER_INVALID_CHOICES_ARG_TYPE = "REPORTER_INVALID_CHOICES_ARG_TYPE"
    """Something other than a Choices instance was passed as the choices argument to the Reporter constructor"""
    REPORTER_ADD_CHOICE_UNSUPPORTED_SECTION = "REPORTER_ADD_CHOICE_UNSUPPORTED_SECTION"
    """A Section in the Choice instance passed to the Reporter.add_choice() method is not supported by the Reporter"""
    REPORTER_ADD_CHOICE_UNSUPPORTED_TARGET = "REPORTER_ADD_CHOICE_UNSUPPORTED_TARGET"
    """A Target in the Choice instance passed to the Reporter.add_choice() method is not supported by the Reporter"""
    REPORTER_ADD_CHOICE_UNSUPPORTED_FORMAT = "REPORTER_ADD_CHOICE_UNSUPPORTED_FORMAT"
    """A Format in the Choice instance passed to the Reporter.add_choice() method is not supported by the Reporter"""
    REPORTER_ADD_FLAGS_INVALID_PARSER_ARG_TYPE = "REPORTER_ADD_FLAGS_INVALID_PARSER_ARG_TYPE"
    """Something other than an ArgumentParser instance was passed to the Reporter.add_flags_to_argparse() method"""
    REPORTER_ADD_FLAGS_ARGUMENT_ERROR = "REPORTER_ADD_FLAGS_ARGUMENT_ERROR"
    """An ArgumentError was raised when adding flags to the ArgumentParser instance"""

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

    # utils.sanitize_filename() tags
    UTILS_SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE = "UTILS_SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE"
    """The filename argument was not a str"""
    UTILS_SANITIZE_FILENAME_EMPTY_NAME_ARG = "UTILS_SANITIZE_FILENAME_EMPTY_NAME_ARG"
    """The filename argument was an empty str"""

    # si_units.si_scale() tags
    SI_UNITS_SI_SCALE_INVALID_UNIT_ARG_TYPE = "SI_UNITS_SI_SCALE_INVALID_UNIT_ARG_TYPE"
    """The unit argument was not a str"""
    SI_UNITS_SI_SCALE_INVALID_UNIT_ARG_VALUE = "SI_UNITS_SI_SCALE_INVALID_UNIT_ARG_VALUE"
    """The unit argument was an empty str"""
    SI_UNITS_SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE = "SI_UNITS_SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE"
    """The base_unit argument was not a str"""
    SI_UNITS_SI_SCALE_EMPTY_BASE_UNIT_ARG = "SI_UNITS_SI_SCALE_EMPTY_BASE_UNIT_ARG"
    """The base_unit argument was an empty str"""
    SI_UNITS_SI_SCALE_UNKNOWN_SI_UNIT_PREFIX = "SI_UNITS_SI_SCALE_UNKNOWN_SI_UNIT_PREFIX"
    """The specified SI unit is not recognized"""
    SI_UNITS_SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT = "SI_UNITS_SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT"
    """The specified SI unit and base unit do not match"""

    # si_units.si_unit_base() tags
    SI_UNITS_SI_UNIT_BASE_EMPTY_UNIT_ARG = "SI_UNITS_SI_UNIT_BASE_EMPTY_UNIT_ARG"
    """The unit argument was an empty str"""
    SI_UNITS_SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE = "SI_UNITS_SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE"
    """The unit argument was not a str"""
    SI_UNITS_SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX = "SI_UNITS_SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX"
    """The specified SI unit prefix is not recognized"""

    # si_units.si_scale_for_smallest() tags
    SI_UNITS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE = "SI_UNITS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE"
    """The numbers argument was not a list"""
    SI_UNITS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE = (
        "SI_UNITS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE")
    """One or more values in the numbers argument was not an int or float"""

    # si_units.si_scale_to_unit() tags
    SI_UNITS_SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE = "SI_UNITS_SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE"
    """The base_unit argument was not a str"""
    SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG = "SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG"
    """The base_unit argument was an empty str"""
    SI_UNITS_SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE = "SI_UNITS_SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE"
    """The current_unit argument was not a str"""
    SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG = "SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG"
    """The current_unit argument was an empty str"""
    SI_UNITS_SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE = "SI_UNITS_SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE"
    """The target_unit argument was not a str"""
    SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG = "SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG"
    """The target_unit argument was an empty str"""
    SI_UNITS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS = "SI_UNITS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS"
    """The specified base_unit, current_unit, target_unit are not all compatible"""

    # utils.kwargs_variations() tags
    UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE = "UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE"
    """The kwargs argument was not a dictionary"""
    UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE = "UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE"
    """A kwargs argument value was not a Sequence (e.g., list, tuple, set) or was a str or bytes instance"""

    # utils.sigfigs() tags
    UTILS_SIGFIGS_INVALID_NUMBER_ARG_TYPE = "UTILS_SIGFIGS_INVALID_NUMBER_ARG_TYPE"
    """The number argument was not an int or float"""
    UTILS_SIGFIGS_INVALID_FIGURES_ARG_TYPE = "UTILS_SIGFIGS_INVALID_FIGURES_ARG_TYPE"
    """The figures argument was not an int"""
    UTILS_SIGFIGS_INVALID_FIGURES_ARG_VALUE = "UTILS_SIGFIGS_INVALID_FIGURES_ARG_VALUE"
    """The figures argument was less than 1"""


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
        msg (str, positional): The error message.
        tag (ErrorTag): The tag code.
    """


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
        msg (str, positional): The error message.
        tag (ErrorTag): The tag code.
    """


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
        msg (str, positional): The error message.
        tag (ErrorTag): The tag code.
    """


class SimpleBenchNotImplementedError(TaggedException[NotImplementedError]):
    """Base class for all SimpleBench not implemented errors.

    It differs from a standard NotImplementedError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchRuntimeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str, positional): The error message.
        tag (ErrorTag): The tag code.
    """


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
        msg (str, positional): The error message.
        name (str | None): The attribute name.
        obj (object): The object the attribute was not found on.
        tag (ErrorTag): The tag code.
    """
    if version_info >= (3, 10):
        def __init__(self, *args: object, name: str | None = None, obj: object = ..., tag: ErrorTag) -> None:
            super().__init__(*args, name, obj, tag=tag)


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
        super().__init__(None, message, tag=tag)
        self.argument_name = argument_name
